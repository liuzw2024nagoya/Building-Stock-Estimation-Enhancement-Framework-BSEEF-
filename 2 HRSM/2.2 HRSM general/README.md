
# BSEEF-HRSM Model Training and Predicting Scripts

This repository contains a script of BSEEF-HRSM for optimizing models and generating predictions based on user-specified training and validation CSV files. The script supports multiple models and allows users to customize the dependent and independent variables as well as the models to be tested.

## Features

- Supports multiple machine learning models from `scikit-learn`.
- Allows customization of dependent and independent variables.
- Outputs predictions to specified CSV files.
- Logs model evaluation results.
- You can continue to add other available model classes in `data_analysis.py`.

## Prerequisites

- Python 3.x
- `scikit-learn` library
- `pandas` library

## Installation

Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Command-Line Arguments

- `--train_files`: Paths to the training CSV files (required).
- `--validation_files`: Paths to the validation CSV files (required).
- `--output_directory`: Directory to save output files (required).
- `--dependent_var`: The dependent variable for the models (required).
- `--independent_vars`: The independent variables for the models (required).
- `--models_config`: JSON string representing the models to be tested (required).

### Example Command

Assuming you have the following training and validation files:
- Training files: `train1.csv`, `train2.csv`
- Validation files: `val1.csv`, `val2.csv`

To use the dependent variable `Floor_SUM` and independent variables `NTL_MEAN` and `NTL_MEAN_Convolution_3x3`, with the following models and configurations:

```json
{
    "LinearRegression": {},
    "DecisionTreeRegressor": {"max_depth": 3},
    "GradientBoostingRegressor": {"n_estimators": 100},
    "MLPRegressor": {"max_iter": 200},
    "RandomForestRegressor": {"n_estimators": 100},
    "SVR": {"kernel": "linear"}
}
```

Run the following command:

```sh
python main.py --train_files train1.csv train2.csv --validation_files val1.csv val2.csv --output_directory ./output --dependent_var Floor_SUM --independent_vars NTL_MEAN NTL_MEAN_Convolution_3x3 --models_config '{"LinearRegression": {}, "DecisionTreeRegressor": {"max_depth": 3}, "GradientBoostingRegressor": {"n_estimators": 100}, "MLPRegressor": {"max_iter": 200}, "RandomForestRegressor": {"n_estimators": 100}, "SVR": {"kernel": "linear"}}'
```

## Directory Structure

The directory structure of the repository is as follows:

```
project/
│
├── main.py
├── data_analysis.py
├── utils.py
├── requirements.txt
└── README.md
```

- `main.py`: The main script for parsing command-line arguments and invoking the data analysis module.
- `data_analysis.py`: The data analysis module for training models and generating predictions.
- `utils.py`: Utility functions used in the project.
- `requirements.txt`: List of required Python packages.
- `README.md`: This README file.


## License

This repository is developed for the article "Adaptive Nighttime Light-Based Building Stock Assessment Framework for Future Environmentally Sustainable Management".
