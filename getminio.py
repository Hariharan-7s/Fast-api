import minio
import io
from minio import Minio
from minio.error import S3Error
import io
import pandas as pd
from setinflux import csv_to_influxdb

minio_client = minio.Minio('play.min.io',
                           'WWT243vlCzx24DlcGKxJ', '4RQoYZ2E2SSo6XeYGchftXEucp5NDqX8lKc4erxk', secure=True)


def read_minio_object(bucket_name, object_name, influx_client):
    try:

        # Read the object
        obj = minio_client.get_object(bucket_name, object_name)
        object_data = obj.read()
        print(type(object_data))
        df = pd.read_csv(io.BytesIO(object_data))
        print(df)
        csv_to_influxdb(df, influx_client)

        # Process the object data as needed
        print(f"Object data:\n{object_data.decode()}")

    except S3Error as e:
        print(f"Error : {e}")
