import arcpy
import datetime
import config  # Import the configuration module

# Processes the feature class by splitting it based on a unique ID and extracting values from rasters to points.
def BatchExtractRaster(input_feature_class, group_by_fields, raster_ntl, raster_building_fa, workspace):
    # Set workspace and other environment settings
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    # Split the feature class based on a unique ID (e.g., "CrosSecID")
    unique_ids = [row[0] for row in arcpy.da.SearchCursor(input_feature_class, ["CrosSecID"])]
    start_time_overall = datetime.datetime.now()
    Iterations_Left = len(unique_ids)
    for unique_id in set(unique_ids):
        start_time_iteration = datetime.datetime.now()
        print("Unique ID:", unique_id)

        output_feature_name = f"SelectedCrossSection_SAMPLENAME_{unique_id}"
        where_clause = f"CrosSecID = {unique_id}"

        arcpy.FeatureClassToFeatureClass_conversion(input_feature_class, arcpy.env.workspace, output_feature_name,
                                                    where_clause)

        # Generate Points Along Lines
        output_points_class = f"SelectedCrossSectionPoints_SAMPLENAME_{unique_id}"
        if not arcpy.Exists(output_points_class):
            arcpy.management.GeneratePointsAlongLines(Input_Features=output_feature_name,
                                                      Output_Feature_Class=output_points_class,
                                                      Point_Placement="DISTANCE", Distance="100 Meters")

        # Extract NTL Values to Points
        SelectedCrossSection_Points_NTL_Extract_JPN_NLCs_3s_Name_ = f"{workspace}/SelectedCrossSectionPointsNTLExt_SAMPLENAME___0000{unique_id}"
        if not arcpy.Exists(SelectedCrossSection_Points_NTL_Extract_JPN_NLCs_3s_Name_):
            arcpy.sa.ExtractValuesToPoints(in_point_features=output_points_class,
                                           in_raster=raster_ntl,
                                           out_point_features=SelectedCrossSection_Points_NTL_Extract_JPN_NLCs_3s_Name_,
                                           interpolate_values="NONE", add_attributes="VALUE_ONLY")

        # Extract BuildingFA Values to Points
        SelectedCrossSection_Points_BuildingFA_Extract_JPN_NLCs_3s_Name_ = f"{workspace}/SelectedCrossSectionPointsBuildingFAExt_SAMPLENAME___0000{unique_id}"
        if not arcpy.Exists(SelectedCrossSection_Points_BuildingFA_Extract_JPN_NLCs_3s_Name_):
            arcpy.sa.ExtractValuesToPoints(in_point_features=output_points_class,
                                           in_raster=raster_building_fa,
                                           out_point_features=SelectedCrossSection_Points_BuildingFA_Extract_JPN_NLCs_3s_Name_,
                                           interpolate_values="NONE", add_attributes="VALUE_ONLY")

        # Delete the intermediate datasets
        arcpy.Delete_management(output_points_class)
        arcpy.Delete_management(output_feature_name)

        # Print Iteration Time
        end_time_iteration = datetime.datetime.now()
        iteration_duration = end_time_iteration - start_time_iteration
        overall_duration = end_time_iteration - start_time_overall
        Iterations_Left = Iterations_Left - 1
        print(
            f"Iteration Time: {iteration_duration}, Overall Time: {overall_duration}, Iterations Left: {Iterations_Left}")
        print("***************************")


if __name__ == '__main__':
    BatchExtractRaster(
        input_feature_class=config.input_feature_class_merged,
        group_by_fields=config.group_by_fields,
        raster_ntl=config.raster_ntl,
        raster_building_fa=config.raster_building_fa,
        workspace=config.workspace_script2
    )

