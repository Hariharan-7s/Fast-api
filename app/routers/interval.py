import os
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.helpers.log_helper import app
from app.helpers.db_helper import init_database_connection
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
# Load environment variables from .env file
from fastapi.responses import JSONResponse
#from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

import io
from minio import Minio
from minio.error import S3Error
import io
import pandas as pd
from pydantic import BaseModel  # Make sure to include this import

from app.routers.setinflux import csv_to_influxdb
from app.helpers.config_helper import props
from app.helpers.db_helper import init_minio_connection
router = APIRouter()
app.set_logger_name(__name__)
load_dotenv()


class MinioEventPayload(BaseModel):
    EventName: str
    Key: str
    Records: list


@router.get("/download-mino")
async def download_bucket_object():
    try:
        influx_client = init_database_connection()
        minio_client = init_minio_connection()
        bucket_name = props.get_minio_bucket()
        object_name = props.get_minio_object()
        # Read the object
        obj = minio_client.get_object(bucket_name, object_name)
        object_data = obj.read()
        print(type(object_data))
        df = pd.read_csv(io.BytesIO(object_data))
        print(df)
        # await process_1_hour_data(df)
        #csv_to_influxdb(df, influx_client)

        # read_minio_object(influx_client=influx_client)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/download")
async def download_bucket_object(payload: MinioEventPayload):

    #local_file_path = f"D:\\Anomaly\\Anomaly-detection\\{object_name}"
    try:
        influx_client = init_database_connection()
        minio_client = init_minio_connection()
        object_name = payload.Key
        bucket_name = "dev"
        object_name = object_name[4:]
        obj = minio_client.get_object(bucket_name, object_name)
        object_data = obj.read()
        print(type(object_data))
        df = pd.read_csv(io.BytesIO(object_data))
        print(df)
        csv_to_influxdb(df, influx_client)
        # read_minio_object(bucket_name,object_name,influx_client=influx_client)
        # Call perform_insertdata with the file path
        # perform_insertdata(file_path=local_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
@router.get("model/hour")
async def process_1_hour_data(df):

    print("Processing 1-hour data...")
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    earliest_timestamp = df['timestamp'].min()
    # Use the actual datetime objects
    latest_timestamp = df['timestamp'].max()
    time_difference = latest_timestamp - earliest_timestamp
    print("Time difference:", time_difference)
    print(earliest_timestamp)
    print(latest_timestamp)
    print('--------------------')
    values = df['value']
    data_values = np.array(values)
    print(data_values)
    # Compare the time difference with 24 hours
    if time_difference >= timedelta(hours=24):
        print("24 hours of data is complete.")
        # process_1_day_data(time_difference)
"""
