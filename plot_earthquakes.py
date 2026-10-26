from datetime import datetime, timezone

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

from earthquakes import get_data, get_magnitude


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in milliseconds since the Unix epoch (1970-01-01 UTC):
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Python's timestamps are in seconds, so we divide by 1000.
    # We use UTC so that the result doesn't depend on the local time zone.
    return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).year


def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.

    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes = {}
    for earthquake in earthquakes:
        magnitudes.setdefault(get_year(earthquake), []).append(get_magnitude(earthquake))
    return magnitudes


def plot_number_per_year(earthquakes):
    """Plot a bar chart of the number of earthquakes in each year."""
    found_years, found_counts = np.unique([get_year(quake) for quake in earthquakes], return_counts=True)
    # Include years with no earthquakes, so they show up as zero
    years = np.arange(found_years.min(), found_years.max() + 1)
    counts = np.zeros_like(years)
    counts[found_years - years[0]] = found_counts
    plt.bar(years, counts)
    plt.xticks(years, rotation=45)
    plt.xlabel("Year")
    plt.ylabel("Number of earthquakes")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title("UK earthquakes (magnitude ≥ 1) per year")
    plt.tight_layout()
    plt.savefig("number_per_year.png")


def plot_average_magnitude_per_year(earthquakes):
    """Plot the average magnitude of the earthquakes in each year."""
    magnitudes = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes)
    averages = [np.mean(magnitudes[year]) for year in years]
    plt.plot(years, averages, marker="o")
    # Label every year, including those with no earthquakes (and so no average)
    plt.xticks(range(years[0], years[-1] + 1), rotation=45)
    plt.xlabel("Year")
    plt.ylabel("Average magnitude")
    plt.title("Average magnitude of UK earthquakes per year")
    plt.tight_layout()
    plt.savefig("average_magnitude_per_year.png")


if __name__ == "__main__":
    # Get the data we will work with
    quakes = get_data()['features']

    plot_number_per_year(quakes)
    plt.clf()  # This clears the figure, so that we don't overlay the two plots
    plot_average_magnitude_per_year(quakes)
