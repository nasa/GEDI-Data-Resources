# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
Spatial and Temporal Querying of GEDI Version 2 Data in Python Script
Author: LP DAAC
Last Updated: 03/31/2023
See README for additional information:
https://github.com/nasa/GEDI-Data-Resources/blob/main/Executables/GEDI_Finder/README.md
---------------------------------------------------------------------------------------------------
"""
########################################## Import Packages ########################################
import requests as r
from datetime import datetime
import argparse
import sys
from shapely.geometry import box
import os

# --------------------------COMMAND LINE ARGUMENTS AND ERROR HANDLING---------------------------- #
# Set up argument and error handling
parser = argparse.ArgumentParser(description="Performs a spatial and temporal query for GEDI V2 data using NASA's CMR and exports downloadable links as a text file.")
parser.add_argument('--product', required=True, help='Specify the data product for your search query. Select from "GEDI01_B.002", "GEDI02_A.002", and "GEDI02_B.002".')
parser.add_argument('--start', required=False, help='Start date for time period of interest: valid format is mm/dd/yyyy (e.g. 10/20/2020).', default='04/25/2019')
parser.add_argument('--end', required=False, help='Start date for time period of interest: valid format is mm/dd/yyyy (e.g. 10/24/2020).', default=datetime.today().strftime ("%m/%d/%Y"))
parser.add_argument('--roi', required=True, help='Region of interest (ROI) to search the GEDI granules. \
                    Valid inputs is bounding box coordinates: LL_lon(Lower Left Longitude),LL_lat, UR_lon, UR_lat (Upper Right Latitude). Example: "-73.65,-12.64,-47.81,9.7"')
args = parser.parse_args()

########################################### Verify bounding box coords ########################################
ROI = args.roi

if len(ROI.split(',')) != 4:
        sys.exit("Valid roi options include: a comma separated string containing bounding box coordinates: 'LL-Lon,LL-Lat,UR-Lon,UR-Lat' (single quotes included)")
else:
    try:
        bbox = [float(rr.strip(']').strip('[').strip("'").strip('"').strip(' ')) for rr in ROI.split(',')]
    except ValueError:
        sys.exit('Invalid coordinate detected in roi provided. Valid bbox coordinates must be numbers (int or float).')
    
    # Check that bbox coords are within the bounds of geographic CRS
    if bbox[0] < -180 or bbox[0] > 180:
        sys.exit(f"{bbox[0]} is not a valid entry for LL-lon (valid range is -180 to 180)")
    if bbox[2] < -180 or bbox[2] > 180:
        sys.exit(f"{bbox[2]} is not a valid entry for UR-lon (valid range is -180 to 180)")
    if bbox[1] < -90 or bbox[1] > 90:
        sys.exit(f"{bbox[1]} is not a valid entry for LL-lat (valid range is -90 to 90)")
    if bbox[3] < -90 or bbox[3] > 90:
        sys.exit(f"{bbox[3]} is not a valid entry for UR-lat (valid range is -90 to 90)")
    
    # Shapely automatically flips coords based on min/max x, y
    bbox_shape = box(bbox[0],bbox[1],bbox[2],bbox[3]) 
    if  bbox_shape.is_valid:
        bounding_box = [b for b in bbox_shape.bounds]
        bbox_string = ''
        for b in bounding_box: bbox_string += f"{b},"
        bbox_string = bbox_string[:-1]
    else:
        sys.exit(f"{ROI} is not valid.")    

########################################### Verify DATES ########################################

start_date = args.start.strip("'").strip('"')  # Assign start date to variable 
end_date = args.end.strip("'").strip('"')      # Assign end date to variable

# Validate the format of the dates submitted
def date_validate(date):
    try:
        dated = datetime.strptime(date, '%m/%d/%Y')
    except:
        sys.exit(f"The date: {date} is not valid. The valid format is mm/dd/yyyy (e.g. 10/20/2020)")
    return dated

start, end = date_validate(start_date),  date_validate(end_date)

# Verify that start date is either the same day or before end date
if start > end:
    sys.exit(f"The Start Date requested: {start} is after the End Date Requested: {end}.")
else:      
    # Change the date format to match CMR-STAC requirements
    dates = f'{start.strftime("%Y")}-{start.strftime("%m")}-{start.strftime("%d")}T00:00:00Z/{end.strftime("%Y")}-{end.strftime("%m")}-{end.strftime("%d")}T23:59:59Z'                  

########################################### Verify Products ########################################
prod = args.product

# Create dictionary of shortnames for GEDI products
concept_ids = {'GEDI01_B.002': 'C2142749196-LPCLOUD', 'GEDI02_A.002': 'C2142771958-LPCLOUD', 'GEDI02_B.002': 'C2142776747-LPCLOUD'}

if prod in concept_ids:
    concept_id = concept_ids[prod]
else:
    print(f'{prod} is not a valid GEDI product. Select from "GEDI01_B.002", "GEDI02_A.002", and "GEDI02_B.002".')
##################################### Define Function to Query CMR ################################

def gedi_finder(concept_id, bbox, dates):
    
    # Define the base CMR granule search url, including LPDAAC provider name and max page size (2000 is the max allowed)
    cmr = "https://cmr.earthdata.nasa.gov/search/granules.json?pretty=true&provider=LPCLOUD&page_size=2000&concept_id="
    
    
    # CMR uses pagination for queries with more features returned than the page size
    page = 1
    # bbox = bbox.replace(' ', '')  # Remove any white spaces
    try:
        # Send GET request to CMR granule search endpoint w/ product concept ID, bbox & page number, format return as json
        cmr_response = r.get(f"{cmr}{concept_id}&bounding_box={bbox}&temporal={dates}&pageNum={page}").json()['feed']['entry']
        # If 2000 features are returned, move to the next page and submit another request, and append to the response
        while len(cmr_response) % 2000 == 0:
            page += 1
            cmr_response += r.get(f"{cmr}{concept_id}&bounding_box={bbox}&pageNum={page}").json()['feed']['entry']
        # CMR returns more info than just the Data Pool links, below use list comprehension to return a list of DP links
        return [c['links'][0]['href'] for c in cmr_response]
    except:
        # If the request did not complete successfully, print out the response from CMR
        print(r.get(f"{cmr}{concept_id}&bounding_box={bbox}&pageNum={page}").json())
        
################################ Execute GEDI Finder Function #####################################
# User-provided inputs (UPDATE FOR YOUR DESIRED PRODUCT AND BOUNDING BOX REGION OF INTEREST)
# product = 'GEDI02_B.002'           # Options include 'GEDI01_B.002', 'GEDI02_A.002', 'GEDI02_B.002'
# bbox = '-73.65,-12.64,-47.81,9.7'  # bounding box coordinates in LL Longitude, LL Latitude, UR Longitude, UR Latitude format

# Call the gedi_finder function using the user-provided inputs
granules = gedi_finder(concept_id, bbox_string, dates)
print(f"{len(granules)} {prod} Version 2 granules found.")

#################################### Export Results ###############################################
# Set up output textfile name using the current datetime
outName = f"{prod.replace('.', '_')}_GranuleList_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

# Open file and write each granule link on a new line
with open(outName, "w") as gf:
    for g in granules:
        gf.write(f"{g}\n")
print(f"File containing links to intersecting {prod} Version 2 data has been saved to:\n {os.getcwd()}\{outName}")