# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import json
from pathlib import Path

import requests

# Some 'utility' functions we've written can be imported for us to use here.
# We put these in another file because they're not super relevant to the
# actual analysis that we want to do here.
from _utils import Earthquake, EQDataset, read_cli_args


def get_data(save: Path | None = None) -> EQDataset:
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            "starttime": "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc",
        },
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    # NOTE: It is a JSON file.

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    json_obj = json.loads(text)
    if save is not None:
        with save.open("w") as f:
            json.dump(json_obj, f)

    return json.loads(text)


def count_earthquakes(data: EQDataset) -> int:
    """Get the total number of earthquakes in the response.

    The 'features' key is a list of dictionaries, with each list
    entry corresponding to a single earthquake. However, the
    'metadata' key also provides the answer as a single number.
    """
    # return len(data["features"])
    # would also work here.
    return data["metadata"]["count"]


def get_magnitude(earthquake: Earthquake) -> float:
    """Retrieve the magnitude of an earthquake item.

    An earthquake item is a single entry in `data["features"]`.
    The magnitude is found under the properties -> mag key.
    """
    return earthquake["properties"]["mag"]


def get_location(earthquake: Earthquake) -> list[float]:
    """Retrieve the latitude and longitude of an earthquake item.

    An earthquake item is a single entry in `data["features"]`.
    The lat / long coords are found under the geometry -> coordinates key.
    """
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake["geometry"]["coordinates"][:2]


def get_maximum(data: EQDataset) -> tuple[float, list[float]]:
    """Get the magnitude and location of the strongest earthquake in the data.

    This can be efficiently done using our methods above.
    - First, sort the earthquake entries by magnitude. The strongest earthquake
      will appear at the end of the resulting list.
    - Extract this earthquake, and use `get_magnitude` and `get_location` to
      return the required information.
    """
    sorted_by_mag = sorted(data["features"], key=get_magnitude)
    strongest_earthquake = sorted_by_mag[-1]
    return get_magnitude(strongest_earthquake), get_location(strongest_earthquake)


########################### issue 12 code start ##########################################

from datetime import datetime, timezone
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# plot: the frequency (number) of earthquakes per year

def get_year(earthquake: Earthquake) -> int:
    timestamp = earthquake["properties"]["time"]

    date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
    # timestamp returns ms
    year = date.year
    return year

def count_by_year(data: EQDataset) -> dict[int, int]:
    yearly_counts = defaultdict(int)
    # defaultdict: when visit an nonexistent key, automatically create the key, value = 0

    for earthquake in data["features"]:
        year = get_year(earthquake)
        yearly_counts[year] += 1

    yearly_counts = dict(sorted(yearly_counts.items()))
    return yearly_counts

def average_magnitude_by_year(data: EQDataset) -> dict[int, float]:
    # magnitude量级
    magnitude_totals_yearly = defaultdict(float)
    yearly_counts = defaultdict(int)

    for earthquake in data["features"]:
        magnitude = get_magnitude(earthquake)

        if magnitude is None:
            continue
        
        year = get_year(earthquake)
        magnitude_totals_yearly[year] += magnitude
        yearly_counts[year] += 1
    yearly_counts = dict(sorted(yearly_counts.items()))
    magnitude_totals_yearly = dict(sorted(magnitude_totals_yearly.items()))

    yearly_average = {}
    for year in yearly_counts:
        yearly_average[year] = (magnitude_totals_yearly[year] / yearly_counts[year])
    
    return yearly_average

def plot_earthquake_frequency(data: EQDataset) -> None:
    """Plot the number of earthquakes per year."""
    yearly_counts = count_by_year(data)

    years = list(yearly_counts.keys())
    counts = list(yearly_counts.values())

    plt.figure()
    plt.bar(years, counts)

    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.title("Earthquake Frequency per Year")

    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    plt.savefig("./earthquake_frequency.png", dpi=300)
    # plt.show()


def plot_average_magnitude(data: EQDataset) -> None:
    """Plot the average earthquake magnitude per year."""
    yearly_averages = average_magnitude_by_year(data)

    years = list(yearly_averages.keys())
    averages = list(yearly_averages.values())

    plt.figure()
    plt.plot(years, averages, marker="o")

    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.title("Average Earthquake Magnitude per Year")

    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    plt.savefig("./average_magnitude.png", dpi=300)
    # plt.show()


########################### issue 12 code end ##########################################

# With all the above functions defined, we can now call them and get the result
if __name__ == "__main__":
    args = read_cli_args()

    data = get_data(args.save)
    print(f"Loaded {count_earthquakes(data)}")

    max_magnitude, max_location = get_maximum(data)
    print(
        f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}"
    )

    plot_earthquake_frequency(data)
    plot_average_magnitude(data)
