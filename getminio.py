import minio
import io
from minio import Minio
from minio.error import S3Error
import io
import pandas as pd
from setinflux import csv_to_influxdb
from app.helpers.config_helper import props


def init_minio_connection():
    """
    Mehtod to initiate DBConnection
    :return: database_object
    """
    try:
        connection_minio = props.get_minio_connection()
        admin = props.get_minio_admin()
        key = props.get_minio_key()
        client = minio.Minio(connection_minio,
                             admin, key, secure=True)
    except Exception:
        raise Exception("Database connection error")
    return client


# minio_client = minio.Minio('play.min.io','minioadmin', 'minioadmin', secure = True)


def read_minio_object(influx_client):
    try:
        minio_client = init_minio_connection()
        bucket_name = props.get_minio_bucket()
        object_name = props.get_minio_object()
        # Read the object
        obj = minio_client.get_object(bucket_name, object_name)
        object_data = obj.read()
        print(type(object_data))
        df = pd.read_csv(io.BytesIO(object_data))
        print(df)
        csv_to_influxdb(df, influx_client)

    except S3Error as e:
        print(f"Error : {e}")
