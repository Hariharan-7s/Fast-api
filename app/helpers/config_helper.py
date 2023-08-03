"""
Helper file to keep the common function
"""
import os
import configparser
from dotenv import load_dotenv


class ConfigHelper:
    def __init__(self):
        # Reading the dotenv file to select the appropriate properties file
        BASEDIR = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(os.path.join(BASEDIR, '../../.env'))
        env = os.getenv("ENVIRONMENT")
        self.filepath = "app/properties/" + env + "_properties.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.filepath)

    def get_properties(self, section, param):
        value = self.config.get(section, param)
        return value

    def get_influx_token(self):
        return self.get_properties('database', 'token')

    def get_influx_org(self):
        return self.get_properties('database', 'org')

    def get_minio_connection(self):
        return self.get_properties('minio', 'connection_minio')

    def get_minio_admin(self):
        return self.get_properties('minio', 'admin')

    def get_minio_key(self):
        return self.get_properties('minio', 'key')

    def get_minio_bucket(self):
        return self.get_properties('minio', 'bucket_name')

    def get_minio_object(self):
        return self.get_properties('minio', 'object_name')


props = ConfigHelper()
