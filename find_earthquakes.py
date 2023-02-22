import os
import requests
import logging
import json

import pandas as pd
# import pandas_gbq
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

# Configure logging
logging.basicConfig(
    filename="errors.log",
    format="%(asctime)s - %(message)s",
    level=logging.ERROR
)

USGS_API_URL = os.getenv("USGS_API_URL")
LOCATIONS_FILE_URL = os.getenv("LOCATIONS_FILE_URL")
BQ_TABLE_ID = os.getenv("BQ_TABLE_ID")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")


def fetch_data(location):
    """
    Fetch data from the USGS API
    """

    data = df = None
    year = datetime.today().year

    params = {
        "format": "geojson",
        "starttime": datetime(year, 1, 1).strftime("%Y-%m-%d"),
        "latitude": f"{location['latitude']}",
        "longitude": f"{location['longitude']}",
        "maxradiuskm": "1000"
    }

    try:
        response = requests.get(USGS_API_URL, params=params)
        data = response.json()
    except requests.exceptions.RequestException as err:
        print("Error fetching data")
        logging.error(err)

    # Check if a response was returned
    # and if the "features" key is present in the json response
    # (i.e that there is data available for this location)
    if (data and data["features"]):
        df = pd.json_normalize(data["features"], sep="_")
        df["location_name"] = location["name"]
    return df


def get_earthquakes_by_location():
    """
    Load the locations from a json file and get earthquake data
    for a radius of 1000km around each of them
    """

    # Load locations from json file
    try:
        f = open(LOCATIONS_FILE_URL)
        locations = json.load(f)
        f.close()
    except FileNotFoundError as err:
        logging.error(err)
        print(err)
        return None

    # Fetch earthquake data for each location
    df = pd.DataFrame()
    for location in locations["locations"]:
        df = pd.concat(
            [df, fetch_data(location)], ignore_index=True)

    # Fix data columns and keep only relevant ones
    df["geometry_coordinates"] = pd.eval(
        df["geometry_coordinates"])
    df["longitude"] = df["geometry_coordinates"].apply(
        lambda x: x[0])
    df["latitude"] = df["geometry_coordinates"].apply(
        lambda x: x[1])
    df["properties_time"] = pd.to_datetime(
        df["properties_time"], unit="ms")

    df.rename(columns={
        "properties_time": "datetime", "properties_mag": "magnitude",
        "properties_place": "place"
    }, inplace=True)

    df = df[[
        "id", "datetime", "magnitude", "latitude",
        "longitude", "place", "location_name"
    ]]

    return df


# def insert_to_bigquery(df):
#     """
#     Insert data into a BigQuery table
#     """
#     try:
#         pandas_gbq.to_gbq(df, BQ_TABLE_ID, project_id=GOOGLE_PROJECT_ID,
#                           if_exists="replace", api_method="load_csv")
#     except Exception as e:
#         logging.error(traceback.print_exc())


if __name__ == "__main__":
    earthquake_data = get_earthquakes_by_location()
    if earthquake_data is not None:
        earthquake_data.to_csv("earthquakes.csv")
        # insert_to_bigquery(earthquake_data)
