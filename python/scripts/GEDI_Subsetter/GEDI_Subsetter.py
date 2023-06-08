#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
GEDI Spatial and Band/Layer Subsetting and Export to GeoJSON Script
Author: Cole Krehbiel
Last Updated: 04/13/2021
See README for additional information:
https://git.earthdata.nasa.gov/projects/LPDUR/repos/gedi-subsetter/browse/
---------------------------------------------------------------------------------------------------
"""
# Import necessary libraries
import os
import h5py
import pandas as pd
from shapely.geometry import Polygon
import geopandas as gp
import argparse
import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# --------------------------COMMAND LINE ARGUMENTS AND ERROR HANDLING---------------------------- #
# Set up argument and error handling
parser = argparse.ArgumentParser(description='Performs Spatial/Band Subsetting and Conversion to GeoJSON for GEDI L1-L2 files')
parser.add_argument('--dir', required=True, help='Local directory containing GEDI files to be processed')
parser.add_argument('--beams', required=False, help='Specific beams to be included in the output GeoJSON (default is all beams) \
                    BEAM0000,BEAM0001,BEAM0010,BEAM0011 are Coverage Beams. BEAM0101,BEAM0110,BEAM1000,BEAM1011 are Full Power Beams.')
parser.add_argument('--sds', required=False, help='Specific science datasets (SDS) to include in the output GeoJSON \
                    (see README for a list of available SDS and a list of default SDS returned for each product).')
parser.add_argument('--roi', required=True, help='Region of interest (ROI) to subset the GEDI orbit to in the output GeoJSON. \
                    Valid inputs are a geojson or .shp file or bounding box coordinates: ul_lat,ul_lon,lr_lat,lr_lon')
args = parser.parse_args()

# --------------------------------SET ARGUMENTS TO VARIABLES------------------------------------- #
# Options include a GeoJSON or a list of bbox coordinates
ROI = args.roi  

# Convert to Shapely polygon for geojson, .shp or bbox
if ROI.endswith('json') or ROI.endswith('.shp'):
    try:
        ROI = gp.GeoDataFrame.from_file(ROI)
        ROI.crs = 'EPSG:4326'
        if len(ROI) > 1:
            print('Multi-feature polygon detected. Only the first feature will be used to subset the GEDI data.')
        ROI = ROI.geometry[0]
    except:
        print('error: unable to read input geojson file or the file was not found')
        sys.exit(2)
else:
    ROI = ROI.replace("'", "")
    ROI = ROI.split(',')
    ROI = [float(r) for r in ROI]
    try:
        ROI = Polygon([(ROI[1], ROI[0]), (ROI[3], ROI[0]), (ROI[3], ROI[2]), (ROI[1], ROI[2])]) 
    except:
        print('error: unable to read input bounding box coordinates, the required format is: ul_lat,ul_lon,lr_lat,lr_lon')
        sys.exit(2)

# Keep the exact input geometry for the final clip to ROI
finalClip = gp.GeoDataFrame(index=[0], geometry=[ROI], crs='EPSG:4326')  
print (finalClip)

# Format and set input/working directory from user-defined arg
if args.dir[-1] != '/' and args.dir[-1] != '\\':
    inDir = args.dir.strip("'").strip('"') + os.sep
else:
    inDir = args.dir

# Find input directory
try:
    os.chdir(inDir)
except FileNotFoundError:
    print('error: input directory (--dir) provided does not exist or was not found')
    sys.exit(2)

# Define beam subset if provided or default to all beams        
if args.beams is not None:
    beamSubset = args.beams.split(',')
else:
    beamSubset = ['BEAM0000', 'BEAM0001', 'BEAM0010', 'BEAM0011', 'BEAM0101', 'BEAM0110', 'BEAM1000', 'BEAM1011']

# Define additional layers to subset if provided    
if args.sds is not None:
    layerSubset = args.sds.split(',')
else:
    layerSubset = None
    
# -------------------------------------SET UP WORKSPACE------------------------------------------ #
# Create and set output directory
outDir = os.path.normpath((os.path.split(inDir)[0] + os.sep + 'output')) + os.sep
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Create list of GEDI HDF-EOS5 files in the directory
gediFiles = [o for o in os.listdir() if o.endswith('.h5') and 'GEDI' in o]

# --------------------DEFINE PRESET BAND/LAYER SUBSETS ------------------------------------------ #
# Default layers to be subset and exported, see README for information on how to add additional layers
l1bSubset = [ '/geolocation/latitude_bin0', '/geolocation/longitude_bin0', '/channel', '/shot_number',
             '/rxwaveform','/rx_sample_count', '/stale_return_flag', '/tx_sample_count', '/txwaveform',
             '/geolocation/degrade', '/geolocation/delta_time', '/geolocation/digital_elevation_model',
              '/geolocation/solar_elevation',  '/geolocation/local_beam_elevation',  '/noise_mean_corrected',
             '/geolocation/elevation_bin0', '/geolocation/elevation_lastbin', '/geolocation/surface_type', '/geolocation/digital_elevation_model_srtm']
l2aSubset = ['/lat_lowestmode', '/lon_lowestmode', '/channel', '/shot_number', '/degrade_flag', '/delta_time', 
             '/digital_elevation_model', '/elev_lowestmode', '/quality_flag', '/rh', '/sensitivity', '/digital_elevation_model_srtm', 
             '/elevation_bias_flag', '/surface_flag',  '/num_detectedmodes',  '/selected_algorithm',  '/solar_elevation']
l2bSubset = ['/geolocation/lat_lowestmode', '/geolocation/lon_lowestmode', '/channel', '/geolocation/shot_number',
             '/cover', '/cover_z', '/fhd_normal', '/pai', '/pai_z',  '/rhov',  '/rhog',
             '/pavd_z', '/l2a_quality_flag', '/l2b_quality_flag', '/rh100', '/sensitivity',  
             '/stale_return_flag', '/surface_flag', '/geolocation/degrade_flag',  '/geolocation/solar_elevation',
             '/geolocation/delta_time', '/geolocation/digital_elevation_model', '/geolocation/elev_lowestmode']
 
# -------------------IMPORT GEDI FILES AS GEODATAFRAMES AND CLIP TO ROI-------------------------- #   
# Loop through each GEDI file and export as a point geojson
l = 0
for g in gediFiles:
    l += 1
    print(f"Processing file: {g} ({l}/{len(gediFiles)})")
    gedi = h5py.File(g, 'r')      # Open file
    gediName = g.split('.h5')[0]  # Keep original filename
    gedi_objs = []            
    gedi.visit(gedi_objs.append)  # Retrieve list of datasets  

    # Search for relevant SDS inside data file
    gediSDS = [str(o) for o in gedi_objs if isinstance(gedi[o], h5py.Dataset)] 
    
    # Define subset of layers based on product
    if 'GEDI01_B' in g:
        sdsSubset = l1bSubset
    elif 'GEDI02_A' in g:
        sdsSubset = l2aSubset 
    else:
        sdsSubset = l2bSubset
    
    # Append additional datasets if provided
    if layerSubset is not None:
        [sdsSubset.append(y) for y in layerSubset]
    
    # Subset to the selected datasets
    gediSDS = [c for c in gediSDS if any(c.endswith(d) for d in sdsSubset)]
        
    # Get unique list of beams and subset to user-defined subset or default (all beams)
    beams = []
    for h in gediSDS:
        beam = h.split('/', 1)[0]
        if beam not in beams and beam in beamSubset:
            beams.append(beam)

    gediDF = pd.DataFrame()  # Create empty dataframe to store GEDI datasets    
    del beam, gedi_objs, h
    
    # Loop through each beam and create a geodataframe with lat/lon for each shot, then clip to ROI
    for b in beams:
        beamSDS = [s for s in gediSDS if b in s]
        
        # Search for latitude, longitude, and shot number SDS
        lat = [l for l in beamSDS if sdsSubset[0] in l][0]  
        lon = [l for l in beamSDS if sdsSubset[1] in l][0]
        shot = f'{b}/shot_number'          
        
        # Open latitude, longitude, and shot number SDS
        shots = gedi[shot][()]
        lats = gedi[lat][()]
        lons = gedi[lon][()]
        
        # Append BEAM, shot number, latitude, longitude and an index to the GEDI dataframe
        geoDF = pd.DataFrame({'BEAM': len(shots) * [b], shot.split('/', 1)[-1].replace('/', '_'): shots,
                              'Latitude':lats, 'Longitude':lons, 'index': np.arange(0, len(shots), 1)})
        
        # Convert lat/lon coordinates to shapely points and append to geodataframe
        geoDF = gp.GeoDataFrame(geoDF, geometry=gp.points_from_xy(geoDF.Longitude, geoDF.Latitude))
        
        # Clip to only include points within the user-defined bounding box
        geoDF = geoDF[geoDF['geometry'].within(ROI.envelope)]    
        gediDF = gediDF.append(geoDF)
        del geoDF
    
    # Convert to geodataframe and add crs
    gediDF = gp.GeoDataFrame(gediDF)
    gediDF.crs = 'EPSG:4326'
    
    if gediDF.shape[0] == 0:
        print(f"No intersecting shots were found between {g} and the region of interest submitted.")
        continue
    del lats, lons, shots
    
# --------------------------------OPEN SDS AND APPEND TO GEODATAFRAME---------------------------- #
    beamsDF = pd.DataFrame()  # Create dataframe to store SDS
    j = 0
    
    # Loop through each beam and extract subset of defined SDS
    for b in beams:
        beamDF = pd.DataFrame()
        beamSDS = [s for s in gediSDS if b in s and not any(s.endswith(d) for d in sdsSubset[0:3])]
        shot = f'{b}/shot_number'
        
        try:
            # set up indexes in order to retrieve SDS data only within the clipped subset from above
            mindex = min(gediDF[gediDF['BEAM'] == b]['index'])
            maxdex = max(gediDF[gediDF['BEAM'] == b]['index']) + 1
            shots = gedi[shot][mindex:maxdex]
        except ValueError:
            print(f"No intersecting shots found for {b}")
            continue
        # Loop through and extract each SDS subset and add to DF
        for s in beamSDS:
            j += 1
            sName = s.split('/', 1)[-1].replace('/', '_')

            # Datasets with consistent structure as shots
            if gedi[s].shape == gedi[shot].shape:
                beamDF[sName] = gedi[s][mindex:maxdex]  # Subset by index
            
            # Datasets with a length of one 
            elif len(gedi[s][()]) == 1:
                beamDF[sName] = [gedi[s][()][0]] * len(shots) # create array of same single value
            
            # Multidimensional datasets
            elif len(gedi[s].shape) == 2 and 'surface_type' not in s: 
                allData = gedi[s][()][mindex:maxdex]
                
                # For each additional dimension, create a new output column to store those data
                for i in range(gedi[s].shape[1]):
                    step = []
                    for a in allData:
                        step.append(a[i])
                    beamDF[f"{sName}_{i}"] = step
            
            # Waveforms
            elif s.endswith('waveform') or s.endswith('pgap_theta_z'):
                waveform = []
                
                if s.endswith('waveform'):
                    # Use sample_count and sample_start_index to identify the location of each waveform
                    start = gedi[f'{b}/{s.split("/")[-1][:2]}_sample_start_index'][mindex:maxdex]
                    count = gedi[f'{b}/{s.split("/")[-1][:2]}_sample_count'][mindex:maxdex]
                
                # for pgap_theta_z, use rx sample start index and count to subset
                else:
                    # Use sample_count and sample_start_index to identify the location of each waveform
                    start = gedi[f'{b}/rx_sample_start_index'][mindex:maxdex]
                    count = gedi[f'{b}/rx_sample_count'][mindex:maxdex]
                wave = gedi[s][()]
                
                # in the dataframe, each waveform will be stored as a list of values
                for k in range(len(start)):
                    singleWF = wave[int(start[k] - 1): int(start[k] - 1 + count[k])]
                    waveform.append(','.join([str(q) for q in singleWF]))
                beamDF[sName] = waveform
            
            # Surface type 
            elif s.endswith('surface_type'):
                surfaces = ['land', 'ocean', 'sea_ice', 'land_ice', 'inland_water']
                allData = gedi[s][()]
                for i in range(gedi[s].shape[0]):
                    beamDF[f'{surfaces[i]}'] = allData[i][mindex:maxdex]
                del allData
            else:
                print(f"SDS: {s} not found")
            print(f"Processing {j} of {len(beamSDS) * len(beams)}: {s}")
        
        beamsDF = beamsDF.append(beamDF)
    del beamDF, beamSDS, beams, gedi, gediSDS, shots, sdsSubset
    
    # Combine geolocation dataframe with SDS layer dataframe
    outDF = pd.merge(gediDF, beamsDF, left_on='shot_number', right_on=[sn for sn in beamsDF.columns if sn.endswith('shot_number')][0])
    outDF.index = outDF['index']
    del gediDF, beamsDF   
    
    # Subset the output DF to the actual boundary of the input ROI
    outDF = gp.overlay(outDF, finalClip)
# --------------------------------EXPORT AS GEOJSON---------------------------------------------- #
    # Check for empty output dataframe
    try:    
        # Export final geodataframe as Geojson
        outDF.to_file(f"{outDir}{g.replace('.h5', '.geojson')}", driver='GeoJSON')
        print(f"{g.replace('.h5', '.json')} saved at: {outDir}")
    except ValueError:
        print(f"{g} intersects the bounding box of the input ROI, but no shots intersect final clipped ROI.")
