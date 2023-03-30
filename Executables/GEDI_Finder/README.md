# Spatial Querying of GEDI Version 2 Data in Python

---
# Objective:
### The objective of this tutorial is to demonstrate how current GEDI Finder users can update their workflow for GEDI Version 2 (V2) data using NASA's CMR to perform spatial [bounding box] queries for GEDI V2 L1B, L2A, and L2B data, and how to reformat the CMR response into a list of links that will allow users to download the intersecting GEDI V2 sub-orbit granules directly from the LP DAAC Data Pool.

The Global Ecosystem Dynamics Investigation ([GEDI](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/gedi-overview/)) mission aims to characterize ecosystem structure and dynamics to enable radically improved quantification and understanding of the Earth's carbon cycle and biodiversity. The Land Processes Distributed Active Archive Center (LP DAAC) distributes the GEDI Level 1 and Level 2 Version 1 and Version 2 products. The LP DAAC created the GEDI Finder _Web Service_ to allow users to perform spatial queries of GEDI _Version 1_ L1-L2 full-orbit granules. One of the updates for GEDI _Version 2_ included additional spatial metadata that allows users to perform spatial queries via a graphical user interface (GUI) using NASA's [Earthdata Search](https://search.earthdata.nasa.gov/search) or programmatically using NASA's [Common Metadata Repository](https://cmr.earthdata.nasa.gov/search) (CMR). Another update is that each GEDI V1 full-orbit granule has been divided into 4 sub-orbit granules in V2.   

## Materials:  
 - The [Spatial Querying of GEDI Version 2 Data in Python Jupyter Notebook](https://git.earthdata.nasa.gov/projects/LPDUR/repos/gedi-finder-tutorial-python/browse/GEDI_Finder_Tutorial_Python.ipynb) shows step-by-step how to write a function to query CMR for a specific GEDI V2 product and bounding box region of interest, format the response into a list of links to download the intersecting GEDI data, and export the list to a text file.  
 - The [GEDI_Finder.py Python script](https://git.earthdata.nasa.gov/projects/LPDUR/repos/gedi-finder-tutorial-python/browse/GEDI_Finder.py) can be used to update current GEDI Finder workflows from the web service API endpoint to a CMR-based solution.     

## Products Used:
**1. [GEDI01_B.002](https://doi.org/10.5067/GEDI/GEDI01_B.002)**   
**2. [GEDI02_A.002](https://doi.org/10.5067/GEDI/GEDI02_A.002)**   
**3. [GEDI02_B.002](https://doi.org/10.5067/GEDI/GEDI02_B.002)**     

---
# Prerequisites:
This tutorial uses packages included in the Python Standard Library. Any `Python 3.X` installation should be able to execute the code. However, in order to execute the `Jupyter Notebook`, users will need to set up a Python environment that includes an installation of Jupyter Notebook.   

---
# Procedures:
## Getting Started:  
#### 1.	Copy/clone/download the [GEDI Finder Tutorial repo](https://git.earthdata.nasa.gov/projects/LPDUR/repos/gedi-finder-tutorial-python/archive?format=zip), or download the [GEDI Finder Python script](https://git.earthdata.nasa.gov/projects/LPDUR/repos/gedi-finder-tutorial-python/browse/GEDI_Finder.py)    
## Python Environment Setup
It is recommended to use [Conda](https://conda.io/docs/), an environment manager to set up a compatible Python environment. Download Conda for your OS here: https://www.anaconda.com/download/. Once you have Conda installed, Follow the instructions below to successfully setup a Python environment on Linux, MacOS, or Windows.

This Python Jupyter Notebook tutorial has been tested using Python version 3.8. Conda was used to create the python environment.

 - Using your preferred command line interface (command prompt, terminal, cmder, etc.) type the following to successfully create a compatible python environment:
  > `conda create -n gedifinder -c conda-forge --yes python=3.8`   

  > `conda activate gedifinder`  

  > `jupyter notebook`  

If you do not have Jupyter Notebook installed, you may need to run:  
  > `conda install jupyter notebook`  

[Additional information](https://conda.io/docs/user-guide/tasks/manage-environments.html) on setting up and managing Conda environments.  

If you prefer to not install Conda, the same setup and dependencies can be achieved by using another package manager such as `pip`.   

#### Still having trouble getting a compatible Python environment set up? Contact [LP DAAC User Services](https://lpdaac.usgs.gov/lpdaac-contact-us/).    

---
# Contact Information:
#### Author: Cole Krehbiel¹   
**Contact:** LPDAAC@usgs.gov  
**Voice:** +1-866-573-3222  
**Organization:** Land Processes Distributed Active Archive Center (LP DAAC)  
**Website:** https://lpdaac.usgs.gov/  
**Date last modified:** 05-21-2021  

¹KBR, Inc., contractor to the U.S. Geological Survey, Earth Resources Observation and Science (EROS) Center,  
 Sioux Falls, South Dakota, USA. Work performed under USGS contract G15PD00467 for LP DAAC².  
²LP DAAC Work performed under NASA contract NNG14HH33I.
