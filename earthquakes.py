# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests

# importing json so that i am able to view the data
# had to edit the format so that i could see all of the data clearly
import json

# datetime converts the timestamps into dates, matplotlib draws the graphs
import datetime
import matplotlib.pyplot as plt

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

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    with open("earthquakes.json", "w") as f:
        f.write(text)
    data = json.loads(text)
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return data

# look at the .json file to find where the sepcific data is stored
def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake["geometry"]["coordinates"][:2]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    # sort the data by magnitude (the strngest earthquake will be at the end) then extract
    sorted_by_mag = sorted(data["features"], key=get_magnitude)
    strongest_earthquake = sorted_by_mag[-1]
    return get_magnitude(strongest_earthquake), get_location(strongest_earthquake)


# With all the above functions defined, we can now call them and get the result
data = get_data()

# have to define the data in the functions before print
print(f"Loaded {count_earthquakes(data)}")
print(get_magnitude(data["features"][0])) #0 as first set of datain .json file
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

def get_year(earthquake: Earthquake) -> float:
    """Given the earthquake, extract the year it occured in"""
    timestamp = earthquake["properties"]["time"]
# we need to convert the timestamp into year - in need of another function
    earthquake_date = datetime.date.fromtimestamp(timestamp)
    return earthquake_date.year

def plot_n_earthquakes_per_year(data):
    # for each year, get the number of earthquakes
    # for each earthquake, get th eyear it occured in 
    # for each year, sum up the number of earthquakes you found 

    earthquake_per_year = []
    date_years = list(range(2000, 2019))
    for year in date_years:
        earthquakes_this_year = 0
        for earthquake in data["features"]:
            year_of_eq = get_year(earthquake)
            if year_of_eq == year:
                earthquakes_this_year += 1
                earthquake_per_year.append(earthquakes_this_year)

   