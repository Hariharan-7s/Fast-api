from fastapi import FastAPI
#from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
app = FastAPI()

# Initialize the scheduler
#scheduler = BackgroundScheduler()
# scheduler.start()


def process_1_day_data(time_difference):

    print("Processing 1-day data...")

    # Compare the time difference with 7 days
    if time_difference >= timedelta(days=7):
        print("1 week of data is complete.")
        process_1_week_data(time_difference)


def process_1_week_data(time_difference):

    print("Processing 1-week data...")

    # Compare the time difference with 28 days
    if time_difference >= timedelta(days=28):
        print("4 weeks of data is complete.")
        process_1_month_data(time_difference)


def process_1_month_data(time_difference):

    print("Processing 1-month data...")

    # Compare the time difference with 365 days (1 year)
    if time_difference >= timedelta(days=365):
        print("1 year of data is complete.")
