import csv
import pandas as pd
from rad.pandas_insert import csv_to_influxdb


def points_to_csv(outliers, time_values, measurement, time_interval, infulxdb_client):
    interval = get_time_interval_name(time_interval)
    data = []

    # Iterate through each data point and timestamp and append them to the data list
    for timestamp, value in zip(time_values, outliers):
        # Convert timestamp to string with desired format 'dd-mm-yyyy HH:MM'
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M')

        # Append the data point as a row to the data list
        data.append({
            'timestamp': formatted_timestamp,
            'measurement': f"{measurement}_outlier",
            'tag_key=tag_value': f"interval={interval}",
            # Updated field_key=field_value
            f'field_key=field_value': f"outlier={value}"
        })

    # Create a DataFrame from the data list
    df = pd.DataFrame(data)
    # print(df)
    csv_to_influxdb(df, infulxdb_client)


def get_time_interval_name(time_interval):
    # Convert the time interval to lowercase to handle variations in input
    time_interval = time_interval.lower()

    if time_interval == "1w":
        return "Week"
    elif time_interval == "1mo":
        return "Month"
    elif time_interval == "1d":
        return "Day"
    elif time_interval == "1h":
        return "Hour"
    else:
        # If the time interval is not recognized, return it as is
        return time_interval
