from datetime import date

import matplotlib.pyplot as plt

from earthquakes import get_data, get_magnitude

# def get_data():
#     """Retrieve the data we will be working with."""
#     ...


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


# def get_magnitude(earthquake):
#     """Retrive the magnitude of an earthquake item."""
#     ...


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_year = {}
    for eq in earthquakes:
        year = get_year(eq)
        magnitude = get_magnitude(eq)
        magnitudes_year.setdefault(year, []).append(magnitude)
    return magnitudes_year
    ...


def plot_average_magnitude_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())
    average_magnitudes = [sum(magnitudes_per_year[year]) / len(magnitudes_per_year[year]) for year in years]
    fig, ax = plt.subplots()
    ax.plot(years, average_magnitudes)
    ax.set(xlabel="Year",ylabel="Average Magnitude",title="Average Magnitude of Earthquakes per Year", )
    return fig


def plot_number_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())
    number_per_year = [len(magnitudes_per_year[year]) for year in years]
    fig, ax = plt.subplots()
    ax.plot(years, number_per_year, marker="o")
    ax.set(xlabel="Year",ylabel="Number of Earthquakes",title="Number of Earthquakes per Year",)
    return fig
    



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
# plot_number_per_year(quakes)
# plt.clf()  # This clears the figure, so that we don't overlay the two plots
# plot_average_magnitude_per_year(quakes)
count_fig = plot_number_per_year(quakes)
average_fig = plot_average_magnitude_per_year(quakes)

count_fig.savefig("number_per_year.png")
average_fig.savefig("average_magnitude_per_year.png")

plt.show()