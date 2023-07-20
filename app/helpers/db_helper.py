"""
Helper class to initialize DB connection
"""
from influxdb_client import InfluxDBClient
from app.helpers.config_helper import props


class DBHelper:
    def __init__(self):
        try:
            connection_url = props.get_properties("database", "connection_url")
            db_name = props.get_properties("database", "db_name")
            self.client = InfluxDBClient(connection_url)
        except Exception:
            raise Exception("Database connection error")


database_connection = DBHelper()
