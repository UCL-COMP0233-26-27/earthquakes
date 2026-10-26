# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    text = response.text
    data = json.loads(text)
    return data


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data["features"])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # coordinates: [longitude, latitude, depth]
    coordinates = earthquake["geometry"]["coordinates"]
    lat = coordinates[1]
    lon = coordinates[0]
    return lat, lon


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_mag = -1.0
    max_pos = None
    for quake in data["features"]:
        mag = get_magnitude(quake)
        if mag > max_mag:
            max_mag = mag
            max_pos = get_location(quake)
    return max_mag, max_pos


# With all the above functions defined, we can now call them and get the result
if __name__ == "__main__":
    data = get_data()
    print(f"Loaded {count_earthquakes(data)} earthquakes")
    max_magnitude, max_location = get_maximum(data)
    print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
