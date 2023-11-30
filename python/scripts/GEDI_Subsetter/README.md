# GEDI Spatial and Band/Layer Subsetting and Export to GeoJSON Script  

## Objective  

The GEDI_Subsetter.py script converts GEDI data products, stored in Hierarchical Data Format version 5 (HDF5, .h5) into GeoJSON files that can be loaded into GIS and Remote Sensing Software. When executing this script, a user will submit a desired region of interest (ROI) and input directory containing GEDI L1B-L2 files as command line arguments. The script begins by opening the GEDI products listed below that are contained in the input directory. Next, it uses the latitude and longitude arrays in the GEDI file to georeference each shot in the file. From there, the script performs spatial subsetting by using the user-submitted ROI to clip the GEDI shots in each file to only include those shots which fall within the bounding box of the region of interest (all GEDI shots and ROIs are treated as Geographic (EPSG:4326) coordinate reference system). By default, the script will loop through each of the eight GEDI beams and include all shots within the given ROI. There is an optional argument to subset for specific beams if needed. There are specific predefined datasets included in each output by product (see below) by default. However, if there are additional datasets within a given product that are desired, they can be included in the output geojson by specifying the optional `--sds` parameter when executing the script. For lists of all datasets in each GEDI L1B-L2 product, see below. The script then imports the data within the ROI for each of the desired GEDI datasets.  Ultimately, the script exports the spatial subset of desired datasets as a GeoJSON. By default, the script will loop through and perform the aforementioned steps for each GEDI L1B-L2 HDF5 file in the input directory. The output GeoJSON file will contain a row for each GEDI shot that was within the user-defined region of interest, and will contain columns for each of the desired layers. The output GeoJSONs can be brought into GIS or Remote Sensing Software and users can visualize each shot based on the layers contained in the attribute table of the output file.  

## Available Products  

1. **[GEDI01_B.002](https://doi.org/10.5067/GEDI/GEDI01_B.002)**  
2. **[GEDI02_A.002](https://doi.org/10.5067/GEDI/GEDI02_A.002)**  
3. **[GEDI02_B.002](https://doi.org/10.5067/GEDI/GEDI02_B.002)**  

---

## Prerequisites

*Disclaimer: This script has been tested on Windows and MacOS using the specifications identified below.*  

### Python version 3.10  
+ `h5py`  
+ `shapely`  
+ `geopandas`  
+ `pandas`  

---

## Procedures

### Getting Started

1. Download GEDI L1B-L2 Version 2 products from the [LP DAAC Data Pool](https://e4ftl01.cr.usgs.gov/GEDI/) or [Earthdata Search Client](https://search.earthdata.nasa.gov/search?q=GEDI) to a local directory (see above for applicable products).  

> **TIP:** Use the LP DAAC [GEDI Finder](https://lpdaacsvc.cr.usgs.gov/services/gedifinder) web service to input your bounding box region of interest and find the specific GEDI granules (files) intersecting your ROI. The service will return direct links to download the files you are looking for.  

2. Copy/clone/download [GEDI_Subsetter.py](https://git.earthdata.nasa.gov/projects/LPDUR/repos/gedi-subsetter/browse/GEDI_Subsetter.py) from the LP DAAC Data User Resources Repository  

### Python Environment Setup  

1. It is recommended to use [miniforge](https://github.com/conda-forge/miniforge), an environment manager, to set up a compatible Python environment. Download miniforge for your OS here: https://github.com/conda-forge/miniforge#miniforge3. Once you have miniforge installed, Follow the instructions below to successfully setup a Python environment on Windows, MacOS, or Linux.  
2. Setup  
    1. Open a new command line interface (MacOS/Linux: Terminal, Windows: Command Prompt) and type: `mamba create -n gedi_env -c conda-forge --yes python=3.10 h5py shapely geopandas pandas`  
    2. Navigate to the directory where you downloaded the `GEDI_Subsetter.py` script  
    3. Activate GEDI Python environment (created in step 1) in the Command Prompt/Terminal and Type:  
        - `activate gedi_env` on Windows  
        - `source activate gedi_env` on MacOS  

### Script Execution  

Once you have set up your environment and it has been activated, run the script with the following in the Command Prompt/Terminal window:  

**Examples**

1. python GEDI_Subsetter.py --dir <insert input directory with GEDI files here> --roi <insert geojson, shapefile, or bounding box coordinates here>  
    > `python GEDI_Subsetter.py --dir C:\Users\GEDI\ --roi LewisCountyWA.geojson`  
2. If you prefer to submit a bounding box, use the following format:  `python GEDI_Subsetter.py --dir <insert input directory with GEDI files here> --roi <UpperLeftLatitude,UpperLeftLongitude,LowerRightLatitude,LowerRightLongitude>` (comma separated with no spaces)  
    > `python GEDI_Subsetter.py --dir C:\Users\GEDI\ --roi 46.2,-122.8,42.1,-120.5`  

### Subsetting Layers  

The default functionality is to export each science dataset (SDS) layer contained in the default GEDI specification (see below) as a column contained in the output GeoJSON attribute table. If you prefer to export one or more layers not included by default, you can do so by adding the optional argument `--sds <insert SDS layer names desired>` (comma separated with no spaces, see below for specific SDS layer names by product).    

**Example**  
  > `python GEDI_Subsetter.py --dir C:\Users\GEDI\ --roi 46.2,-122.8,42.1,-120.5 --sds /all_samples_sum,/channel,/ancillary/mean_samples`  

See below for specific SDS layer names by product.  

### Subsetting Beams  

The default functionality is to export each desired layer for each of the eight GEDI beams. If you prefer to only include specific beams, you can do so by adding the optional argument `--beams` **in comma separated format** with no spaces between beams:  

**Example** (Full Power Beams only)  
  > `python GEDI_Subsetter.py --dir C:\Users\GEDI\ --roi 46.2,-122.8,42.1,-120.5 --beams BEAM0101,BEAM0110,BEAM1000,BEAM1011` 

### Considerations

- Due to the large file size of GEDI products and thousands of layers included in each file, processing times can take from **minutes to hours**. In order to speed up processing, be sure to clip to your exact region of interest and only include the Beams/layers needed for your research/application. This will also provide a faster experience when importing the output GeoJSON file into GIS or Remote Sensing software.  
- For multidimensional datasets, (ex: rh, which includes rh0 - rh100), each dimension will be split into a separate column in the output GeoJSON file (i.e. column rh0, column rh1, ... column rh99, column rh100)  
- For the `rxwaveform` and `txwaveform` datasets, each waveform will be stored as a comma separated list of the waveform values for each shot (ex: 230.6967,230.554,230.4744,...229.1028,228.6807,228.4076)  

### List of GEDI Layers by Product

**NOTE:** The layers in **BOLD** are the layers that are included in each output GeoJSON by default.    

#### GEDI01_B  
 - /all_samples_sum  
 - /ancillary/master_time_epoch  (Version 2 only)
 - /ancillary/mean_samples
 - /ancillary/smoothing_width
 - **/beam**
 - **/channel**
 - /geolocation/altitude_instrument
 - /geolocation/altitude_instrument_error
 - /geolocation/bounce_time_offset_bin0
 - /geolocation/bounce_time_offset_bin0_error
 - /geolocation/bounce_time_offset_lastbin
 - /geolocation/bounce_time_offset_lastbin_error
 - **/geolocation/degrade**
 - **/geolocation/delta_time**
 - **/geolocation/digital_elevation_model**  
 - **/geolocation/digital_elevation_model_srtm** (Version 2 only)
 - **/geolocation/elevation_bin0**
 - /geolocation/elevation_bin0_error
 - /geolocation/elevation_lastbin
 - /geolocation/elevation_lastbin_error
 - **/geolocation/latitude_bin0**
 - /geolocation/latitude_bin0_error
 - /geolocation/latitude_instrument
 - /geolocation/latitude_instrument_error
 - /geolocation/latitude_lastbin
 - /geolocation/latitude_lastbin_error
 - /geolocation/local_beam_azimuth
 - /geolocation/local_beam_azimuth_error
 - **/geolocation/local_beam_elevation**
 - /geolocation/local_beam_elevation_error
 - **/geolocation/longitude_bin0**
 - /geolocation/longitude_bin0_error
 - /geolocation/longitude_instrument
 - /geolocation/longitude_instrument_error
 - /geolocation/longitude_lastbin
 - /geolocation/longitude_lastbin_error
 - /geolocation/mean_sea_surface
 - /geolocation/neutat_delay_derivative_bin0
 - /geolocation/neutat_delay_derivative_lastbin
 - /geolocation/neutat_delay_total_bin0
 - /geolocation/neutat_delay_total_lastbin
 - /geolocation/range_bias_correction  
 - /geolocation/shot_number  (Version 2 only)
 - /geolocation/solar_azimuth
 - **/geolocation/solar_elevation**
 - **/geolocation/surface_type**  
 - /geophys_corr/delta_time  (Version 2 only)
 - /geophys_corr/dynamic_atmosphere_correction
 - /geophys_corr/geoid
 - /geophys_corr/tide_earth
 - /geophys_corr/tide_load
 - /geophys_corr/tide_ocean
 - /geophys_corr/tide_ocean_pole
 - /geophys_corr/tide_pole
 - /master_frac
 - /master_int
 - **/noise_mean_corrected**
 - /noise_stddev_corrected
 - /nsemean_even
 - /nsemean_odd
 - /rx_energy
 - /rx_offset
 - /rx_open
 - **/rx_sample_count**
 - /rx_sample_start_index
 - **/rxwaveform**
 - /selection_stretchers_x
 - /selection_stretchers_y
 - **/shot_number**
 - **/stale_return_flag**
 - /th_left_used
 - /tx_egamplitude
 - /tx_egamplitude_error
 - /tx_egbias
 - /tx_egbias_error
 - /tx_egflag
 - /tx_eggamma
 - /tx_eggamma_error
 - /tx_egsigma
 - /tx_egsigma_error
 - /tx_gloc
 - /tx_gloc_error
 - /tx_pulseflag
 - **/tx_sample_count**
 - /tx_sample_start_index
 - **/txwaveform**

#### GEDI02_A  
 - /ancillary/l2a_alg_count
 - **/beam**
 - **/channel**
 - **/degrade_flag**
 - **/delta_time**
 - **/digital_elevation_model**  
 - **/digital_elevation_model_srtm** (Version 2 only)
 - /elev_highestreturn
 - **/elev_lowestmode**
 - **/elevation_bias_flag**
 - /elevation_bin0_error
 - /energy_total
 - /geolocation/elev_highestreturn_a1
 - /geolocation/elev_highestreturn_a2
 - /geolocation/elev_highestreturn_a3
 - /geolocation/elev_highestreturn_a4
 - /geolocation/elev_highestreturn_a5
 - /geolocation/elev_highestreturn_a6
 - /geolocation/elev_lowestmode_a1
 - /geolocation/elev_lowestmode_a2
 - /geolocation/elev_lowestmode_a3
 - /geolocation/elev_lowestmode_a4
 - /geolocation/elev_lowestmode_a5
 - /geolocation/elev_lowestmode_a6
 - /geolocation/elev_lowestreturn_a1
 - /geolocation/elev_lowestreturn_a2
 - /geolocation/elev_lowestreturn_a3
 - /geolocation/elev_lowestreturn_a4
 - /geolocation/elev_lowestreturn_a5
 - /geolocation/elev_lowestreturn_a6
 - /geolocation/elevation_1gfit
 - /geolocation/elevs_allmodes_a1
 - /geolocation/elevs_allmodes_a2
 - /geolocation/elevs_allmodes_a3
 - /geolocation/elevs_allmodes_a4
 - /geolocation/elevs_allmodes_a5
 - /geolocation/elevs_allmodes_a6
 - /geolocation/energy_lowestmode_a1
 - /geolocation/energy_lowestmode_a2
 - /geolocation/energy_lowestmode_a3
 - /geolocation/energy_lowestmode_a4
 - /geolocation/energy_lowestmode_a5
 - /geolocation/energy_lowestmode_a6
 - /geolocation/lat_highestreturn_a1
 - /geolocation/lat_highestreturn_a2
 - /geolocation/lat_highestreturn_a3
 - /geolocation/lat_highestreturn_a4
 - /geolocation/lat_highestreturn_a5
 - /geolocation/lat_highestreturn_a6
 - /geolocation/lat_lowestmode_a1
 - /geolocation/lat_lowestmode_a2
 - /geolocation/lat_lowestmode_a3
 - /geolocation/lat_lowestmode_a4
 - /geolocation/lat_lowestmode_a5
 - /geolocation/lat_lowestmode_a6
 - /geolocation/lat_lowestreturn_a1
 - /geolocation/lat_lowestreturn_a2
 - /geolocation/lat_lowestreturn_a3
 - /geolocation/lat_lowestreturn_a4
 - /geolocation/lat_lowestreturn_a5
 - /geolocation/lat_lowestreturn_a6
 - /geolocation/latitude_1gfit
 - /geolocation/lats_allmodes_a1
 - /geolocation/lats_allmodes_a2
 - /geolocation/lats_allmodes_a3
 - /geolocation/lats_allmodes_a4
 - /geolocation/lats_allmodes_a5
 - /geolocation/lats_allmodes_a6
 - /geolocation/lon_highestreturn_a1
 - /geolocation/lon_highestreturn_a2
 - /geolocation/lon_highestreturn_a3
 - /geolocation/lon_highestreturn_a4
 - /geolocation/lon_highestreturn_a5
 - /geolocation/lon_highestreturn_a6
 - /geolocation/lon_lowestmode_a1
 - /geolocation/lon_lowestmode_a2
 - /geolocation/lon_lowestmode_a3
 - /geolocation/lon_lowestmode_a4
 - /geolocation/lon_lowestmode_a5
 - /geolocation/lon_lowestmode_a6
 - /geolocation/lon_lowestreturn_a1
 - /geolocation/lon_lowestreturn_a2
 - /geolocation/lon_lowestreturn_a3
 - /geolocation/lon_lowestreturn_a4
 - /geolocation/lon_lowestreturn_a5
 - /geolocation/lon_lowestreturn_a6
 - /geolocation/longitude_1gfit
 - /geolocation/lons_allmodes_a1
 - /geolocation/lons_allmodes_a2
 - /geolocation/lons_allmodes_a3
 - /geolocation/lons_allmodes_a4
 - /geolocation/lons_allmodes_a5
 - /geolocation/lons_allmodes_a6
 - /geolocation/num_detectedmodes_a1
 - /geolocation/num_detectedmodes_a2
 - /geolocation/num_detectedmodes_a3
 - /geolocation/num_detectedmodes_a4
 - /geolocation/num_detectedmodes_a5
 - /geolocation/num_detectedmodes_a6
 - /geolocation/quality_flag_a1
 - /geolocation/quality_flag_a2
 - /geolocation/quality_flag_a3
 - /geolocation/quality_flag_a4
 - /geolocation/quality_flag_a5
 - /geolocation/quality_flag_a6
 - /geolocation/rh_a1
 - /geolocation/rh_a2
 - /geolocation/rh_a3
 - /geolocation/rh_a4
 - /geolocation/rh_a5
 - /geolocation/rh_a6
 - /geolocation/sensitivity_a1
 - /geolocation/sensitivity_a2
 - /geolocation/sensitivity_a3
 - /geolocation/sensitivity_a4
 - /geolocation/sensitivity_a5
 - /geolocation/sensitivity_a6
 - /geolocation/stale_return_flag
 - /land_cover_data/landsat_treecover  
 - /land_cover_data/landsat_water_persistence (Version 2 only)  
 - /land_cover_data/leaf_off_doy (Version 2 only)  
 - /land_cover_data/leaf_off_flag (Version 2 only)  
 - /land_cover_data/leaf_on_cycle (Version 2 only)  
 - /land_cover_data/leaf_on_doy (Version 2 only)  
 - /land_cover_data/modis_nonvegetated
 - /land_cover_data/modis_nonvegetated_sd
 - /land_cover_data/modis_treecover
 - /land_cover_data/modis_treecover_sd  
 - /land_cover_data/pft_class (Version 2 only)  
 - /land_cover_data/region_class (Version 2 only)  
 - /land_cover_data/urban_focal_window_size (Version 2 only)  
 - /land_cover_data/urban_proportion (Version 2 only)  
 - /lat_highestreturn
 - **/lat_lowestmode**
 - /latitude_bin0_error
 - /lon_highestreturn
 - **/lon_lowestmode**
 - /longitude_bin0_error
 - /master_frac
 - /master_int
 - /mean_sea_surface
 - **/num_detectedmodes**
 - **/quality_flag**
 - **/rh**
 - /rx_1gaussfit/ancillary/mpfit_max_func_evals
 - /rx_1gaussfit/ancillary/mpfit_maxiters
 - /rx_1gaussfit/ancillary/mpfit_tolerance
 - /rx_1gaussfit/ancillary/rx_constraint_gamplitude_lower
 - /rx_1gaussfit/ancillary/rx_constraint_gamplitude_upper
 - /rx_1gaussfit/ancillary/rx_constraint_gloc_lower
 - /rx_1gaussfit/ancillary/rx_constraint_gloc_upper
 - /rx_1gaussfit/ancillary/rx_constraint_gwidth_lower
 - /rx_1gaussfit/ancillary/rx_constraint_gwidth_upper
 - /rx_1gaussfit/ancillary/rx_estimate_bias
 - /rx_1gaussfit/ancillary/rx_mean_noise_level
 - /rx_1gaussfit/ancillary/rx_smoothwidth
 - /rx_1gaussfit/rx_gamplitude
 - /rx_1gaussfit/rx_gamplitude_error
 - /rx_1gaussfit/rx_gbias
 - /rx_1gaussfit/rx_gbias_error
 - /rx_1gaussfit/rx_gchisq
 - /rx_1gaussfit/rx_gflag
 - /rx_1gaussfit/rx_giters
 - /rx_1gaussfit/rx_gloc
 - /rx_1gaussfit/rx_gloc_error
 - /rx_1gaussfit/rx_gwidth
 - /rx_1gaussfit/rx_gwidth_error
 - /rx_assess/ancillary/rx_ampbounds_ll
 - /rx_assess/ancillary/rx_ampbounds_ul
 - /rx_assess/ancillary/rx_clipamp
 - /rx_assess/ancillary/rx_pulsethresh
 - /rx_assess/ancillary/rx_ringthresh
 - /rx_assess/ancillary/smoothing_width_locs
 - /rx_assess/mean
 - /rx_assess/mean_64kadjusted
 - /rx_assess/ocean_calibration_shot_flag
 - /rx_assess/quality_flag
 - /rx_assess/rx_assess_flag
 - /rx_assess/rx_clipbin0
 - /rx_assess/rx_clipbin_count
 - /rx_assess/rx_energy
 - /rx_assess/rx_maxamp
 - /rx_assess/rx_maxpeakloc
 - /rx_assess/sd_corrected
 - /rx_processing_a1/ancillary/amp_thresh
 - /rx_processing_a1/ancillary/ampval_limit2
 - /rx_processing_a1/ancillary/ampval_limit3
 - /rx_processing_a1/ancillary/botlocdist_limit1
 - /rx_processing_a1/ancillary/botlocdist_limit2
 - /rx_processing_a1/ancillary/botlocdist_limit3
 - /rx_processing_a1/ancillary/cumulative_energy_minimum
 - /rx_processing_a1/ancillary/cumulative_energy_thresh
 - /rx_processing_a1/ancillary/enable_select_mode
 - /rx_processing_a1/ancillary/energy_thresh
 - /rx_processing_a1/ancillary/preprocessor_threshold
 - /rx_processing_a1/ancillary/pulse_sep_thresh
 - /rx_processing_a1/ancillary/rx_back_threshold
 - /rx_processing_a1/ancillary/rx_front_threshold
 - /rx_processing_a1/ancillary/rx_max_mode_count
 - /rx_processing_a1/ancillary/rx_searchsize
 - /rx_processing_a1/ancillary/rx_sentinel_location
 - /rx_processing_a1/ancillary/rx_smoothing_width_locs
 - /rx_processing_a1/ancillary/rx_smoothing_width_zcross
 - /rx_processing_a1/ancillary/rx_subbin_resolution
 - /rx_processing_a1/ancillary/rx_use_fixed_thresholds
 - /rx_processing_a1/back_threshold
 - /rx_processing_a1/botloc
 - /rx_processing_a1/botloc_amp
 - /rx_processing_a1/energy_sm
 - /rx_processing_a1/front_threshold
 - /rx_processing_a1/lastmodeenergy
 - /rx_processing_a1/mean
 - /rx_processing_a1/mean_sm
 - /rx_processing_a1/min_detection_energy
 - /rx_processing_a1/min_detection_threshold
 - /rx_processing_a1/peak
 - /rx_processing_a1/pk_sm
 - /rx_processing_a1/rx_algrunflag
 - /rx_processing_a1/rx_cumulative
 - /rx_processing_a1/rx_iwaveamps
 - /rx_processing_a1/rx_modeamps
 - /rx_processing_a1/rx_modeenergytobotloc
 - /rx_processing_a1/rx_modelocalenergy
 - /rx_processing_a1/rx_modelocalenergyabovemean
 - /rx_processing_a1/rx_modelocalslope
 - /rx_processing_a1/rx_modelocs
 - /rx_processing_a1/rx_modewidths
 - /rx_processing_a1/rx_nummodes
 - /rx_processing_a1/sd_sm
 - /rx_processing_a1/search_end
 - /rx_processing_a1/search_start
 - /rx_processing_a1/selected_mode
 - /rx_processing_a1/selected_mode_flag
 - /rx_processing_a1/smoothwidth
 - /rx_processing_a1/smoothwidth_zcross
 - /rx_processing_a1/stddev
 - /rx_processing_a1/toploc
 - /rx_processing_a1/toploc_miss
 - /rx_processing_a1/zcross
 - /rx_processing_a1/zcross0
 - /rx_processing_a1/zcross_amp
 - /rx_processing_a1/zcross_localenergy
 - /rx_processing_a2/ancillary/amp_thresh
 - /rx_processing_a2/ancillary/ampval_limit2
 - /rx_processing_a2/ancillary/ampval_limit3
 - /rx_processing_a2/ancillary/botlocdist_limit1
 - /rx_processing_a2/ancillary/botlocdist_limit2
 - /rx_processing_a2/ancillary/botlocdist_limit3
 - /rx_processing_a2/ancillary/cumulative_energy_minimum
 - /rx_processing_a2/ancillary/cumulative_energy_thresh
 - /rx_processing_a2/ancillary/enable_select_mode
 - /rx_processing_a2/ancillary/energy_thresh
 - /rx_processing_a2/ancillary/preprocessor_threshold
 - /rx_processing_a2/ancillary/pulse_sep_thresh
 - /rx_processing_a2/ancillary/rx_back_threshold
 - /rx_processing_a2/ancillary/rx_front_threshold
 - /rx_processing_a2/ancillary/rx_max_mode_count
 - /rx_processing_a2/ancillary/rx_searchsize
 - /rx_processing_a2/ancillary/rx_sentinel_location
 - /rx_processing_a2/ancillary/rx_smoothing_width_locs
 - /rx_processing_a2/ancillary/rx_smoothing_width_zcross
 - /rx_processing_a2/ancillary/rx_subbin_resolution
 - /rx_processing_a2/ancillary/rx_use_fixed_thresholds
 - /rx_processing_a2/back_threshold
 - /rx_processing_a2/botloc
 - /rx_processing_a2/botloc_amp
 - /rx_processing_a2/energy_sm
 - /rx_processing_a2/front_threshold
 - /rx_processing_a2/lastmodeenergy
 - /rx_processing_a2/mean
 - /rx_processing_a2/mean_sm
 - /rx_processing_a2/min_detection_energy
 - /rx_processing_a2/min_detection_threshold
 - /rx_processing_a2/peak
 - /rx_processing_a2/pk_sm
 - /rx_processing_a2/rx_algrunflag
 - /rx_processing_a2/rx_cumulative
 - /rx_processing_a2/rx_iwaveamps
 - /rx_processing_a2/rx_modeamps
 - /rx_processing_a2/rx_modeenergytobotloc
 - /rx_processing_a2/rx_modelocalenergy
 - /rx_processing_a2/rx_modelocalenergyabovemean
 - /rx_processing_a2/rx_modelocalslope
 - /rx_processing_a2/rx_modelocs
 - /rx_processing_a2/rx_modewidths
 - /rx_processing_a2/rx_nummodes
 - /rx_processing_a2/sd_sm
 - /rx_processing_a2/search_end
 - /rx_processing_a2/search_start
 - /rx_processing_a2/selected_mode
 - /rx_processing_a2/selected_mode_flag
 - /rx_processing_a2/smoothwidth
 - /rx_processing_a2/smoothwidth_zcross
 - /rx_processing_a2/stddev
 - /rx_processing_a2/toploc
 - /rx_processing_a2/toploc_miss
 - /rx_processing_a2/zcross
 - /rx_processing_a2/zcross0
 - /rx_processing_a2/zcross_amp
 - /rx_processing_a2/zcross_localenergy
 - /rx_processing_a3/ancillary/amp_thresh
 - /rx_processing_a3/ancillary/ampval_limit2
 - /rx_processing_a3/ancillary/ampval_limit3
 - /rx_processing_a3/ancillary/botlocdist_limit1
 - /rx_processing_a3/ancillary/botlocdist_limit2
 - /rx_processing_a3/ancillary/botlocdist_limit3
 - /rx_processing_a3/ancillary/cumulative_energy_minimum
 - /rx_processing_a3/ancillary/cumulative_energy_thresh
 - /rx_processing_a3/ancillary/enable_select_mode
 - /rx_processing_a3/ancillary/energy_thresh
 - /rx_processing_a3/ancillary/preprocessor_threshold
 - /rx_processing_a3/ancillary/pulse_sep_thresh
 - /rx_processing_a3/ancillary/rx_back_threshold
 - /rx_processing_a3/ancillary/rx_front_threshold
 - /rx_processing_a3/ancillary/rx_max_mode_count
 - /rx_processing_a3/ancillary/rx_searchsize
 - /rx_processing_a3/ancillary/rx_sentinel_location
 - /rx_processing_a3/ancillary/rx_smoothing_width_locs
 - /rx_processing_a3/ancillary/rx_smoothing_width_zcross
 - /rx_processing_a3/ancillary/rx_subbin_resolution
 - /rx_processing_a3/ancillary/rx_use_fixed_thresholds
 - /rx_processing_a3/back_threshold
 - /rx_processing_a3/botloc
 - /rx_processing_a3/botloc_amp
 - /rx_processing_a3/energy_sm
 - /rx_processing_a3/front_threshold
 - /rx_processing_a3/lastmodeenergy
 - /rx_processing_a3/mean
 - /rx_processing_a3/mean_sm
 - /rx_processing_a3/min_detection_energy
 - /rx_processing_a3/min_detection_threshold
 - /rx_processing_a3/peak
 - /rx_processing_a3/pk_sm
 - /rx_processing_a3/rx_algrunflag
 - /rx_processing_a3/rx_cumulative
 - /rx_processing_a3/rx_iwaveamps
 - /rx_processing_a3/rx_modeamps
 - /rx_processing_a3/rx_modeenergytobotloc
 - /rx_processing_a3/rx_modelocalenergy
 - /rx_processing_a3/rx_modelocalenergyabovemean
 - /rx_processing_a3/rx_modelocalslope
 - /rx_processing_a3/rx_modelocs
 - /rx_processing_a3/rx_modewidths
 - /rx_processing_a3/rx_nummodes
 - /rx_processing_a3/sd_sm
 - /rx_processing_a3/search_end
 - /rx_processing_a3/search_start
 - /rx_processing_a3/selected_mode
 - /rx_processing_a3/selected_mode_flag
 - /rx_processing_a3/smoothwidth
 - /rx_processing_a3/smoothwidth_zcross
 - /rx_processing_a3/stddev
 - /rx_processing_a3/toploc
 - /rx_processing_a3/toploc_miss
 - /rx_processing_a3/zcross
 - /rx_processing_a3/zcross0
 - /rx_processing_a3/zcross_amp
 - /rx_processing_a3/zcross_localenergy
 - /rx_processing_a4/ancillary/amp_thresh
 - /rx_processing_a4/ancillary/ampval_limit2
 - /rx_processing_a4/ancillary/ampval_limit3
 - /rx_processing_a4/ancillary/botlocdist_limit1
 - /rx_processing_a4/ancillary/botlocdist_limit2
 - /rx_processing_a4/ancillary/botlocdist_limit3
 - /rx_processing_a4/ancillary/cumulative_energy_minimum
 - /rx_processing_a4/ancillary/cumulative_energy_thresh
 - /rx_processing_a4/ancillary/enable_select_mode
 - /rx_processing_a4/ancillary/energy_thresh
 - /rx_processing_a4/ancillary/preprocessor_threshold
 - /rx_processing_a4/ancillary/pulse_sep_thresh
 - /rx_processing_a4/ancillary/rx_back_threshold
 - /rx_processing_a4/ancillary/rx_front_threshold
 - /rx_processing_a4/ancillary/rx_max_mode_count
 - /rx_processing_a4/ancillary/rx_searchsize
 - /rx_processing_a4/ancillary/rx_sentinel_location
 - /rx_processing_a4/ancillary/rx_smoothing_width_locs
 - /rx_processing_a4/ancillary/rx_smoothing_width_zcross
 - /rx_processing_a4/ancillary/rx_subbin_resolution
 - /rx_processing_a4/ancillary/rx_use_fixed_thresholds
 - /rx_processing_a4/back_threshold
 - /rx_processing_a4/botloc
 - /rx_processing_a4/botloc_amp
 - /rx_processing_a4/energy_sm
 - /rx_processing_a4/front_threshold
 - /rx_processing_a4/lastmodeenergy
 - /rx_processing_a4/mean
 - /rx_processing_a4/mean_sm
 - /rx_processing_a4/min_detection_energy
 - /rx_processing_a4/min_detection_threshold
 - /rx_processing_a4/peak
 - /rx_processing_a4/pk_sm
 - /rx_processing_a4/rx_algrunflag
 - /rx_processing_a4/rx_cumulative
 - /rx_processing_a4/rx_iwaveamps
 - /rx_processing_a4/rx_modeamps
 - /rx_processing_a4/rx_modeenergytobotloc
 - /rx_processing_a4/rx_modelocalenergy
 - /rx_processing_a4/rx_modelocalenergyabovemean
 - /rx_processing_a4/rx_modelocalslope
 - /rx_processing_a4/rx_modelocs
 - /rx_processing_a4/rx_modewidths
 - /rx_processing_a4/rx_nummodes
 - /rx_processing_a4/sd_sm
 - /rx_processing_a4/search_end
 - /rx_processing_a4/search_start
 - /rx_processing_a4/selected_mode
 - /rx_processing_a4/selected_mode_flag
 - /rx_processing_a4/smoothwidth
 - /rx_processing_a4/smoothwidth_zcross
 - /rx_processing_a4/stddev
 - /rx_processing_a4/toploc
 - /rx_processing_a4/toploc_miss
 - /rx_processing_a4/zcross
 - /rx_processing_a4/zcross0
 - /rx_processing_a4/zcross_amp
 - /rx_processing_a4/zcross_localenergy
 - /rx_processing_a5/ancillary/amp_thresh
 - /rx_processing_a5/ancillary/ampval_limit2
 - /rx_processing_a5/ancillary/ampval_limit3
 - /rx_processing_a5/ancillary/botlocdist_limit1
 - /rx_processing_a5/ancillary/botlocdist_limit2
 - /rx_processing_a5/ancillary/botlocdist_limit3
 - /rx_processing_a5/ancillary/cumulative_energy_minimum
 - /rx_processing_a5/ancillary/cumulative_energy_thresh
 - /rx_processing_a5/ancillary/enable_select_mode
 - /rx_processing_a5/ancillary/energy_thresh
 - /rx_processing_a5/ancillary/preprocessor_threshold
 - /rx_processing_a5/ancillary/pulse_sep_thresh
 - /rx_processing_a5/ancillary/rx_back_threshold
 - /rx_processing_a5/ancillary/rx_front_threshold
 - /rx_processing_a5/ancillary/rx_max_mode_count
 - /rx_processing_a5/ancillary/rx_searchsize
 - /rx_processing_a5/ancillary/rx_sentinel_location
 - /rx_processing_a5/ancillary/rx_smoothing_width_locs
 - /rx_processing_a5/ancillary/rx_smoothing_width_zcross
 - /rx_processing_a5/ancillary/rx_subbin_resolution
 - /rx_processing_a5/ancillary/rx_use_fixed_thresholds
 - /rx_processing_a5/back_threshold
 - /rx_processing_a5/botloc
 - /rx_processing_a5/botloc_amp
 - /rx_processing_a5/energy_sm
 - /rx_processing_a5/front_threshold
 - /rx_processing_a5/lastmodeenergy
 - /rx_processing_a5/mean
 - /rx_processing_a5/mean_sm
 - /rx_processing_a5/min_detection_energy
 - /rx_processing_a5/min_detection_threshold
 - /rx_processing_a5/peak
 - /rx_processing_a5/pk_sm
 - /rx_processing_a5/rx_algrunflag
 - /rx_processing_a5/rx_cumulative
 - /rx_processing_a5/rx_iwaveamps
 - /rx_processing_a5/rx_modeamps
 - /rx_processing_a5/rx_modeenergytobotloc
 - /rx_processing_a5/rx_modelocalenergy
 - /rx_processing_a5/rx_modelocalenergyabovemean
 - /rx_processing_a5/rx_modelocalslope
 - /rx_processing_a5/rx_modelocs
 - /rx_processing_a5/rx_modewidths
 - /rx_processing_a5/rx_nummodes
 - /rx_processing_a5/sd_sm
 - /rx_processing_a5/search_end
 - /rx_processing_a5/search_start
 - /rx_processing_a5/selected_mode
 - /rx_processing_a5/selected_mode_flag
 - /rx_processing_a5/smoothwidth
 - /rx_processing_a5/smoothwidth_zcross
 - /rx_processing_a5/stddev
 - /rx_processing_a5/toploc
 - /rx_processing_a5/toploc_miss
 - /rx_processing_a5/zcross
 - /rx_processing_a5/zcross0
 - /rx_processing_a5/zcross_amp
 - /rx_processing_a5/zcross_localenergy
 - /rx_processing_a6/ancillary/amp_thresh
 - /rx_processing_a6/ancillary/ampval_limit2
 - /rx_processing_a6/ancillary/ampval_limit3
 - /rx_processing_a6/ancillary/botlocdist_limit1
 - /rx_processing_a6/ancillary/botlocdist_limit2
 - /rx_processing_a6/ancillary/botlocdist_limit3
 - /rx_processing_a6/ancillary/cumulative_energy_minimum
 - /rx_processing_a6/ancillary/cumulative_energy_thresh
 - /rx_processing_a6/ancillary/enable_select_mode
 - /rx_processing_a6/ancillary/energy_thresh
 - /rx_processing_a6/ancillary/preprocessor_threshold
 - /rx_processing_a6/ancillary/pulse_sep_thresh
 - /rx_processing_a6/ancillary/rx_back_threshold
 - /rx_processing_a6/ancillary/rx_front_threshold
 - /rx_processing_a6/ancillary/rx_max_mode_count
 - /rx_processing_a6/ancillary/rx_searchsize
 - /rx_processing_a6/ancillary/rx_sentinel_location
 - /rx_processing_a6/ancillary/rx_smoothing_width_locs
 - /rx_processing_a6/ancillary/rx_smoothing_width_zcross
 - /rx_processing_a6/ancillary/rx_subbin_resolution
 - /rx_processing_a6/ancillary/rx_use_fixed_thresholds
 - /rx_processing_a6/back_threshold
 - /rx_processing_a6/botloc
 - /rx_processing_a6/botloc_amp
 - /rx_processing_a6/energy_sm
 - /rx_processing_a6/front_threshold
 - /rx_processing_a6/lastmodeenergy
 - /rx_processing_a6/mean
 - /rx_processing_a6/mean_sm
 - /rx_processing_a6/min_detection_energy
 - /rx_processing_a6/min_detection_threshold
 - /rx_processing_a6/peak
 - /rx_processing_a6/pk_sm
 - /rx_processing_a6/rx_algrunflag
 - /rx_processing_a6/rx_cumulative
 - /rx_processing_a6/rx_iwaveamps
 - /rx_processing_a6/rx_modeamps
 - /rx_processing_a6/rx_modeenergytobotloc
 - /rx_processing_a6/rx_modelocalenergy
 - /rx_processing_a6/rx_modelocalenergyabovemean
 - /rx_processing_a6/rx_modelocalslope
 - /rx_processing_a6/rx_modelocs
 - /rx_processing_a6/rx_modewidths
 - /rx_processing_a6/rx_nummodes
 - /rx_processing_a6/sd_sm
 - /rx_processing_a6/search_end
 - /rx_processing_a6/search_start
 - /rx_processing_a6/selected_mode
 - /rx_processing_a6/selected_mode_flag
 - /rx_processing_a6/smoothwidth
 - /rx_processing_a6/smoothwidth_zcross
 - /rx_processing_a6/stddev
 - /rx_processing_a6/toploc
 - /rx_processing_a6/toploc_miss
 - /rx_processing_a6/zcross
 - /rx_processing_a6/zcross0
 - /rx_processing_a6/zcross_amp
 - /rx_processing_a6/zcross_localenergy
 - **/selected_algorithm**
 - /selected_mode  
 - /selected_mode_flag  (Version 2 only)  
 - **/sensitivity**
 - **/shot_number**
 - /solar_azimuth
 - **/solar_elevation**
 - **/surface_flag**

#### GEDI02_B  
 - /algorithmrun_flag
 - /ancillary/dz
 - /ancillary/l2a_alg_count
 - /ancillary/maxheight_cuttoff
 - /ancillary/rg_eg_constraint_center_buffer
 - /ancillary/rg_eg_mpfit_max_func_evals
 - /ancillary/rg_eg_mpfit_maxiters
 - /ancillary/rg_eg_mpfit_tolerance
 - /ancillary/signal_search_buff
 - /ancillary/tx_noise_stddev_multiplier
 - **/beam**
 - **/channel**
 - **/cover**
 - **/cover_z**
 - **/fhd_normal**
 - **/geolocation/degrade_flag**
 - **/geolocation/delta_time**
 - **/geolocation/digital_elevation_model**
 - /geolocation/elev_highestreturn
 - **/geolocation/elev_lowestmode**
 - /geolocation/elevation_bin0
 - /geolocation/elevation_bin0_error
 - /geolocation/elevation_lastbin
 - /geolocation/elevation_lastbin_error
 - /geolocation/height_bin0
 - /geolocation/height_lastbin
 - /geolocation/lat_highestreturn
 - **/geolocation/lat_lowestmode**
 - /geolocation/latitude_bin0
 - /geolocation/latitude_bin0_error
 - /geolocation/latitude_lastbin
 - /geolocation/latitude_lastbin_error
 - /geolocation/local_beam_azimuth
 - /geolocation/local_beam_elevation
 - /geolocation/lon_highestreturn
 - **/geolocation/lon_lowestmode**
 - /geolocation/longitude_bin0
 - /geolocation/longitude_bin0_error
 - /geolocation/longitude_lastbin
 - /geolocation/longitude_lastbin_error
 - /geolocation/shot_number
 - /geolocation/solar_azimuth
 - **/geolocation/solar_elevation**
 - **/l2a_quality_flag**
 - **/l2b_quality_flag**
 - /land_cover_data/landsat_treecover
 - /land_cover_data/landsat_water_persistence (Version 2 only)  
 - /land_cover_data/leaf_off_doy (Version 2 only)  
 - /land_cover_data/leaf_off_flag (Version 2 only)  
 - /land_cover_data/leaf_on_cycle (Version 2 only)  
 - /land_cover_data/leaf_on_doy (Version 2 only)  
 - /land_cover_data/modis_nonvegetated
 - /land_cover_data/modis_nonvegetated_sd
 - /land_cover_data/modis_treecover
 - /land_cover_data/modis_treecover_sd  
 - /land_cover_data/pft_class (Version 2 only)  
 - /land_cover_data/region_class (Version 2 only)  
 - /land_cover_data/urban_focal_window_size (Version 2 only)  
 - /land_cover_data/urban_proportion (Version 2 only)  
 - /master_frac
 - /master_int
 - /num_detectedmodes
 - /omega
 - **/pai**
 - **/pai_z**
 - **/pavd_z**
 - /pgap_theta
 - /pgap_theta_error
 - /pgap_theta_z
 - /rg
 - **/rh100**
 - **/rhog**
 - /rhog_error
 - **/rhov**
 - /rhov_error
 - /rossg
 - /rv
 - /rx_processing/algorithmrun_flag_a1
 - /rx_processing/algorithmrun_flag_a2
 - /rx_processing/algorithmrun_flag_a3
 - /rx_processing/algorithmrun_flag_a4
 - /rx_processing/algorithmrun_flag_a5
 - /rx_processing/algorithmrun_flag_a6
 - /rx_processing/pgap_theta_a1
 - /rx_processing/pgap_theta_a2
 - /rx_processing/pgap_theta_a3
 - /rx_processing/pgap_theta_a4
 - /rx_processing/pgap_theta_a5
 - /rx_processing/pgap_theta_a6
 - /rx_processing/pgap_theta_error_a1
 - /rx_processing/pgap_theta_error_a2
 - /rx_processing/pgap_theta_error_a3
 - /rx_processing/pgap_theta_error_a4
 - /rx_processing/pgap_theta_error_a5
 - /rx_processing/pgap_theta_error_a6
 - /rx_processing/rg_a1
 - /rx_processing/rg_a2
 - /rx_processing/rg_a3
 - /rx_processing/rg_a4
 - /rx_processing/rg_a5
 - /rx_processing/rg_a6
 - /rx_processing/rg_eg_amplitude_a1
 - /rx_processing/rg_eg_amplitude_a2
 - /rx_processing/rg_eg_amplitude_a3
 - /rx_processing/rg_eg_amplitude_a4
 - /rx_processing/rg_eg_amplitude_a5
 - /rx_processing/rg_eg_amplitude_a6
 - /rx_processing/rg_eg_amplitude_error_a1
 - /rx_processing/rg_eg_amplitude_error_a2
 - /rx_processing/rg_eg_amplitude_error_a3
 - /rx_processing/rg_eg_amplitude_error_a4
 - /rx_processing/rg_eg_amplitude_error_a5
 - /rx_processing/rg_eg_amplitude_error_a6
 - /rx_processing/rg_eg_center_a1
 - /rx_processing/rg_eg_center_a2
 - /rx_processing/rg_eg_center_a3
 - /rx_processing/rg_eg_center_a4
 - /rx_processing/rg_eg_center_a5
 - /rx_processing/rg_eg_center_a6
 - /rx_processing/rg_eg_center_error_a1
 - /rx_processing/rg_eg_center_error_a2
 - /rx_processing/rg_eg_center_error_a3
 - /rx_processing/rg_eg_center_error_a4
 - /rx_processing/rg_eg_center_error_a5
 - /rx_processing/rg_eg_center_error_a6
 - /rx_processing/rg_eg_chisq_a1
 - /rx_processing/rg_eg_chisq_a2
 - /rx_processing/rg_eg_chisq_a3
 - /rx_processing/rg_eg_chisq_a4
 - /rx_processing/rg_eg_chisq_a5
 - /rx_processing/rg_eg_chisq_a6
 - /rx_processing/rg_eg_flag_a1
 - /rx_processing/rg_eg_flag_a2
 - /rx_processing/rg_eg_flag_a3
 - /rx_processing/rg_eg_flag_a4
 - /rx_processing/rg_eg_flag_a5
 - /rx_processing/rg_eg_flag_a6
 - /rx_processing/rg_eg_gamma_a1
 - /rx_processing/rg_eg_gamma_a2
 - /rx_processing/rg_eg_gamma_a3
 - /rx_processing/rg_eg_gamma_a4
 - /rx_processing/rg_eg_gamma_a5
 - /rx_processing/rg_eg_gamma_a6
 - /rx_processing/rg_eg_gamma_error_a1
 - /rx_processing/rg_eg_gamma_error_a2
 - /rx_processing/rg_eg_gamma_error_a3
 - /rx_processing/rg_eg_gamma_error_a4
 - /rx_processing/rg_eg_gamma_error_a5
 - /rx_processing/rg_eg_gamma_error_a6
 - /rx_processing/rg_eg_niter_a1
 - /rx_processing/rg_eg_niter_a2
 - /rx_processing/rg_eg_niter_a3
 - /rx_processing/rg_eg_niter_a4
 - /rx_processing/rg_eg_niter_a5
 - /rx_processing/rg_eg_niter_a6
 - /rx_processing/rg_eg_sigma_a1
 - /rx_processing/rg_eg_sigma_a2
 - /rx_processing/rg_eg_sigma_a3
 - /rx_processing/rg_eg_sigma_a4
 - /rx_processing/rg_eg_sigma_a5
 - /rx_processing/rg_eg_sigma_a6
 - /rx_processing/rg_eg_sigma_error_a1
 - /rx_processing/rg_eg_sigma_error_a2
 - /rx_processing/rg_eg_sigma_error_a3
 - /rx_processing/rg_eg_sigma_error_a4
 - /rx_processing/rg_eg_sigma_error_a5
 - /rx_processing/rg_eg_sigma_error_a6
 - /rx_processing/rg_error_a1
 - /rx_processing/rg_error_a2
 - /rx_processing/rg_error_a3
 - /rx_processing/rg_error_a4
 - /rx_processing/rg_error_a5
 - /rx_processing/rg_error_a6
 - /rx_processing/rv_a1
 - /rx_processing/rv_a2
 - /rx_processing/rv_a3
 - /rx_processing/rv_a4
 - /rx_processing/rv_a5
 - /rx_processing/rv_a6
 - /rx_processing/rx_energy_a1
 - /rx_processing/rx_energy_a2
 - /rx_processing/rx_energy_a3
 - /rx_processing/rx_energy_a4
 - /rx_processing/rx_energy_a5
 - /rx_processing/rx_energy_a6
 - /rx_processing/shot_number
 - /rx_range_highestreturn
 - /rx_sample_count
 - /rx_sample_start_index
 - /selected_l2a_algorithm  
 - /selected_mode (Version 2 only)  
 - /selected_mode_flag (Version 2 only)  
 - /selected_rg_algorithm
 - **/sensitivity**
 - **/shot_number**
 - **/stale_return_flag**
 - **/surface_flag**

---
# Contact Information:
#### Author: LP DAAC¹   
**Contact:** LPDAAC@usgs.gov  
**Voice:** +1-866-573-3222  
**Organization:** Land Processes Distributed Active Archive Center (LP DAAC)  
**Website:** https://lpdaac.usgs.gov/  
**Date last modified:** 11-30-2023  

¹KBR, Inc., contractor to the U.S. Geological Survey, Earth Resources Observation and Science (EROS) Center,  
 Sioux Falls, South Dakota, USA. Work performed under USGS contract G15PD00467 for LP DAAC².  
²LP DAAC Work performed under NASA contract NNG14HH33I.
