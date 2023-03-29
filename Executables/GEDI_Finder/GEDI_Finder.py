# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
Spatial Querying of GEDI Version 2 Data in Python Script
Author: Cole Krehbiel
Last Updated: 05/10/2021
See README for additional information:
https://git.earthdata.nasa.gov/projects/LPDUR/repos/gedi-finder-tutorial-python/browse/
---------------------------------------------------------------------------------------------------
"""
########################################## Import Packages ########################################
import requests as r
from datetime import datetime
import os

##################################### Define Function to Query CMR ################################
def gedi_finder(product, bbox):
    
    # Define the base CMR granule search url, including LPDAAC provider name and max page size (2000 is the max allowed)
    cmr = "https://cmr.earthdata.nasa.gov/search/granules.json?pretty=true&provider=LPDAAC_ECS&page_size=2000&concept_id="
    
    # Set up dictionary where key is GEDI shortname + version and value is CMR Concept ID
    concept_ids = {'GEDI01_B.002': 'C1908344278-LPDAAC_ECS', 
                   'GEDI02_A.002': 'C1908348134-LPDAAC_ECS', 
                   'GEDI02_B.002': 'C1908350066-LPDAAC_ECS'}
    
    # CMR uses pagination for queries with more features returned than the page size
    page = 1
    bbox = bbox.replace(' ', '')  # Remove any white spaces
    try:
        # Send GET request to CMR granule search endpoint w/ product concept ID, bbox & page number, format return as json
        cmr_response = r.get(f"{cmr}{concept_ids[product]}&bounding_box={bbox}&pageNum={page}").json()['feed']['entry']
        
        # If 2000 features are returned, move to the next page and submit another request, and append to the response
        while len(cmr_response) % 2000 == 0:
            page += 1
            cmr_response += r.get(f"{cmr}{concept_ids[product]}&bounding_box={bbox}&pageNum={page}").json()['feed']['entry']
        
        # CMR returns more info than just the Data Pool links, below use list comprehension to return a list of DP links
        return [c['links'][0]['href'] for c in cmr_response]
    except:
        # If the request did not complete successfully, print out the response from CMR
        print(r.get(f"{cmr}{concept_ids[product]}&bounding_box={bbox.replace(' ', '')}&pageNum={page}").json())
        
################################ Execute GEDI Finder Function #####################################
# User-provided inputs (UPDATE FOR YOUR DESIRED PRODUCT AND BOUNDING BOX REGION OF INTEREST)
product = 'GEDI02_B.002'           # Options include 'GEDI01_B.002', 'GEDI02_A.002', 'GEDI02_B.002'
bbox = '-73.65,-12.64,-47.81,9.7'  # bounding box coordinates in LL Longitude, LL Latitude, UR Longitude, UR Latitude format

# Call the gedi_finder function using the user-provided inputs
granules = gedi_finder(product, bbox)
print(f"{len(granules)} {product} Version 2 granules found.")

#################################### Export Results ###############################################
# Set up output textfile name using the current datetime
outName = f"{product.replace('.', '_')}_GranuleList_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

# Open file and write each granule link on a new line
with open(outName, "w") as gf:
    for g in granules:
        gf.write(f"{g}\n")
print(f"File containing links to intersecting {product} Version 2 data has been saved to:\n {os.getcwd()}\{outName}")