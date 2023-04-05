# Spatial and Temporal Querying of GEDI Version 2 Data in Python

--- 
# Objective:
### The objective of this tutorial is to demonstrate how to perform spatial [bounding box] and temporal queries for GEDI V2 L1B, L2A, and L2B data, how to reformat the CMR response into a list of links that will allow users to download the intersecting GEDI V2 sub-orbit granules directly from the LP DAAC Data Pool.

--- 
# Script Execution

Once you have set up your environment and it has been activated, navigate to the directory containing the downloaded or cloned repo. The script requires a product shortname and region of interest as a bounding box.

> `python GEDI_Finder.py --product <Specify the data product from 'GEDI01_B.002', 'GEDI02_A.002', and 'GEDI02_B.002' for your search query.> --roi <insert bounding box coordinates here (LL_lon,LL_lat, UR_lon, UR_lat)> --start <Start date for time period of interest:valid format is mm/dd/yyyy> --end <Etart date for time period of interest:valid format is mm/dd/yyyy>`  

### Example

> `python GEDI_Finder.py --product GEDI02_B.002 --roi '-73.65,-12.64,-47.81,9.7' --start 10/20/2020 --end 10/30/2020`  


### Script Arguments  

To see the full set of command line arguments and how to use them, type the following in the command prompt:

```None
> python HLS_SuPER.py -h  

usage: GEDI_Finder.py [-h] --product PRODUCT [--start START] [--end END] --roi ROI
...
```

#### --product {"GEDI01_B.002", "GEDI02_A.002", "GEDI02_B.002"}

```None
(Required) Desired GEDI product.   

``` 
#### --roi ROI

```None
(Required) Region of Interest (ROI) for spatial query. Valid input is bounding box coordinates: 'LowerLeft_lon,LowerLeft_lat,UpperRight_lon,UpperRight_lat' NOTE: Negative coordinates MUST be
written in single quotation marks '-120,43,-118,48'. If you are using MacOS, you may need to use double quotes followed by single quotes "'-120,43,-118,48'".

```  

#### --start START

```None
(Optional) Start date for time period of interest: valid format is mm/dd/yyyy (e.g. 10/20/2020). (default: 04/25/2019)  

```  

#### --end END

```None
(Optional) End date for time period of interest: valid format is mm/dd/yyyy (e.g. 10/30/2020). (default: Today)  

```  
 

---
# Contact Information:
#### Author: LP DAAC¹   
**Contact:** LPDAAC@usgs.gov  
**Voice:** +1-866-573-3222  
**Organization:** Land Processes Distributed Active Archive Center (LP DAAC)  
**Website:** https://lpdaac.usgs.gov/  
**Date last modified:** 04-04-2023  

¹KBR, Inc., contractor to the U.S. Geological Survey, Earth Resources Observation and Science (EROS) Center,  
 Sioux Falls, South Dakota, USA. Work performed under USGS contract G15PD00467 for LP DAAC².  
²LP DAAC Work performed under NASA contract NNG14HH33I.
