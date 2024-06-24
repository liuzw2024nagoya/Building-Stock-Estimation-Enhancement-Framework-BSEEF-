import arcpy
from arcpy.sa import ZonalStatisticsAsTable
from config import workspace, scratch_workspace, original_fishnet_layer, raster1, raster2, output_layer_1

# Copy input layer to output layer
def copy_features(input_layer, output_layer):
    arcpy.CopyFeatures_management(input_layer, output_layer)
    print(f"Copied {input_layer} to {output_layer}")

# Check if the field exists in the dataset
def field_exists(dataset, field_name):
    return field_name in [f.name for f in arcpy.ListFields(dataset)]

# Delete the field if already exists
def delete_field_if_exists(dataset, field_name):
    if field_exists(dataset, field_name):
        arcpy.DeleteField_management(dataset, field_name)

# Calculate line numbers from PAGE letters
def calculate_row(letters):
    row = 0
    for i, letter in enumerate(reversed(letters)):
        row += (26 ** i) * (ord(letter.upper()) - ord('A') + 1)
    return row

# The main function that executes the entire workflow
def main():
    # Enable the overwrite existing dataset option
    arcpy.env.overwriteOutput = True

    # Installation of environmental workspaces and temporary workspaces
    arcpy.env.workspace = workspace
    arcpy.env.scratchWorkspace = scratch_workspace

    # Copy fishnet layer
    copied_fishnet_layer = original_fishnet_layer + "_Copy"
    copy_features(original_fishnet_layer, copied_fishnet_layer)
    fishnet_layer = copied_fishnet_layer

    # Define the intermediate output table
    out_table1 = "zonal_mean_table"
    out_table2 = "zonal_sum_table"

    # Perform zonal statistics and generate statistics table
    ZonalStatisticsAsTable(fishnet_layer, "PageName", raster1, out_table1, "DATA", "MEAN")
    ZonalStatisticsAsTable(fishnet_layer, "PageName", raster2, out_table2, "DATA", "SUM")
    print("Zonal Statistics completed.")

    # Join the statistics table to the Fishnet layer using PageName key
    arcpy.JoinField_management(fishnet_layer, "PageName", out_table1, "PageName", ["MEAN"])
    arcpy.JoinField_management(fishnet_layer, "PageName", out_table2, "PageName", ["SUM"])
    print("Fields joined.")

    # Add new field of columnID/rowID if field does not exist
    if not field_exists(fishnet_layer, "columnID"):
        arcpy.AddField_management(fishnet_layer, "columnID", "LONG")
        print("Added 'columnID' field.")
    if not field_exists(fishnet_layer, "rowID"):
        arcpy.AddField_management(fishnet_layer, "rowID", "LONG")
        print("Added 'rowID' field.")

    # Use UpdateCursor to calculate the value of rowID and columnID
    with arcpy.da.UpdateCursor(fishnet_layer, ["PageName", "rowID", "columnID"]) as cursor:
        for row in cursor:
            page_name = row[0]
            letters = ''.join(filter(str.isalpha, page_name))
            numbers = ''.join(filter(str.isdigit, page_name))

            row[1] = calculate_row(letters)  # 计算 rowID
            row[2] = int(numbers) if numbers else 0  # 提取并转换 columnID 的值

            cursor.updateRow(row)
    print("Updated cursor.")

    # Change field name and alias
    arcpy.AlterField_management(fishnet_layer, "MEAN", "NTL_MEAN", "NTL_MEAN")
    arcpy.AlterField_management(fishnet_layer, "SUM", "Floor_SUM", "Floor_SUM")
    print("Fields altered.")

    # Export the integrated fishnet layer
    arcpy.CopyFeatures_management(fishnet_layer, output_layer_1)
    print(f"Output layer created: {output_layer_1}")

    # Cleaning up intermediates
    arcpy.Delete_management(out_table1)
    arcpy.Delete_management(out_table2)
    arcpy.Delete_management(fishnet_layer)
    print("Intermediate outputs deleted.")


if __name__ == "__main__":
    main()