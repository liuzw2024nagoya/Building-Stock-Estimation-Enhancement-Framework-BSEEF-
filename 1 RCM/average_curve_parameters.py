import pandas as pd

def process_and_save_csv(input_file_path, output_file_path, output_file_path_skipna):
    """
    Processes the fit results CSV to calculate average curve parameters for each polygon.

    Parameters:
    input_file_path (str): Path to the input fit results CSV file.
    output_file_path (str): Path to save the grouped average fit results CSV file.
    output_file_path_skipna (str): Path to save the grouped average fit results CSV file, skipping NaN values.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file_path)

    # Check for missing values in the DataFrame
    missing_values_info = df.isnull().sum()
    print("Missing values information:")
    print(missing_values_info)

    # Divide the 'File' column by 10000 and take the integer part
    df['File_grouped'] = (df['File'] // 100000).astype(int)

    # Group by the new 'File_grouped' column and calculate the mean
    grouped_df = df.groupby('File_grouped').mean()

    # Reset the index and rename the 'File_grouped' column back to 'File'
    grouped_df.reset_index(inplace=True)
    grouped_df.rename(columns={'File_grouped': 'File'}, inplace=True)

    # Save the new DataFrame to a CSV file
    grouped_df.to_csv(output_file_path, index=False)
    print(f"Grouped fit results saved to '{output_file_path}'.")

    # Group by 'File_grouped' and calculate the mean, skipping missing values
    grouped_df_skipna = df.groupby('File_grouped').mean()

    # Reset the index and rename the 'File_grouped' column back to 'File'
    grouped_df_skipna.reset_index(inplace=True)
    grouped_df_skipna.rename(columns={'File_grouped': 'File'}, inplace=True)

    # Save the new DataFrame to a CSV file, skipping NaN values
    grouped_df_skipna.to_csv(output_file_path_skipna, index=False)
    print(f"Grouped fit results (skipping NaN) saved to '{output_file_path_skipna}'.")


if __name__ == '__main__':
    import config

    process_and_save_csv(
        input_file_path=config.input_fit_results_csv,
        output_file_path=config.output_grouped_csv,
        output_file_path_skipna=config.output_grouped_skipna_csv
    )


