import arcpy
from collections import Counter

def classify_remaining_polygons(polygon_layer, cluster_field, temp_layer):
    """
    Classifies remaining polygons with null cluster information based on adjacent polygons' cluster values.

    Parameters:
    polygon_layer (str): Path to the polygon layer.
    cluster_field (str): Name of the cluster field.
    temp_layer (str): Path to the temporary layer.
    """
    # Creates a temporary layer to store the selected features
    arcpy.MakeFeatureLayer_management(polygon_layer, temp_layer)

    # Select polygons with NULL clustering results
    query = "{} IS NULL".format(cluster_field)
    arcpy.SelectLayerByAttribute_management(temp_layer, "NEW_SELECTION", query)

    # Get an OID list for polygons clustered at NULL
    null_polygons = [row[0] for row in arcpy.da.SearchCursor(temp_layer, "OID@")]

    # For each polygon clustered at NULL
    for oid in null_polygons:
        # Select the current polygon
        arcpy.SelectLayerByAttribute_management(temp_layer, "NEW_SELECTION", "OBJECTID = {}".format(oid))

        # Select the polygons that adjacent to the current polygon
        arcpy.SelectLayerByLocation_management(temp_layer, "INTERSECT", temp_layer, selection_type="NEW_SELECTION")

        # Get a list of clustering results for adjacent polygons
        adjacent_clusters = [row[0] for row in arcpy.da.SearchCursor(temp_layer, cluster_field) if row[0] is not None]

        # If the adjacent_clusters list is empty, slip the current iteration
        if not adjacent_clusters:
            continue

        # Determine the most common clustering results
        most_common_cluster = Counter(adjacent_clusters).most_common(1)[0][0]

        # Update the clustering results for the current polygons clustered at NULL
        with arcpy.da.UpdateCursor(temp_layer, cluster_field, "OBJECTID = {}".format(oid)) as cursor:
            for row in cursor:
                row[0] = most_common_cluster
                cursor.updateRow(row)

    print("Process completed!")


if __name__ == '__main__':
    import config

    classify_remaining_polygons(
        polygon_layer=config.polygon_layer,
        cluster_field=config.cluster_field,
        temp_layer=config.temp_layer
    )
