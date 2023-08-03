import influxdb_client
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def csv_to_influxdb(df, influx_client):
    # Read CSV data into a pandas DataFrame
    data = df

    # Convert DataFrame to InfluxDB-compatible Point objects
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    points = []

    for _, row in data.iterrows():
        point = Point(row['measurement']).time(
            row['timestamp'], WritePrecision.NS)

        # Process tags
        for tag in row['tag_key=tag_value'].split(' '):
            key, value = tag.split('=')
            point = point.tag(key, value)

        # Process fields
        for field in row['field_key=field_value'].split(','):
            key, value = field.split('=')
            point = point.field(key, float(value))

        points.append(point)

    # Write the data to InfluxDB
    write_api.write(bucket="dev", org="eminds", record=points)
    print("inserted successfully ")
