# Earthquake hotspots

## Overview
This project uses the [United States Geological Survey (USGS)](https://earthquake.usgs.gov/fdsnws/event/1/) API to find all recorded earthquakes within 500 km of each of the locations in the `locations.json` file for the year to date. ~~This data is then inserted into a `Google BigQuery` table.~~
## ~~Initial set up before running the project~~
- ~~Set up a project on [Google Cloud](https://console.cloud.google.com/)~~
- ~~Create a `BigQuery` [dataset](https://cloud.google.com/bigquery/docs/datasets) and [table](https://cloud.google.com/bigquery/docs/tables)~~
- ~~Create a service account in order to enable you create a set of credentials for accessing your dataset~~

## How to run the project
- Clone the project: `git clone https://github.com/NLSanyu/earthquake-hotspots.git`
- Within the root project folder, create a virtual environment: `python3 -m virtualenv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the project dependencies: `pip install -r requirements.txt`
- Create a `.env` file and add environment variables as shown in the `.env.example` file. The variables `USGS_API_URL` and `LOCATIONS_FILE_URL` are already provided there because they do not contain senstive data like ids or credentials. Other variables are left to the user of the project to fill in their own ids.
- Run the project: `python find_earthquakes.py`
- ~~Check your BigQuery table for your newly inserted data.~~

## What prerequisites are assumed
- `Python 3` and `pip` installed on your computer
- A Google account and access to Google Cloud

