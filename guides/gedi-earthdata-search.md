# GEDI Version 2 Earthdata Search Guide

The Global Ecosystem Dynamics Investigation (GEDI) instrument aboard the International Space Station
(ISS) collects light detection and ranging (lidar) full waveform observations. The Level 1B Geolocated
Waveform Data ([GEDI01_B](https://doi.org/10.5067/GEDI/GEDI01_B.002)), Level 2A Elevation and Height Metrics Data ([GEDI02_A](https://doi.org/10.5067/GEDI/GEDI02_A.002)), and Level 2B
Canopy Cover and Vertical Profile Metrics Data ([GEDI02_B](https://doi.org/10.5067/GEDI/GEDI02_B.002)) granules are available through NASA’s Earthdata Search. This quick guide demonstrates how to find and subset GEDI Version 2 granules using Earthdata Search. GEDI Version 2 data are split into sub-orbit granules and contain the spatial metadata necessary to perform spatial queries in Earthdata Search.

This tutorial guides you through how to use NASA's [Earthdata Search](https://search.earthdata.nasa.gov/) to search for GEDI data containing only data for a region of interest (ROI) and for a temporal range. It also provides instruction on how to perform spatial and/or layer subsetting of GEDI sub-orbit granules in Earthdata Search and how to connect the search output (e.g. download or access links) to a programmatic workflow (locally or from within the cloud).  

## Step 1. Earthdata Search Login  

Earthdata Login credentials are required to download or access NASA Earth data products available at [Earthdata Search](https://search.earthdata.nasa.gov/). If you do not have an Earthdata account, create one at https://urs.earthdata.nasa.gov. 
Remember your username and password; and use it to log in to Earthdata Search.


## Step 2. Search for dataset of interest  

Search for a GEDI Version 2 collection by entering "GEDI v2"/"GEDI" or the dataset short name (e.g., GEDI01_B v002) into the search box in the upper left-hand corner of the page, and check the box for "Customizable" option under Feature options. The list of matching collections in the middle panel will be updated with your input. 
Hover over the collections and select your collection. 

![Image shows the collection search for GEDI granules in Earthdata Search](https://github.com/nasa/GEDI-Data-Resources/tree/main/img/collection.png)

### Step 3. Perform a Spatiotemporal Search for Granules

All available granules for the product will be included in the list of matching granules. The list of granules can be queried by temporal and/or spatial boundaries using the tools below the search bar in Earthdata Search.  
The temporal subsetting allows for user-provided start and end date/time and will return any available granules acquired between those dates.  
The spatial subsetting allows you to draw a polygon, circle, or rectangle region of interest to filter granules by location. Other spatial options include submitting a lat/lon point location, or uploading a KML, shapefile, GeoJSON, or GeoRSS.  

**Note** that there is an existing issue with uploading zipped shapefile currently.

![Image shows the spatiotemporal subset for GEDI granules in Earthdata Search](https://github.com/nasa/GEDI-Data-Resources/tree/main/img/granules.png)

### Step 4: Selecting Granules for Download  

Now that the results have been filtered to the desired temporal and spatial extent, you can see the footprints of the GEDI Version 2 sub-orbit granules intersecting your spatiotemporal query.  

Download all granules associated with the selected collection using the green button located in the bottom right-hand corner (Download All), select specific granules to add to an order using the add (**+**) button, or directly download the full granule using the icon.  

### Step 5: Spatial and Band/Layer Subsetting  

Once you click on the green **Download All** button, you will be directed to Edit Options tab. Under “Select a data access method,” select **Stage For Delivery** to download source files or select **Customize** to create subset of granules.

To set up the parameters for subsetting each granule to your region of interest, scroll down to the Spatial Subsetting section. Check the box next to "Click to enable" and it will populate the coordinates of the bounding box for the ROI.

To clip the granules to the exact boundaries of a GeoJSON or shapefile, deselect "Click to enable" and select "Use Shapefile from Search".

Select specific science dataset layers to extract by scrolling down to the Band Subsetting section. Expand the directories and select the desired GEDI beams and/or layers. Additional information for each of the data layers can be found on [GEDI product Digital Object Identifier (DOI) landing pages](https://lpdaac.usgs.gov/product_search/?collections=GEDI&status=Operational&view=cards&sort=title).
After the desired parameters for spatial and/or layer subsetting have been selected, click Done to complete the custom order form then click Download Data to initiate the order. 

![Image shows the customized option for GEDI data in Earthdata Search](https://github.com/nasa/GEDI-Data-Resources/tree/main/img/customize.png)

### Step 6: Retrieve Data  

When the data request is submitted, a Download Status screen will monitor the progress of the order.

The status update emails are sent to the email address associated with the Earthdata login credentials or specified in the custom order form. Check the status of the order in the [Download Status and History](https://search.earthdata.nasa.gov/downloads) page. The order completion email contains URLs for accessing the data outputs. Note that the URLs have an expiration date and are only valid for one week.

Contact LP DAAC User Services at <lpdaac@usgs.gov> with any questions about the request. Be sure to reference the request ID in any correspondence.

### Step 7: Download Data  

Download the output files by clicking on the .zip link in the email and unzipping into a local directory. Or, click on the .html link, which goes to a page including options to download files one by one, or download a .txt file containing links to all of the output files.   

Automate downloading by saving the .txt file and using command line utilities [wget](https://github.com/nasa/LPDAAC-Data-Resources/blob/main/guides/bulk_download_using_wget.md) and [curl](https://github.com/nasa/LPDAAC-Data-Resources/blob/main/guides/bulk_download_using_curl.md). Additionally, R or Python can be used to download data directly from the .txt or .csv file using the scripts provided in How to [Access the LP DAAC Data Pool with R](https://git.earthdata.nasa.gov/projects/LPDUR/repos/daac_data_download_r/browse) and [How to Access the LP DAAC Data Pool with Python](https://git.earthdata.nasa.gov/projects/LPDUR/repos/daac_data_download_python/browse/DAACDataDownload.py).


![Image shows the Dowanlaod Status page in Earthdata Search](https://github.com/nasa/GEDI-Data-Resources/tree/main/img/download.png)
