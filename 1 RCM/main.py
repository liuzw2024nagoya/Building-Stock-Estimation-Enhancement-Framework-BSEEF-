import arcpy
import CrossSection_BatchGeneration
import CrossSection_BatchExtractRaster
import config
import export
import CrossSection_curvefitting
import average_curve_parameters
import clustering
import cluster_remaining

# Merges all feature classes in the input geodatabase into a single feature class.
def merge_feature_classes(input_gdb, output_gdb, output_feature_class_name):
    """
    Parameters:
    input_gdb (str): Path to the input geodatabase containing individual feature classes.
    output_gdb (str): Path to the output geodatabase where the merged feature class will be stored.
    output_feature_class_name (str): Name of the merged feature class.

    Returns:
    str: Path to the merged feature class.
    """
    arcpy.env.workspace = input_gdb
    feature_classes = arcpy.ListFeatureClasses()
    output_feature_class = f"{output_gdb}/{output_feature_class_name}"

    arcpy.Merge_management(inputs=feature_classes, output=output_feature_class)
    return output_feature_class


if __name__ == '__main__':
    # Run CrossSection_BatchGeneration.py
    CrossSection_BatchGeneration.BatchGeneration(
        config.workspace,
        config.scratch_workspace,
        config.input_raster,
        config.feature_class,
        config.output_gdb,
        config.toolbox_path
    )

    # Merge feature classes from the output of CrossSection_BatchGeneration.py
    merged_feature_class = merge_feature_classes(
        input_gdb=config.merge_input_gdb,
        output_gdb=config.merge_output_gdb,
        output_feature_class_name=config.merge_output_feature_class_name
    )

    # Update the configuration for CrossSection_BatchExtractRaster.py
    config.input_feature_class_merged = merged_feature_class

    # Run CrossSection_BatchExtractRaster.py
    CrossSection_BatchExtractRaster.BatchExtractRaster(
        input_feature_class=config.input_feature_class_merged,
        group_by_fields=config.group_by_fields,
        raster_ntl=config.raster_ntl,
        raster_building_fa=config.raster_building_fa,
        workspace=config.workspace_script2
    )

    # Run export.py
    export.export_to_csv(
        workspace=config.csv_workspace,
        output_folder=config.csv_output_folder,
        desired_fields=config.csv_desired_fields
    )

    # Run CrossSection_curvefitting.py
    CrossSection_curvefitting.curve_fitting(
        csv_folder=config.csv_output_folder,
        fit_results_folder=config.fit_results_folder,
        fit_results_csv=config.fit_results_csv
    )

    # Run average_curve_parameters.py
    average_curve_parameters.process_and_save_csv(
        input_file_path=config.input_fit_results_csv,
        output_file_path=config.output_grouped_csv,
        output_file_path_skipna=config.output_grouped_skipna_csv
    )

    # Run clustering.py
    clustering.cluster_polygons(
        input_csv=config.input_grouped_skipna_csv,
        output_csv=config.output_clustered_csv
    )

    # Run cluster_remaining.py
    cluster_remaining.classify_remaining_polygons(
        polygon_layer=config.polygon_layer,
        cluster_field=config.cluster_field,
        temp_layer=config.temp_layer
    )