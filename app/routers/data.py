from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.helpers.log_helper import app
from app.helpers.db_helper import init_database_connection
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from fastapi.responses import JSONResponse
from app.helpers.config_helper import props
import os

router = APIRouter()

app.set_logger_name(__name__)

# Load environment variables from .env file
load_dotenv()


@router.get("/data/{start_time}/{end_time}/{aggregation}")
def get_data(start_time: datetime, end_time: datetime, aggregation: str):
    try:
        print(
            f"Received request: start_time={start_time}, end_time={end_time}, interval={aggregation}")
        # Initialize the InfluxDB client using the database connection function
        connection = init_database_connection()

        # Retrieve the db_bucket from the connection dictionary
        db_bucket = props.get_properties("database", "db_name")
        org = props.get_influx_org()

        # Convert the time range to RFC3339 format
        start_time_rfc3339 = start_time.isoformat() + "Z"
        end_time_rfc3339 = end_time.isoformat() + "Z"

        # Fetch data from the measurement within the specified time range and aggregation
        query_api = connection.query_api()
        query = (
            f'from(bucket: "{db_bucket}") '  # Use db_bucket directly
            f'|> range(start: {start_time_rfc3339}, stop: {end_time_rfc3339}) '
            f'|> filter(fn: (r) => r["_measurement"] == "dataset_tt") '
            f'|> aggregateWindow(every: {aggregation}, fn: mean, createEmpty: false)'
        )

        # Access the InfluxDBClient from the connection dictionary
        result = query_api.query(org=org, query=query)

        # Extract the data from the query result
        data = []
        i = 1
        for table in result:
            for record in table.records:
                data.append({
                    "id": i,
                    "_point": f" Point {i}",
                    "_value": record.values["_value"],
                    "_time": record.values["_time"],
                })
                i += 1
        response_data = {"data": data}

        return response_data

    except Exception as e:
        app.log.error(f"Error occurred: {e}")
