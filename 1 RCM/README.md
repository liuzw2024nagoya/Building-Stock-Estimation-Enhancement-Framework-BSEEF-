
# BSEEF-RCM Geospatial Data Processing and Analysing Scripts

This repository aims to process geospatial data, generate and analyze cross-sectional curves of polygons, and finally classify these polygons through clustering. The project is divided into multiple scripts, each performing a specific task. All configurable variables are defined in the `config.py` file.

The scripts in this repository only show a general script structure, the actual applied structure can be modified according to actual needs.
## Directory Structure

```
project_root/
│
├── config.py
├── main.py
├── CrossSection_BatchGeneration.py
├── CrossSection_BatchExtractRaster.py
├── export.py
├── CrossSection_curvefitting.py
├── average_curve_parameters.py
├── clustering.py
├── cluster_remaining.py
├── requirements.txt
└── README.md
```

- `config.py`: Contains all configurable variables such as file paths and parameters.
- `main.py`: The main script that sequentially calls other scripts to complete the entire processing workflow.
- `CrossSection_BatchGeneration.py`: Generates cross-sections of polygons.
- `CrossSection_BatchExtractRaster.py`: Extracts cross-sectional data from raster data.
- `export.py`: Exports the extracted data to CSV files.
- `CrossSection_curvefitting.py`: Fits curves to the extracted cross-sectional data.
- `average_curve_parameters.py`: Calculates the average curve parameters for each polygon.
- `clustering.py`: Performs clustering analysis on the polygons.
- `cluster_remaining.py`: Classifies polygons that were not clustered.
- `requirements.txt`: List of required Python packages.
- `README.md`: This README file.

## Installation
Please note that `arcpy` is a proprietary library provided by Esri and it is typically included with ArcGIS software installations. It may not be available through common package managers like pip and might require a valid ArcGIS license to use. 

1. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

2. For `arcpy`, make sure you have ArcGIS installed and properly configured on your system. Consult Esri's documentation for instructions on how to set up `arcpy`.

## Usage Steps

### 1. Configuration File `config.py`

Before starting, modify the variables in `config.py` as needed. Below is the default content of the configuration file:

```python
# Configuration file with all configurable variables (files and their absolute path, editable)
import os

# Define paths and parameters for CrossSection_BatchGeneration.py
workspace = r"D:/sample_workspace.gdb"
scratch_workspace = r"D:/sample_scratch_workspace.gdb"
input_raster = r"D:/Sample_NTL"
feature_class = "sample_polygons"
output_gdb = r"D:/sample_output01.gdb"
toolbox_path = r"c:/program files/arcgis/pro/Resources/ArcToolbox/toolboxes/Data Management Tools.tbx"

# Parameters for merging feature classes
merge_input_gdb = r"D:/sample_output01.gdb"
merge_output_gdb = r"D:/sample_output02.gdb"
merge_output_feature_class_name = "merged_SelectedCrossSectionSort_sample"

# Define paths and parameters for CrossSection_BatchExtractRaster.py
input_feature_class_merged = r"D:/sample_output02.gdb/merged_SelectedCrossSectionSort_sample"
group_by_fields = [["CrosSecID", ""]]
raster_ntl = r"D:/Sample_NTL"
raster_building_fa = r"D:/Sample_WSF3D_V02_BuildingFloorArea_all_64b"
workspace_script2 = r"D:/sample_output03.gdb"

# Define paths and parameters for export.py
csv_workspace = r"D:/sample_output03.gdb"
csv_output_folder = r"D:/Cross_sections/batch_CSV"
csv_desired_fields = ["OBJECTID", "RASTERVALU"]

# Define paths and parameters for CrossSection_curvefitting.py
fit_results_folder = r"D:/Cross_sections/batch_CSV"
fit_results_csv = os.path.join(fit_results_folder, "fit_results.csv")

# Define paths and parameters for average_curve_parameters.py
input_fit_results_csv = fit_results_csv
output_grouped_csv = os.path.join(fit_results_folder, "grouped_fit_results.csv")
output_grouped_skipna_csv = os.path.join(fit_results_folder, "grouped_fit_results_skipna.csv")

# Define paths and parameters for clustering.py
input_grouped_skipna_csv = output_grouped_skipna_csv
output_clustered_csv = os.path.join(fit_results_folder, "clustered_grouped_fit_results_skipna.csv")

# Define paths and parameters for cluster_remaining.py (classification of remaining polygons)
polygon_layer = r"D:/sample_scratch_workspace.gdb/sample_polygons_clustered"
cluster_field = "Cluster"
temp_layer = r"D:/sample_scratch_workspace.gdb/temp_layer"
```

### 2. Main Script `main.py`

`main.py` is the main script that sequentially calls other scripts to complete the entire processing workflow.

## Running the Workflow

1. **Configure `config.py`**: Modify the variables in the configuration file to suit your data and paths.
2. **Run `main.py`**: Execute the main script, which will sequentially call all sub-scripts to complete the entire processing workflow.
3. **Check Output**: All output results will be saved in the paths specified in `config.py`.

By following these steps, you can complete the entire workflow from data generation, extraction, export, curve fitting, clustering, to classification.

## License

This repository is developed for the article "Adaptive Nighttime Light-Based Building Stock Assessment Framework for Future Environmentally Sustainable Management".
