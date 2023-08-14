import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import schedule
import time
from influxdb_client import InfluxDBClient
from result import process_temperature_values


def process_1_hour_data(client, influxdb_bucket, measurement, influxdb_client):
    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-07T00:00:00Z , stop:2014-08-09T00:00:00Z ) |> filter(fn: (r) => r._measurement == "{measurement}") |> aggregateWindow(every:1h, fn: mean, createEmpty: false) |> yield(name: "mean")'
    result = client.query_api().query(query)
    time_interval = "1h"
    if not result:
        print("No data found for the specified measurement.")
        return None

    data = {}
    fields = result[0].records[0].values.keys()

    for table in result:
        records = table.records

        for record in records:
            time = pd.to_datetime(record.get_time())
            if 'Time' not in data:
                data['Time'] = []
            data['Time'].append(time)
            for field in fields:
                if field not in data:
                    data[field] = []
                data[field].append(record.values[field])

    data_frame = pd.DataFrame(data)
    filtered_data_frame = data_frame[data_frame['_field'] == 'value']
    time_values = filtered_data_frame['Time']
    value_values = filtered_data_frame['_value']

    print("Processing 1-hour data...")
    data_frame['timestamp'] = pd.to_datetime(data_frame['Time'])
    earliest_timestamp = data_frame['timestamp'].min()
    # Use the actual datetime objects
    latest_timestamp = data_frame['timestamp'].max()
    time_difference = latest_timestamp - earliest_timestamp
    """print("Time difference:", time_difference)
    print("earliest", earliest_timestamp)
    print("last", latest_timestamp)
    print('--------------------')"""
    values = data_frame['_value']
    data_values = np.array(values)
    #print(time_values, value_values)
    #print("Hour: ", data_values)
    process_temperature_values(
        value_values, time_values, measurement, time_interval, influxdb_client)
    # Compare the time difference with 24 hours
    if time_difference >= timedelta(hours=23):
        print("24 hours of data is complete.")
        process_1_day_data(time_difference,
                           influxdb_bucket, measurement, influxdb_client)


def process_1_day_data(time_difference, influxdb_client, influxdb_bucket, measurement):
    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-07T00:00:00Z , stop:2014-08-09T00:00:00Z ) |> filter(fn: (r) => r._measurement == "{measurement}") |> aggregateWindow(every:1d, fn: mean, createEmpty: false) |> yield(name: "mean")'
    result = influxdb_client.query_api().query(query)
    time_interval = "1d"
    if not result:
        print("No data found for the specified measurement.")
        return None

    data = {}
    fields = result[0].records[0].values.keys()

    for table in result:
        records = table.records

        for record in records:
            time = pd.to_datetime(record.get_time())
            if 'Time' not in data:
                data['Time'] = []
            data['Time'].append(time)
            for field in fields:
                if field not in data:
                    data[field] = []
                data[field].append(record.values[field])

    data_frame = pd.DataFrame(data)
    filtered_data_frame = data_frame[data_frame['_field'] == 'value']
    time_values = filtered_data_frame['Time']
    value_values = filtered_data_frame['_value']
    print("Processing 1-day data...")
    data_frame['timestamp'] = pd.to_datetime(data_frame['Time'])
    values = data_frame['_value']
    data_values = np.array(values)
    print('day: ', data_values)
    process_temperature_values(
        value_values, time_values, measurement, time_interval, influxdb_client)
    # Compare the time difference with 7 days
    if time_difference >= timedelta(days=7):
        print("1 week of data is started.")
        process_1_week_data(time_difference, influxdb_client,
                            influxdb_bucket, measurement)


def process_1_week_data(time_difference, influxdb_client, influxdb_bucket, measurement):
    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-07T00:00:00Z , stop:2014-08-09T00:00:00Z ) |> filter(fn: (r) => r._measurement == "{measurement}") |> aggregateWindow(every:1w, fn: mean, createEmpty: false) |> yield(name: "mean")'
    result = influxdb_client.query_api().query(query)
    time_interval = "1w"
    if not result:
        print("No data found for the specified measurement.")
        return None

    data = {}
    fields = result[0].records[0].values.keys()

    for table in result:
        records = table.records

        for record in records:
            time = pd.to_datetime(record.get_time())
            if 'Time' not in data:
                data['Time'] = []
            data['Time'].append(time)
            for field in fields:
                if field not in data:
                    data[field] = []
                data[field].append(record.values[field])

    data_frame = pd.DataFrame(data)
    filtered_data_frame = data_frame[data_frame['_field'] == 'value']
    time_values = filtered_data_frame['Time']
    value_values = filtered_data_frame['_value']
    data_frame['timestamp'] = pd.to_datetime(data_frame['Time'])

    values = data_frame['_value']
    data_values = np.array(values)
    print("Processing 1-week data...")
    print("Week: ", data_values)
    process_temperature_values(
        value_values, time_values, measurement, time_interval, influxdb_client)
    # Compare the time difference with 28 days
    if time_difference >= timedelta(days=28):
        print("month of data is started.")
        process_1_month_data(time_difference, influxdb_client,
                             influxdb_bucket, measurement)


def process_1_month_data(time_difference, influxdb_client, influxdb_bucket, measurement):
    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-07T00:00:00Z , stop:2014-08-09T00:00:00Z ) |> filter(fn: (r) => r._measurement == "{measurement}") |> aggregateWindow(every:1mo, fn: mean, createEmpty: false) |> yield(name: "mean")'
    result = influxdb_client.query_api().query(query)
    time_interval = "1mo"
    if not result:
        print("No data found for the specified measurement.")
        return None

    data = {}
    fields = result[0].records[0].values.keys()

    for table in result:
        records = table.records

        for record in records:
            time = pd.to_datetime(record.get_time())
            if 'Time' not in data:
                data['Time'] = []
            data['Time'].append(time)
            for field in fields:
                if field not in data:
                    data[field] = []
                data[field].append(record.values[field])
    print("Processing 1-month data...")
    data_frame = pd.DataFrame(data)
    filtered_data_frame = data_frame[data_frame['_field'] == 'value']
    time_values = filtered_data_frame['Time']
    value_values = filtered_data_frame['_value']
    data_frame['timestamp'] = pd.to_datetime(data_frame['Time'])

    values = data_frame['_value']
    data_values = np.array(values)
    print("Month: ", data_values)

    # Compare the time difference with 365 days (1 year)
    if time_difference >= timedelta(days=365):
        print("1 year of data is complete.")
        # process_1_year_data(time_difference)


def process_1_year_data(time_difference):
    print("Processing 1-year data...")
    # Your yearly data processing logic here
    pass


def setup_scheduler():
    influxdb_url = "http://localhost:8086"  # Replace with your InfluxDB URL
    # Replace with your InfluxDB token
    influxdb_token = "VvOF3pA9dwR_OvaiOCL90J_Q0ZkTWdonJW7eGu6qUJJzb9kpZa5pl-w5AB2fVvA92-wnuXt284IdVU0pIpU81g=="
    influxdb_org = "Hari"  # Replace with your InfluxDB organization
    influxdb_bucket = "sample"  # Replace with your InfluxDB bucket
    measurement = "dataset_tb"  # Replace with your measurement name
    time_interval = "1h"

    client = InfluxDBClient(
        url=influxdb_url, token=influxdb_token, org=influxdb_org)
    # dd = retrive_from_influx(client, influxdb_bucket,measurement, time_interval)
    schedule.every(1).second.do(process_1_hour_data,
                                influxdb_bucket, measurement, influxdb_client=client)
    # schedule.every().day.at("00:00").do(process_1_day_data, timedelta(days=1))
    # schedule.every().monday.at("00:00").do(process_1_week_data, timedelta(weeks=1))

    while True:
        schedule.run_pending()
        time.sleep(10)  # Adjust the sleep time as needed


# Example usage
setup_scheduler()


"""
def retrive_from_influx(influxdb_client, influxdb_bucket, measurement, time_interval):
    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-07T00:00:00Z , stop:2014-07-08T00:00:00Z ) |> filter(fn: (r) => r._measurement == "{measurement}") |> aggregateWindow(every: {time_interval}, fn: mean, createEmpty: false) |> yield(name: "mean")'
    result = influxdb_client.query_api().query(query)

    if not result:
        print("No data found for the specified measurement.")
        return None

    data = {}
    fields = result[0].records[0].values.keys()

    for table in result:
        records = table.records

        for record in records:
            time = pd.to_datetime(record.get_time())
            if 'Time' not in data:
                data['Time'] = []
            data['Time'].append(time)
            for field in fields:
                if field not in data:
                    data[field] = []
                data[field].append(record.values[field])

    data_frame = pd.DataFrame(data)
    filtered_data_frame = data_frame[data_frame['_field'] == 'value']
    time_values = filtered_data_frame['Time']
    value_values = filtered_data_frame['_value']

    return data_frame
"""
