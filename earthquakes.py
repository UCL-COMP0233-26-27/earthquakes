# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import json
from pathlib import Path

import requests


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"},
        timeout=30,
    )
    response.raise_for_status()

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    data_file = Path(__file__).with_name("earthquake_data.json")
    data_file.write_text(text, encoding="utf-8")

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data["features"])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # USGS stores longitude, latitude, depth; return latitude, longitude.
    longitude, latitude, depth = earthquake["geometry"]["coordinates"]
    return latitude, longitude


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    # key tells max() to compare earthquakes by magnitude.
    strongest = max(data["features"], key=get_magnitude)
    return get_magnitude(strongest), get_location(strongest)


# With all the above functions defined, we can now call them and get the result
if __name__ == "__main__":
    data = get_data()
    print(f"Loaded {count_earthquakes(data)} earthquakes")
    max_magnitude, max_location = get_maximum(data)
    print(
        f"The strongest earthquake was at latitude/longitude {max_location} "
        f"with magnitude {max_magnitude}"
    )
