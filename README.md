# GEDI-Data-Resources  

Welcome! This repository provides guides, short how-tos, and tutorials to help users access and work with data from the Global Ecosystem Dynamics Investigation (GEDI) mission. In the interest of open science this repository has been made public but is still under active development. All Jupyter notebooks and scripts should be functional, however, changes or additions may be made. Contributions from all parties are welcome.  

---  

## GEDI Background  

The Global Ecosystem Dynamics Investigation ([GEDI](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/gedi-overview/)) mission aims to characterize ecosystem structure and dynamics to enable radically improved quantification and understanding of the Earth's carbon cycle and biodiversity. [GEDI](https://gedi.umd.edu/mission/mission-overview/) Level 1 and Level 2 Data Products are distributed by the Land Processes Distributed Active Archive Center ([LP DAAC](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/gedi-overview/)) and Level 3 and Level 4 Data Products are distributed by the [ORNL DAAC]([https://daac.ornl.gov/cgi-bin/dataset_lister.pl?p=40]).  

Search for and download GEDI _Version 2_ data products via a graphical user interface (GUI) using [NASA EarthData Search](https://search.earthdata.nasa.gov/search?q=%22GEDI%22) or programmatically using NASA's [Common Metadata Repository](https://cmr.earthdata.nasa.gov/search) (CMR).  

---  

## [GEDI V2 Data Products](https://lpdaac.usgs.gov/product_search/?collections=GEDI&status=Operational&view=cards&sort=title)  

- **GEDI L1B Geolocated Waveform Data Global Footprint Level - [GEDI01_B.002](https://doi.org/10.5067/GEDI/GEDI01_B.002)**  
- **GEDI L2A Elevation and Height Metrics Data Global Footprint Level - [GEDI02_A.002](https://doi.org/10.5067/GEDI/GEDI02_A.002)**  
- **GEDI L2B Canopy Cover and Vertical Profile Metrics Data Global Footprint Level - [GEDI02_B.002](https://doi.org/10.5067/GEDI/GEDI02_B.002)**  

---  

## Prerequisites/Setup Instructions  

Instructions for setting up a compatible environment for working with GEDI data are linked to below.
- [`Python` set up instructions](setup/setup_instructions_python.md)

---  

## Getting Started  

### Clone or download the [GEDI-Data-Resources repository](https://github.com/nasa/GEDI-Data-Resources).  

- [Download](https://github.com/nasa/GEDI-Data-Resources/archive/refs/heads/main.zip)  
- To clone the repository, type `git clone https://github.com/nasa/GEDI-Data-Resources.git` in the command line.  

## Repository Contents  

Content in this repository is divided into Python and R tutorials/scripts. The tutorials walk you through workin with GEDI data step by step while the scripts are command line executables. 

| Repository Contents | Summary | Path |
|----|-----|----|
| **[GEDI_L1B_V2_Tutorial.ipynb](https://github.com/nasa/GEDI-Data-Resources/blob/main/python/tutorials/GEDI_L1B_V2_Tutorial.ipynb)** | Jupyter Notebook tutorial demonstrating how to work with the Geolocated Waveform GEDI01_B.002 data product using Python | `python\tutorials` |
| **[GEDI_L2A_V2_Tutorial.ipynb](https://github.com/nasa/GEDI-Data-Resources/blob/main/python/tutorials/GEDI_L2A_V2_Tutorial.ipynb)** | Jupyter Notebook tutorial demonstrating how to work with the Geolocated Waveform GEDI02_A.002 data product using Python | `python\tutorials` |
| **[GEDI_L2B_V2_Tutorial.ipynb](https://github.com/nasa/GEDI-Data-Resources/blob/main/python/tutorials/GEDI_L2B_V2_Tutorial.ipynb)** | Jupyter Notebook tutorial demonstrating how to how to work with the Geolocated Waveform GEDI02_B.002 data product using Python  | `python\tutorials` |
| **[GEDI_Finder_Tutorial_Python.ipynb](https://github.com/nasa/GEDI-Data-Resources/blob/main/python/tutorials/GEDI_Finder_Tutorial_Python.ipynb)** | Jupyter Notebook tutorial demonstrating how to perform spatial [bounding box] queries for GEDI V2 L1B, L2A, and L2B data using NASA's CMR, and how to reformat the CMR response into a list of links that will allow users to download the intersecting GEDI V2 sub-orbit granules directly from the LP DAAC Data Pool using Python | `python\tutorials` |
| **[GEDI_Finder_Tutorial_R.Rmd](https://github.com/nasa/GEDI-Data-Resources/blob/main/r/GEDI_Finder_Tutorial_R.rmd)** | R Markdown tutorial demonstrating how to use R to perform spatial [bounding box] queries for GEDI V2 L1B, L2A, and L2B data using NASA's CMR, and how to reformat the CMR response into a list of links that will allow users to download the intersecting GEDI V2 sub-orbit granules directly from the LP DAAC Data Pool  | `R` |
| **[GEDI_Finder.py](https://github.com/nasa/GEDI-Data-Resources/tree/main/python/scripts/GEDI_Finder)** | Command line executable performing spatial [bounding box] and temporal queries for GEDI V2 L1B, L2A, and L2B data using NASA's CMR and reformats the CMR response into a list of links that will allow users to download the intersecting GEDI V2 sub-orbit granules directly from the LP DAAC Data Pool.  | `python/scripts/GEDI_Finder` |
| **[GEDI_Subsetter.py](https://github.com/nasa/GEDI-Data-Resources/tree/main/python/scripts/GEDI_Subsetter)** | Command line executable converting GEDI data products, stored in Hierarchical Data Format version 5 (HDF5, .h5) into GeoJSON files that can be loaded into GIS and Remote Sensing Software | `python/scripts/GEDI_Subsetter` |


---  

## Helpful Links  

- [University of Maryland GEDI](https://gedi.umd.edu/) - Learn more about the GEDI Mission  
- [OpenAltimetry](https://openaltimetry.org/data/gedi/) - Learn about GEDI coverage  
- [LP DAAC Website](https://lpdaac.usgs.gov/)
- [LP DAAC GitHub](https://github.com/nasa/LPDAAC-Data-Resources)
- [NASA Earthdata Search](https://search.earthdata.nasa.gov/search)

---  

## Contact Info  

Email: LPDAAC@usgs.gov  
Voice: +1-866-573-3222  
Organization: Land Processes Distributed Active Archive Center (LP DAAC)¹  
Website: <https://lpdaac.usgs.gov/>  
Date last modified: 06-08-2023  

¹Work performed under USGS contract G15PD00467 for NASA contract NNG14HH33I.  
