# Earthquake data exploration

Data checked on 25 October 2026 using the starter query parameters.

## What the request selects

- Dates: 1 January 2000 to 11 October 2018.
- Latitude: 50.008 to 58.723 degrees.
- Longitude: -9.756 to 1.67 degrees.
- Minimum magnitude: 1.
- Order: earliest earthquake first (`time-asc`).

These are the supplied exercise parameters. The geographic filter is a
rectangle around the UK, and the dates do not cover an entire century.

## Structure of the response

The JSON response becomes a Python dictionary with four top-level keys:
`type`, `metadata`, `features`, and `bbox`.

- `metadata["count"]` is 120.
- `features` is a list containing 120 earthquake dictionaries.
- Each earthquake's magnitude is at `earthquake["properties"]["mag"]`.
- A place description is at `earthquake["properties"]["place"]`.
- Coordinates are at `earthquake["geometry"]["coordinates"]`, in the order
  longitude, latitude, depth in kilometres.
- `earthquake["properties"]["time"]` is a Unix timestamp in milliseconds.
  Dividing by 1000 converts it to seconds for Python's datetime functions.

The first earthquake in this time-ordered response has magnitude 2.6 and
place description "12 km NNW of Penrith, United Kingdom". Its coordinates
are `[-2.81, 54.77, 14]`, and its time is `956553055700`, corresponding to
24 April 2000 at 05:10:55.700 UTC.

## Analysis result

- Earthquakes loaded: **120**.
- Maximum magnitude: **4.8**.
- Location returned by the program, as **(latitude, longitude)**:
  **(52.52, -2.15)**.
- Place: **2 km ESE of Wombourn, United Kingdom**.
- Time: **22 September 2002 at 23:53:14.600 UTC**.
- USGS event ID: `usp000bcxg`.

## Running the program

Run `python earthquakes.py` in the `comp0233` environment. The downloaded
response is saved as `earthquake_data.json` beside the script for inspection.
This generated file and local editor settings are excluded from Git.

The count, magnitude lookup, coordinate order, and maximum selection were
also checked using a small example with a known answer.

USGS references:
- https://earthquake.usgs.gov/fdsnws/event/1/
- https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
