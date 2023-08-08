from influxdb_client import InfluxDBClient
import pandas as pd
from rad.result import process_temperature_values


def retrive_from_influx():

    # InfluxDB connection details
    influxdb_url = "http://10.0.0.106:8086"  # Replace with your InfluxDB URL
    # Replace with your InfluxDB token
    influxdb_token = "sIokMknLOBmfxMMrtkrMQTqImwd_wGnMH1-b6Hz_WDvuWp4-ysJ0Cl7UHpaRw-0SovIfMPXwcwmN8bd_HERnGA=="
    influxdb_org = "eminds"  # Replace with your InfluxDB organization
    influxdb_bucket = "dev"  # Replace with your InfluxDB bucket
    measurement = "dataset_tb"  # Replace with the measurement name
    time_interval = "1w"
    # Create an InfluxDB client
    client = InfluxDBClient(
        url=influxdb_url, token=influxdb_token, org=influxdb_org)

    # Flux query to retrieve all data from the specified measurement
    query = f'from(bucket: "{influxdb_bucket}") |> range(start:2014-07-01T00:00:00Z , stop:2014-10-13T01:30:00Z ) |> filter(fn: (r) => r._measurement == "{measurement}") |> aggregateWindow(every: {time_interval}, fn: mean, createEmpty: false) |> yield(name: "mean")'

    # Execute the query
    result = client.query_api().query(query, org=influxdb_org)

    # Check if the result is empty
    if not result:
        print("No data found for the specified measurement.")
        exit()

    # Extract field names dynamically from the query result
    fields = result[0].records[0].values.keys()

    data = {}

    # Iterate over the tables in the query result
    for table in result:
        # Extract the records from each table
        records = table.records

        # Extract the time and field values from the records
        for record in records:
            time = pd.to_datetime(record.get_time())
            if 'Time' not in data:
                data['Time'] = []
            data['Time'].append(time)
            for field in fields:
                if field not in data:
                    data[field] = []
                data[field].append(record.values[field])

    # Create a pandas DataFrame from the extracted data
    data_frame = pd.DataFrame(data)
    filtered_data_frame = data_frame[data_frame['_field'] == 'value']
    time_values = filtered_data_frame['Time']
    value_values = filtered_data_frame['_value']
    print("-------", data_frame)
    # print(value_values)

    #print("--------------------Temperature value before processing--------------------------------")
    # print(value_values)
    # print("---------------------------------------------------------------------------------------")
    process_temperature_values(value_values, time_values,
                               measurement, time_interval, influxdb_client=client)

    """
    temperature_values = data_frame[data_frame['_field']
                                    == 'tb']['_value']

    print(data_frame)
    #time_values = data_frame[data_frame['_field'] == 'temperature']['_time']
    # print(time_values)
    # print(data_frame)
    """
