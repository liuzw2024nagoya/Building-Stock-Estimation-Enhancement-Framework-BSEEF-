import arcpy
import math
from config import workspace, output_layer_1, output_layer_2, csv_output_path

# Copy input layer to output layer
def copy_features(input_layer, output_layer):
    arcpy.CopyFeatures_management(input_layer, output_layer)
    print(f"Copied {input_layer} to {output_layer}")

# Add fields to layer
def add_fields(layer, fields):
    for field, field_type in fields:
        arcpy.AddField_management(layer, field, field_type)
        print(f"Added field {field} of type {field_type}")

# Calculate convolution
def calculate_convolution(row_id, column_id, data_dict, size):
    total = 0
    count = size * size

    for i in range(-(size // 2), (size // 2) + 1):
        for j in range(-(size // 2), (size // 2) + 1):
            neighbor_row = row_id + i
            neighbor_column = column_id + j
            total += data_dict.get((neighbor_row, neighbor_column), 0)

    return total / count

# Calculate the Sobel Operator
def calculate_sobel(row_id, column_id, data_dict):
    Gx = 0
    Gy = 0

    sobel_kernel_x = [(-1, -1, -1), (-1, 0, -2), (-1, 1, -1),
                      (0, -1, 0), (0, 0, 0), (0, 1, 0),
                      (1, -1, 1), (1, 0, 2), (1, 1, 1)]
    sobel_kernel_y = [(-1, -1, 1), (-1, 0, 0), (-1, 1, -1),
                      (0, -1, 2), (0, 0, 0), (0, 1, -2),
                      (1, -1, 1), (1, 0, 0), (1, 1, -1)]

    for dx, dy, value in sobel_kernel_x:
        neighbor_row = row_id + dx
        neighbor_column = column_id + dy
        Gx += data_dict.get((neighbor_row, neighbor_column), 0) * value

    for dx, dy, value in sobel_kernel_y:
        neighbor_row = row_id + dx
        neighbor_column = column_id + dy
        Gy += data_dict.get((neighbor_row, neighbor_column), 0) * value

    return math.sqrt(Gx ** 2 + Gy ** 2)

# Calculate the Prewitt Operator
def calculate_prewitt(row_id, column_id, data_dict):
    Gx = 0
    Gy = 0

    prewitt_kernel_x = [(-1, -1, -1), (-1, 0, -1), (-1, 1, -1),
                        (0, -1, 0), (0, 0, 0), (0, 1, 0),
                        (1, -1, 1), (1, 0, 1), (1, 1, 1)]
    prewitt_kernel_y = [(-1, -1, 1), (-1, 0, 1), (-1, 1, 1),
                        (0, -1, 0), (0, 0, 0), (0, 1, 0),
                        (1, -1, -1), (1, 0, -1), (1, 1, -1)]

    for dx, dy, value in prewitt_kernel_x:
        neighbor_row = row_id + dx
        neighbor_column = column_id + dy
        Gx += data_dict.get((neighbor_row, neighbor_column), 0) * value

    for dx, dy, value in prewitt_kernel_y:
        neighbor_row = row_id + dx
        neighbor_column = column_id + dy
        Gy += data_dict.get((neighbor_row, neighbor_column), 0) * value

    return math.sqrt(Gx ** 2 + Gy ** 2)

# Calculate the Laplacian Operator
def calculate_laplacian(row_id, column_id, data_dict):
    """
    计算 Laplacian 算子。
    """
    laplacian_kernel = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    center_value = data_dict.get((row_id, column_id), 0)
    laplacian_sum = -4 * center_value

    for dx, dy in laplacian_kernel:
        neighbor_row = row_id + dx
        neighbor_column = column_id + dy
        laplacian_sum += data_dict.get((neighbor_row, neighbor_column), 0)

    return abs(laplacian_sum)

# The main function that executes the entire workflow.
def main():
    # Enable the overwrite existing dataset option
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = workspace

    # Copy layer
    copy_features(output_layer_1, output_layer_2)

    # Add kernel filter fields
    fields_to_add = [
        ('NTL_MEAN_Convolution_3x3', 'FLOAT'),
        ('NTL_MEAN_Convolution_5x5', 'FLOAT'),
        ('Edge_Strength_Sobel', 'FLOAT'),
        ('Edge_Strength_Prewitt', 'FLOAT'),
        ('Edge_Strength_Laplacian', 'FLOAT')
    ]
    add_fields(output_layer_2, fields_to_add)

    # Create data dictionary
    data_dict = {}
    with arcpy.da.SearchCursor(output_layer_1, ['rowID', 'columnID', 'NTL_MEAN']) as cursor:
        for row in cursor:
            data_dict[(row[0], row[1])] = row[2]

    # Calculate convolution and update fields
    with arcpy.da.UpdateCursor(output_layer_2,
                               ['rowID', 'columnID', 'NTL_MEAN_Convolution_3x3', 'NTL_MEAN_Convolution_5x5']) as cursor:
        for row in cursor:
            row[2] = calculate_convolution(row[0], row[1], data_dict, 3)  # 3x3 卷积
            row[3] = calculate_convolution(row[0], row[1], data_dict, 5)  # 5x5 卷积
            cursor.updateRow(row)
    print("3x3 and 5x5 Convolution calculations completed.")

    # Calculate Sobel Operator and update fields
    with arcpy.da.UpdateCursor(output_layer_2, ['rowID', 'columnID', 'Edge_Strength_Sobel']) as cursor:
        for row in cursor:
            row[2] = calculate_sobel(row[0], row[1], data_dict)
            cursor.updateRow(row)
    print("Sobel edge strength calculation completed.")

    # Calculate Prewitt Operator and update fields
    with arcpy.da.UpdateCursor(output_layer_2, ['rowID', 'columnID', 'Edge_Strength_Prewitt']) as cursor:
        for row in cursor:
            row[2] = calculate_prewitt(row[0], row[1], data_dict)
            cursor.updateRow(row)
    print("Prewitt edge strength calculation completed.")

    # Calculate Laplacian Operator and update fields
    with arcpy.da.UpdateCursor(output_layer_2, ['rowID', 'columnID', 'Edge_Strength_Laplacian']) as cursor:
        for row in cursor:
            row[2] = calculate_laplacian(row[0], row[1], data_dict)
            cursor.updateRow(row)
    print("Laplacian edge strength calculation completed.")

    # Export to CSV
    arcpy.TableToTable_conversion(output_layer_2, csv_output_path.rsplit('/', 1)[0], csv_output_path.rsplit('/', 1)[1])
    print(f"Exported to CSV at {csv_output_path}")


if __name__ == "__main__":
    main()
