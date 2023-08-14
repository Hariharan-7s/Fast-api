# File: result.py
import numpy as np
import matplotlib.pyplot as plt
from rad._anomaly_detection import AnomalyDetection_RPCA
import pandas as pd
from rad.csvdata import points_to_csv


def find_s_parameter(outliers):
    # find mean & standard deviation
    outliers_mean = np.mean(outliers)

    #print("mean :", outliers_mean)
    outliers_standard_deviation = np.std(outliers)
    #print("std_d :", outliers_standard_deviation)
    # Find the S-parameter for the outliers
    s_parameters = []
    for outlier in outliers:
        s_parameters.append((outlier - outliers_mean) /
                            outliers_standard_deviation)

    return s_parameters


def process_temperature_values(value_values, time_values, measurement, time_interval, influxdb_client):
    # Convert temperature_values to time series data
    time_series = np.array(value_values)

    # Create an instance of AnomalyDetection_RPCA
    anomaly_detector = AnomalyDetection_RPCA(
        frequency=7, autodiff=True, scale=True)

    # Fit the model and transform the data
    L, S, E = anomaly_detector.fit_transform(time_series)

    # Get the outliers
    outliers = anomaly_detector.get_outliers()
    #outliers_s_parameter = find_s_parameter(outliers)
    csv_data = points_to_csv(outliers, time_values,
                             measurement, time_interval, influxdb_client)

    # print(outliers)
    """
    print("--------------------s_paramter--------------------------------")
    print("s-parameter: ", outliers_s_parameter)
    print("--------------------------------------------------------------")
    
    plt.figure()
    plt.plot(time_series, label='Original')


# Get the x-coordinates for the outlier points (indices of the outliers in the time_series array)
    outlier_indices = np.where(outliers != 0)[0]

# Get the corresponding y-coordinates for the outlier points (outlier values)
    outlier_values = time_series[outlier_indices]

# Plot the outlier points on the original time series
    plt.scatter(outlier_indices, outlier_values,
                color='red', marker='o', label='Outliers')

    plt.legend()
    plt.show()
"""
