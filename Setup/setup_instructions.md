# Repository Setup Instructions

The tutorials and Executables in this repository require a compatible Python Environment, an installation of [Git](https://git-scm.com/downloads), and GEDI granules to download. To setup the environment and download these files, follow the steps in sections 1 and 2. 

+ If you do not have an Environment Manager installed, we recommend  [Anaconda](https://www.anaconda.com/products/distribution) or [miniconda](https://docs.conda.io/en/latest/miniconda.html). When installing, be sure to check the box to "Add Anaconda to my PATH environment variable" to enable use of conda directly from your command line interface.  
+ If you do not have Git, you can download it [here](https://git-scm.com/downloads).  

## 1. Python Environment Setup

This Python Environment will work for all of the tutorials and executables within this repository. It is recommended to use Conda, an environment manager to set up a compatible Python environment. Download Conda for your OS here: https://www.anaconda.com/download/. Additional information on setting up and managing Conda environments can be found [here](https://conda.io/docs/user-guide/tasks/manage-environments.html). Once you have Conda installed, Follow the instructions below to successfully setup a Python environment on Linux, MacOS, or Windows.

This Python Jupyter Notebook tutorial has been tested using Python version 3.9. 

Using your preferred command line interface (command prompt, terminal, cmder, etc.) type the following to successfully create a compatible python environment:
> `conda create -n gedi -c conda-forge --yes python=3.9 h5py shapely geopandas pandas geoviews holoviews`

Next, activate the Python Environment that you just created.

> `conda activate gedi`

Now you can launch Jupyter Notebook to open the notebooks included.

> `jupyter notebook`

If you do not have Jupyter Notebook installed, you may need to run:

> `conda install jupyter notebook`

**Having trouble getting a compatible Python environment set up? Contact [LP DAAC User Services](https://lpdaac.usgs.gov/lpdaac-contact-us/).**
If you prefer to not install Conda, the same setup and dependencies can be achieved by using another package manager such as pip.


## 2. File Downloads  


These granules below are used within the tutorials. Click/copy the URLs into a browser to download. Save them into the `./Additional_files/` folder within this repository. You will need a [NASA Earth Data Search](https://search.earthdata.nasa.gov/search) login to download the data used in this tutorial. You can create an account at the link provided.   

+ L1B Granule - <https://e4ftl01.cr.usgs.gov/GEDI/GEDI01_B.002/2019.06.19/GEDI01_B_2019170155833_O02932_02_T02267_02_005_01_V002.h5>  
+ L2A Granule - <https://e4ftl01.cr.usgs.gov/GEDI/GEDI02_A.002/2019.06.19/GEDI02_A_2019170155833_O02932_02_T02267_02_003_01_V002.h5>  
+ L2B Granule - <https://e4ftl01.cr.usgs.gov/GEDI/GEDI02_B.002/2019.06.19/GEDI02_B_2019170155833_O02932_02_T02267_02_003_01_V002.h5>  

---

## Contact Info:  

Email: LPDAAC@usgs.gov  
Voice: +1-866-573-3222  
Organization: Land Processes Distributed Active Archive Center (LP DAAC)¹  
Website: <https://lpdaac.usgs.gov/>  
Date last modified: 03-28-2023  

¹Work performed under USGS contract G15PD00467 for NASA contract NNG14HH33I.  
