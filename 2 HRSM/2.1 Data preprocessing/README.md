
# BSEEF-HRSM Data Preprocessing Scripts

## Overview

This repository includes scripts for data preprocessing from geospatial data using ArcPy. It then exports CSV files which can be processed by HRSM.



## Installation

1. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

2. Ensure you have ArcPy installed and configured properly.

## Usage

1. Run the main script:
    ```sh
    python main.py
    ```
## Directory Structure

```
project/
│
├── main.py
├── fishnet_extract.py
├── fishnet_kernel_filter.py
├── config.py
├── requirements.txt
└── README.md
```

- `main.py`: The main script for invoking the two data preprocessing modules.
- `fishnet_extract.py`: Processes the fishnet layer and extract raster values to fishnet grids.
- `fishnet_kernel_filter.py`: Applies various edge detection filter operators to the processed fishnet layer and exports to a CSV file.
- `config.py`: Contains all the configurable variables for the scripts.
- `requirements.txt`: List of required Python packages.
- `README.md`: This README file.


## License

This repository is developed for the article "Adaptive Nighttime Light-Based Building Stock Assessment Framework for Future Environmentally Sustainable Management".
