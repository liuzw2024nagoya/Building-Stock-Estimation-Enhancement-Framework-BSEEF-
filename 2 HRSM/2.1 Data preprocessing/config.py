# Configuration file with all configurable variables (files and their absolute path, editable)

workspace = "D:/sample_workspace.gdb"
scratch_workspace = "D:/sample_scratch_workspace.gdb"

# The created fishnet layer based on the current cluster info and purpose label (e.g. "fishnet, Suburban, Training")
original_fishnet_layer = "Fishnet_sample"

# NTL raster layer
raster1 = "Sample_NTL"

# Reference building stock raster layer
raster2 = "Sample_WSF3D_V02_BuildingFloorArea_all_64b"

# Intermediate output: fishnet with extracted raster values/edge detection filter calculation
output_layer_1 = "Fishnet_extract_NTL_Floor"
output_layer_2 = "Fishnet_kernel_filter"

# User can specify the path and name of the exported CSV file here
csv_output_path = "D:/Sample_fishnet_Suburban_Training.csv"