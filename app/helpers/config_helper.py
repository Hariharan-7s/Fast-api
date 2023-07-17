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


props = ConfigHelper()
