"""
Main script to initialize logger and server
"""
import minio
from fastapi import Query
import os
from minio import Minio
import uvicorn


from fastapi import FastAPI, status, Response, Depends, HTTPException
from fastapi.responses import StreamingResponse
from influxdb_client import InfluxDBClient
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.helpers.config_helper import props
from app.routers.interval import router as int_router
from app.routers.data import router as ret_router


__author__ = "Dinesh Sinnarasse"
__copyright__ = "Copyright 2023, Enterprise Minds"
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Enterprise Minds"
__status__ = "Development"


def get_application() -> FastAPI:
    """
    Initialize the application server with logger
    :return: fastApi app
    """
    application = FastAPI(title="Anomaly-detection", debug=True)
    return application


app = get_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(int_router)
app.include_router(ret_router)


@app.get('healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {'healthcheck': 'Everything OK!'}


"""
@app.get("/getdata", status_code=status.HTTP_200_OK)
async def get_datafrom_influx():
    try:

        retrive_from_influx()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

if __name__ == "__main__":
    # Read server connection details
    host = props.get_properties("connection", "host")
    port = props.get_properties("connection", "port")

    uvicorn.run(app, host=host, port=int(port))
