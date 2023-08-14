from influxdb_client import InfluxDBClient
import pandas as pd
from rad.result import process_temperature_values
from datetime import datetime, timedelta
import numpy as np
from app.helpers.config_helper import props
from app.helpers.db_helper import init_database_connection

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import schedule
import time
from influxdb_client import InfluxDBClient
from rad.result import process_temperature_values


def process_1_hour_data(client, influxdb_bucket, measurement):

    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-07T00:00:00Z , stop:2015-01-25T00:00:00Z ) |> filter(fn: (r) => r["_measurement"] == "{measurement}") |> aggregateWindow(every: 1h, fn: mean, createEmpty: false) |> yield(name: "mean")'
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

    time_values = data_frame['Time']
    value_values = data_frame['_value']

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

    # print(time_values, value_values)
    # print("Hour: ", data_values)
    process_temperature_values(
        value_values, time_values, measurement, time_interval, client)
    # Compare the time difference with 24 hours
    if time_difference >= timedelta(hours=23):
        print("24 hours of data is complete.")
        process_1_day_data(time_difference, client,
                           influxdb_bucket, measurement)


def process_1_day_data(time_difference, client, influxdb_bucket, measurement):
    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-07T00:00:00Z , stop:2015-01-25T00:00:00Z ) |> filter(fn: (r) => r._measurement == "{measurement}") |> aggregateWindow(every:1d, fn: mean, createEmpty: false) |> yield(name: "mean")'
    result = client.query_api().query(query)
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

    time_values = data_frame['Time']
    value_values = data_frame['_value']
    print("Processing 1-day data...")
    data_frame['timestamp'] = pd.to_datetime(data_frame['Time'])

    print('day: ', value_values)
    process_temperature_values(
        value_values, time_values, measurement, time_interval, client)
    # Compare the time difference with 7 days
    if time_difference >= timedelta(days=7):
        print("1 week of data is started.")
        process_1_week_data(time_difference, client,
                            influxdb_bucket, measurement)


def process_1_week_data(time_difference, client, influxdb_bucket, measurement):
    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-07T00:00:00Z , stop:2015-01-25T00:00:00Z ) |> filter(fn: (r) => r._measurement == "{measurement}") |> aggregateWindow(every:1w, fn: mean, createEmpty: false) |> yield(name: "mean")'
    result = client.query_api().query(query)
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

    time_values = data_frame['Time']
    value_values = data_frame['_value']
    data_frame['timestamp'] = pd.to_datetime(data_frame['Time'])

    print("Processing 1-week data...")
    print("Week: ", value_values)
    process_temperature_values(
        value_values, time_values, measurement, time_interval, client)
    # Compare the time difference with 28 days
    if time_difference >= timedelta(days=28):
        print("month of data is started.")
        process_1_month_data(time_difference, client,
                             influxdb_bucket, measurement)


def process_1_month_data(time_difference, client, influxdb_bucket, measurement):
    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-07T00:00:00Z , stop:2015-01-25T00:00:00Z ) |> filter(fn: (r) => r._measurement == "{measurement}") |> aggregateWindow(every:1mo, fn: mean, createEmpty: false) |> yield(name: "mean")'
    result = client.query_api().query(query)
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

    time_values = data_frame['Time']
    value_values = data_frame['_value']
    data_frame['timestamp'] = pd.to_datetime(data_frame['Time'])
    print("Month: ", value_values)
    process_temperature_values(
        value_values, time_values, measurement, time_interval, client)
    # Compare the time difference with 365 days (1 year)
    if time_difference >= timedelta(days=365):
        print("1 year of data is complete.")
        # process_1_year_data(time_difference)


def setup_scheduler(measurement):
    print("called")
    influxdb_bucket = props.get_properties(
        "database", "db_name")  # Replace with your InfluxDB bucket
    connection_url = props.get_properties("database", "connection_url")
    influx_token = props.get_influx_token()
    influx_org = props.get_influx_org()

    client = InfluxDBClient(
        url=connection_url, token=influx_token, org=influx_org)

    schedule.every(1).second.do(process_1_hour_data, client,
                                influxdb_bucket, measurement)

    while True:
        schedule.run_pending()
        time.sleep(10)  # Adjust the sleep time as needed
