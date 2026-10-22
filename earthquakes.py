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

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    # text = response.text # not required
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(response.text)
    
def count_earthquakes(earthquake_data):
    """Get the total number of earthquakes in the response."""
    return len(earthquake_data['features'])


def get_max_magnitude(earthquake_data):
    """Retrive the magnitude of an earthquake item."""
    return max([earthquake_data['features'][n]['properties']['mag'] for n in range(count_earthquakes(earthquake_data))])

def get_max_magnitude(earthquake_data):
    """Retrive the magnitude of an earthquake item."""
    return max([earthquake_data['features'][n]['properties']['mag'] 
                for n in range(count_earthquakes(earthquake_data))])


def get_location(earthquake_no):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    # I have included the place as well, so that it is more readable
    cord1 = earthquake_data['features'][earthquake_no]['geometry']['coordinates'][0]
    cord2 = earthquake_data['features'][earthquake_no]['geometry']['coordinates'][1] 
    place = earthquake_data['features'][earthquake_no]['properties']['place']
    return [cord1, cord2, place]


def get_location(earthquake_no):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    # I have included the place as well, so that it is more readable
    return [earthquake_data['features'][earthquake_no]['geometry']['coordinates'][0], 
            earthquake_data['features'][earthquake_no]['geometry']['coordinates'][1],
            earthquake_data['features'][earthquake_no]['properties']['place'] ]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_magnitude = get_max_magnitude(earthquake_data)
    max_location = []
    for n in range(count_earthquakes(earthquake_data)):
        if earthquake_data['features'][n]['properties']['mag'] == max_magnitude:
            max_location.append(get_location(n))        
    return max_magnitude, max_location


# With all the above functions defined, we can now call them and get the result
earthquake_data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")