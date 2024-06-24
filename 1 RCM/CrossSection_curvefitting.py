import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def normal_distribution(x, pi, mu, sigma):
    """
    Define the normal distribution function for curve fitting.

    Parameters:
    x (array-like): Independent variable.
    pi (float): Amplitude of the distribution.
    mu (float): Mean of the distribution.
    sigma (float): Standard deviation of the distribution.

    Returns:
    array-like: Calculated values based on the normal distribution function.
    """
    return pi * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


def fit_data(x, y):
    """
    Fit the normal distribution function to the given data.

    Parameters:
    x (array-like): Independent variable.
    y (array-like): Dependent variable.

    Returns:
    tuple: Fitted parameters (pi, mu, sigma) or None if fitting fails.
    """
    valid_indices = np.isfinite(x) & np.isfinite(y)
    x_valid = x[valid_indices]
    y_valid = y[valid_indices]

    # Check for sufficient number of data points
    if len(x_valid) < 3 or len(y_valid) < 3:
        print("Insufficient number of data points. Skipping this dataset.")
        return None

    else:
        # Adjust initial guess
        initial_guess = [np.max(y_valid), np.mean(x_valid), np.std(x_valid)]

        # Try different optimization algorithms
        try:
            params, _ = curve_fit(normal_distribution, x_valid, y_valid, p0=initial_guess, method='lm', maxfev=1000)
        except RuntimeError:
            return None

        pi, mu, sigma = params
        return pi, mu, sigma


def curve_fitting(csv_folder, fit_results_folder, fit_results_csv):
    """
    Perform curve fitting on CSV data and save results.

    Parameters:
    csv_folder (str): Path to the folder containing the CSV files.
    fit_results_folder (str): Path to the folder to save the fit results plots.
    fit_results_csv (str): Path to the output CSV file to save the fit parameters.
    """
    results_df = pd.DataFrame(columns=["File", "Mu", "Sigma", "Pi", "Peak", "Span"])

    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            print(filename)
            file_path = os.path.join(csv_folder, filename)
            data = pd.read_csv(file_path)
            if data.iloc[:, 1].isna().all():
                print(f"Skipping {filename} because the second column has no data.")
            else:
                x = data["OBJECTID"].values
                y = data["RASTERVALU"].values
                y_filled = np.where(np.isnan(y), 0, y)
                result = fit_data(x, y)
                if result is None:
                    pi, mu, sigma = None, None, None
                else:
                    pi, mu, sigma = result

                    if pi is not None:
                        CSspan = (max(x) - min(x)) * 0.1  # Calculate the span of each cross section (km)
                        max_value = np.max(y_filled)  # Calculate the peak value of each cross section (nW/cm2/sr)
                        results_df = results_df.append({"File": filename[:-4], "Mu": mu, "Sigma": sigma, "Pi": pi,
                                                        "Peak": max_value, "Span": CSspan}, ignore_index=True)

                        x_fit = np.linspace(min(x), max(x), 100)
                        y_fit = normal_distribution(x_fit, pi, mu, sigma)
                        plt.plot(x, y, label='Data Points')
                        plt.plot(x_fit, y_fit, 'r-', label='Fit Curve')
                        plt.legend()
                        plt.xlabel('OBJECTID')
                        plt.ylabel('NTL(nW/cm2/sr)')
                        plot_filename = os.path.splitext(filename)[0] + "_plot.png"
                        plot_path = os.path.join(fit_results_folder, plot_filename)
                        plt.savefig(plot_path)
                        plt.close()
                    else:
                        print("Skipping this dataset due to insufficient data points or an error in fitting.")

    results_df.to_csv(fit_results_csv, index=False)
    print(f"Fit results have been saved to '{fit_results_csv}'.")


if __name__ == '__main__':
    import config

    curve_fitting(
        csv_folder=config.csv_output_folder,
        fit_results_folder=config.fit_results_folder,
        fit_results_csv=config.fit_results_csv
    )

