# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
from pathlib import Path
import datetime
def get_data(save:Path | None = None):
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

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    with open("response.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?

    with open("response.txt", "r", encoding="utf-8") as f:
        loaded = json.load(f)

    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(loaded, f, indent=4)

    with open("response.json", "r", encoding="utf-8") as f:
        text = f.read()
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
    # There are three coordinates, but we don't care about the third (altitude)

    return (earthquake["geometry"]["coordinates"][0], earthquake["geometry"]["coordinates"][1])


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    index = 0
    earthquake_information = data["features"]
    mag = 0
    location = None
    for i in earthquake_information:
        if get_magnitude(i) > mag:
            mag = get_magnitude(i)
            location = get_location(i)
            index = i
    return mag, location

def get_frequency(data, year):
    """Get the frequency of earthquakes in a given year."""
    count = 0
    for earthquake in data["features"]:
        time = earthquake["properties"]["time"]
        date = datetime.datetime.fromtimestamp(time / 1000)
        if date.year == year:
            count += 1
    return count

def get_average_mag(data, year):
    """Get the average magnitude of earthquakes in a given year."""
    count = 0
    total_magnitude = 0
    for earthquake in data["features"]:
        time = earthquake["properties"]["time"]
        date = datetime.datetime.fromtimestamp(time / 1000)
        if date.year == year:
            count += 1
            total_magnitude += get_magnitude(earthquake)
    if count == 0:
        return 0
    return round(total_magnitude / count, 2)

# With all the above functions defined, we can now call them and get the result
data = get_data()
print(type(data))
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

frequency = [[x, get_frequency(data, x)] for x in range(2000, 2019)]
average_magnitude = [[x, get_average_mag(data, x)] for x in range(2000, 2019)]
frequency_average_mag = [[x, get_frequency(data, x), get_average_mag(data, x)] for x in range(2000, 2019)]
print(f"Frequency and average magnitude of earthquakes by year: {frequency_average_mag}")

import matplotlib.pyplot as plt

# # Plot the frequency of earthquakes by year
# years = [x[0] for x in frequency]
# frequencies = [x[1] for x in frequency]
# plt.plot(years, frequencies, marker='o')
# plt.xlabel('Year')
# plt.ylabel('Frequency')
# plt.title('Frequency of Earthquakes by Year')
# plt.show()

# # Plot the average magnitude of earthquakes by year
# years = [x[0] for x in frequency]
# plt.plot(years, average_magnitudes, marker='o')
# plt.xlabel('Year')
# plt.ylabel('Average Magnitude')
# plt.title('Average Magnitude of Earthquakes by Year')
# plt.show()

years = [x[0] for x in frequency]
frequencies = [x[1] for x in frequency]
average_magnitudes = [x[1] for x in average_magnitude]
fig = plt.figure(figsize=(12, 6))
fig.add_subplot(1, 2, 1)
plt.plot(years, frequencies, marker='o')
plt.xlabel('Year')
plt.ylabel('Frequency')
plt.title('Frequency of Earthquakes by Year')
fig.add_subplot(1, 2, 2)
plt.plot(years, average_magnitudes, marker='o')
plt.xlabel('Year')
plt.ylabel('Average Magnitude')
plt.title('Average Magnitude of Earthquakes by Year')
plt.show()