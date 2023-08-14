import pandas as pd
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from app.helpers.config_helper import props
from rad.getdata import setup_scheduler


def csv_to_influxdb(df, influx_client):
    # Read CSV data into a pandas DataFrame
    data = df
    measurement = data['measurement'][0]
    #print("---------->", measurement)
    # Convert DataFrame to InfluxDB-compatible Point objects
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    points = []

    for _, row in data.iterrows():
        point = Point(row['measurement']).time(
            row['timestamp'], WritePrecision.NS)

        # Process tags
        # for tag in row['tag_key=tag_value'].split(','):
        # key, value = tag.split(' = ')
        # point = point.tag(key, value)

        # Process fields
        for field in row['field_key=field_value'].split(','):
            key, value = field.split('=')
            point = point.field(key, float(value))

        points.append(point)

    bucket = props.get_properties("database", "db_name")
    org = props.get_influx_org()
    # Write the data to InfluxDB
    write_api.write(bucket=bucket, org=org, record=points)
    print(" source data inserted  ")

    setup_scheduler(measurement)
