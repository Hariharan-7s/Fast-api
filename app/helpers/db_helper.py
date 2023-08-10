"""
Helper class to initialize DB connection
"""
from influxdb_client import InfluxDBClient
from app.helpers.config_helper import props
import minio


def init_database_connection():
    """
    Mehtod to initiate DBConnection
    :return: database_object
    """
    try:
        connection_url = props.get_properties("database", "connection_url")
        db_name = props.get_properties("database", "db_name")
        influx_token = props.get_influx_token()
        influx_org = props.get_influx_org()
        client = InfluxDBClient(
            connection_url, influx_token, influx_org)
    except Exception:
        raise Exception("Database connection error")
    return client


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
                             admin, key, secure=False)
    except Exception:
        raise Exception("Database connection error")
    return client
