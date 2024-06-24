import argparse
import time
import json
from data_analysis import perform_data_analysis
from utils import format_elapsed_time

def main(train_files, validation_files, output_directory, dependent_var, independent_vars, models_config):
    data_analysis_start_time = time.time()
    perform_data_analysis(train_files, validation_files, output_directory, dependent_var, independent_vars, models_config)
    data_analysis_end_time = time.time()
    print(f"Data analysis complete. Time elapsed: {format_elapsed_time(data_analysis_end_time - data_analysis_start_time)}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script for model training and prediction with specified CSV files.")
    parser.add_argument('--train_files', nargs='+', type=str, required=True, help='Paths to the training CSV files.')
    parser.add_argument('--validation_files', nargs='+', type=str, required=True, help='Paths to the validation CSV files.')
    parser.add_argument('--output_directory', type=str, required=True, help='Directory to save output files.')
    parser.add_argument('--dependent_var', type=str, required=True, help='The dependent variable for the models.')
    parser.add_argument('--independent_vars', nargs='+', type=str, required=True, help='The independent variables for the models.')
    parser.add_argument('--models_config', type=str, required=True, help='JSON string representing the models to be tested.')

    args = parser.parse_args()

    models_config = json.loads(args.models_config)

    main(args.train_files, args.validation_files, args.output_directory, args.dependent_var, args.independent_vars, models_config)
