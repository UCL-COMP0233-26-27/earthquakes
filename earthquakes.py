import json
import requests


def get_data():
    # Request earthquake data from the USGS web service.
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            "starttime": "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"
        },
        timeout=60
    )

    # Check whether the request was successful.
    response.raise_for_status()

    text = response.text

    # Convert JSON text into a Python dictionary.
    data = json.loads(text)

    return data


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]


def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # Coordinates are [longitude, latitude, depth].
    longitude, latitude, _ = earthquake["geometry"]["coordinates"]

    return latitude, longitude


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake."""
    earthquakes = data["features"]

    # Start by assuming the first earthquake is the strongest.
    largest_so_far = earthquakes[0]

    # Compare each earthquake with the current maximum.
    for earthquake in earthquakes:
        if get_magnitude(earthquake) > get_magnitude(largest_so_far):
            largest_so_far = earthquake

    return get_magnitude(largest_so_far), get_location(largest_so_far)


# Run the analysis.
data = get_data()

print(f"Loaded {count_earthquakes(data)}")

max_magnitude, max_location = get_maximum(data)

print(
    f"The strongest earthquake was at {max_location} "
    f"with magnitude {max_magnitude}"
)
