import arcpy
import config  # Import the configuration module

# This function processes GIS data to extract cross-sections from raster and feature class inputs.
def BatchGeneration(workspace, scratch_workspace, input_raster, feature_class, output_gdb, toolbox_path):
    # Set environment settings
    arcpy.env.workspace = workspace
    arcpy.env.scratchWorkspace = scratch_workspace
    arcpy.env.overwriteOutput = True

    try:
        # Import necessary toolbox for data management tools
        arcpy.ImportToolbox(toolbox_path)

        # Load the input raster
        raster = arcpy.Raster(input_raster)

        # Use a SearchCursor to iterate over each feature in the feature class
        with arcpy.da.SearchCursor(feature_class, ["SHAPE@", "NLC_ID"]) as cursor:
            for row in cursor:
                geometry, NLC_ID = row
                name = f"{feature_class.split('/')[-1]}_{NLC_ID}"

                # Create a temporary in-memory feature class for the current feature
                temp_feature_class = "in_memory/temp_feature"
                arcpy.CopyFeatures_management(geometry, temp_feature_class)

                # Set the path for the output feature class
                copied_features = f"{output_gdb}/{name}"

                # Copy the temporary feature class to the desired location
                arcpy.CopyFeatures_management(temp_feature_class, copied_features)

                # Clean up the in-memory feature class
                arcpy.Delete_management(temp_feature_class)

                # Extract by Mask
                extract_by_mask = f"{output_gdb}/Extract_{name}"
                extract_result = arcpy.sa.ExtractByMask(in_raster=raster, in_mask_data=copied_features)
                extract_result.save(extract_by_mask)

                # Raster to Polygon
                polygon_output = f"{output_gdb}/Poly_{name}"
                arcpy.conversion.RasterToPolygon(in_raster=extract_by_mask, out_polygon_features=polygon_output,
                                                 simplify="NO_SIMPLIFY", raster_field="Value")

                # Summary Statistics
                summary_output = f"{output_gdb}/Summary_{name}"
                arcpy.analysis.Statistics(in_table=polygon_output, out_table=summary_output,
                                          statistics_fields=[["GRIDCODE", "MAX"]])

                # Join Field
                joined_output = arcpy.management.JoinField(in_data=polygon_output, in_field="GRIDCODE",
                                                           join_table=summary_output, join_field="MAX_GRIDCODE")

                # Select Layer By Attribute
                selected_output, _ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=joined_output,
                                                                             selection_type="NEW_SELECTION",
                                                                             where_clause="MAX_GRIDCODE IS NOT NULL")

                # Polygon to Line
                line_output = f"{output_gdb}/Perimeter_{name}"
                arcpy.management.PolygonToLine(in_features=copied_features, out_feature_class=line_output)

                # Generate Points Along Lines
                points_output = f"{output_gdb}/BoundaryPoints_{name}"
                arcpy.management.GeneratePointsAlongLines(Input_Features=line_output,
                                                          Output_Feature_Class=points_output,
                                                          Point_Placement="DISTANCE", Distance="100 Meters")

                # Add Field: PseudoHeight
                pseudo_height_field = arcpy.management.AddField(in_table=points_output, field_name="PseudoHeight",
                                                                field_type="LONG")

                # Calculate Field: PseudoHeight=1
                arcpy.management.CalculateField(in_table=pseudo_height_field, field="PseudoHeight", expression="1",
                                                expression_type="PYTHON3")

                # Construct Sight Lines
                sight_lines_output = f"{output_gdb}/SightLines_{name}"
                arcpy.ddd.ConstructSightLines(in_observer_points=pseudo_height_field,
                                              in_target_features=pseudo_height_field,
                                              out_line_feature_class=sight_lines_output,
                                              observer_height_field="PseudoHeight", target_height_field="PseudoHeight")

                # Copy Features (2)
                max_pixel_polygon_output = f"{output_gdb}/MaxPoly_{name}"
                arcpy.management.CopyFeatures(in_features=selected_output, out_feature_class=max_pixel_polygon_output)

                # Select Layer By Location
                intersect_output, _, _ = arcpy.management.SelectLayerByLocation(in_layer=[sight_lines_output],
                                                                                overlap_type="INTERSECT",
                                                                                select_features=max_pixel_polygon_output)

                # Copy Features (3)
                cross_section_output = f"{output_gdb}/CrossSection_{name}"
                arcpy.management.CopyFeatures(in_features=intersect_output, out_feature_class=cross_section_output)

                # Add Field: Bearing
                bearing_field = arcpy.management.AddField(in_table=cross_section_output, field_name="Bearing",
                                                          field_type="DOUBLE")

                # Calculate Geometry Attributes: Line bearing
                calculated_bearing = arcpy.management.CalculateGeometryAttributes(in_features=bearing_field,
                                                                                  geometry_property=[
                                                                                      ["Bearing", "LINE_BEARING"]])

                # Add Field: BearingRoundup
                bearing_roundup_field = arcpy.management.AddField(in_table=calculated_bearing,
                                                                  field_name="BearingRoundup", field_type="LONG")

                # Calculate Field: BearingRoundup
                arcpy.management.CalculateField(in_table=bearing_roundup_field, field="BearingRoundup",
                                                expression="Roundup(!Bearing!)", expression_type="PYTHON3", code_block="""def Roundup(value):
    return int((value + 4.5) // 5 * 5)""")

                # Summary Statistics: Maximum length
                summary_length_output = f"{output_gdb}/LengthSummary_{name}"
                arcpy.analysis.Statistics(in_table=bearing_roundup_field, out_table=summary_length_output,
                                          statistics_fields=[["Shape_Length", "MAX"], ["Shape_Length", "MIN"]])

                # Join Field (2)
                joined_length_output = arcpy.management.JoinField(in_data=bearing_roundup_field,
                                                                  in_field="Shape_Length",
                                                                  join_table=summary_length_output,
                                                                  join_field="MAX_Shape_Length")

                # Select Layer By Attribute
                filtered_output, _ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=joined_length_output,
                                                                             selection_type="NEW_SELECTION",
                                                                             where_clause="BearingRoundup = 90 OR BearingRoundup = 180 OR MAX_Shape_Length IS NOT NULL")

                # Copy Features (4)
                selected_cross_section_output = f"{output_gdb}/SelectedCrossSection_{name}"
                arcpy.management.CopyFeatures(in_features=filtered_output,
                                              out_feature_class=selected_cross_section_output)

                # Sort: Descending length
                sorted_output = f"{output_gdb}/Sorted_{name}"
                arcpy.management.Sort(in_dataset=selected_cross_section_output, out_dataset=sorted_output,
                                      sort_field=[["Shape_Length", "DESCENDING"]])

                # Delete Identical
                deduplicated_output = arcpy.management.DeleteIdentical(in_dataset=sorted_output,
                                                                       fields=["BearingRoundup"])

                # Add Field: CrosSecID
                cross_sec_id_field = arcpy.management.AddField(in_table=deduplicated_output, field_name="CrosSecID",
                                                               field_type="LONG", field_alias="CrossSectionID")

                # Calculate Field: CrosSecID
                arcpy.management.CalculateField(in_table=cross_sec_id_field, field="CrosSecID",
                                                expression=f"int({NLC_ID}) * 10000 + !OBJECTID!",
                                                expression_type="PYTHON3")

    except Exception as e:
        arcpy.AddError(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    BatchGeneration(
        config.workspace,
        config.scratch_workspace,
        config.input_raster,
        config.feature_class,
        config.output_gdb,
        config.toolbox_path
    )

