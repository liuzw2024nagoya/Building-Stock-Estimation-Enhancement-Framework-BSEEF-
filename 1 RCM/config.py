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