import logging
import sys
from app.helpers.config_helper import props


class LogHelper:
    def __init__(self):
        self.logger = None

    def set_logger_name(self, name):
        self.logger = logging.getLogger(name)

app = LogHelper()

logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stderr,
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/etl_framework.log",
            "formatter": "json"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            props.get_properties("log", "log_type")
        ],
        "propagate": True
    }
}

logging.config.dictConfig(logging_config)
