import arcpy
import csv
import os
import config  # Import the configuration module

# Exports the attributes of point values on each cross-section to CSV files.
def export_to_csv(workspace, output_folder, desired_fields):
    """
    Parameters:
    workspace (str): Path to the geodatabase containing the feature classes.
    output_folder (str): Path to the folder where the CSV files will be saved.
    desired_fields (list): List of fields to export.
    """
    # Set workspace
    arcpy.env.workspace = workspace

    # Get all feature classes in the geodatabase
    feature_classes = arcpy.ListFeatureClasses()

    # Loop through each feature class
    for feature_class in feature_classes:
        feature_class_path = os.path.join(workspace, feature_class)
        print(feature_class)

        # Build the output CSV file path
        output_csv_path = os.path.join(output_folder, f"{feature_class}.csv")

        # Use SearchCursor to read the attributes of the feature class
        with arcpy.da.SearchCursor(feature_class_path, desired_fields) as cursor:
            # Open the CSV file and write the header
            with open(output_csv_path, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(desired_fields)

                # Write each row of attributes to the CSV file
                for row in cursor:
                    csv_writer.writerow(row)

    print("CSV export completed.")


if __name__ == '__main__':
    export_to_csv(
        workspace=config.csv_workspace,
        output_folder=config.csv_output_folder,
        desired_fields=config.csv_desired_fields
    )
