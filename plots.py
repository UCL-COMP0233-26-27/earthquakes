import json
import matplotlib.pyplot as plt
from datetime import date,datetime
import pandas as pd

import numpy as np
from matplotlib.ticker import MaxNLocator


def data_pull():
    with open("earthquakes.json") as f:
        raw_data = json.load(f)
    return raw_data


raw_data = data_pull()
earthquakes = []

for quake in raw_data["features"]:
    properties = quake["properties"]
    location = properties["place"]
    date = datetime.fromtimestamp(properties["time"] / 1000).year
    magnitude = properties["mag"]
    earthquakes.append([location, date, magnitude])

earthquakes = pd.DataFrame(earthquakes)

def plot_magnitude(earthquakes):
    mag_mean = earthquakes[2].groupby(by=earthquakes[1]).mean()
    plt.bar(mag_mean.index, mag_mean.values)
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.xticks(mag_mean.index,rotation=90)
    plt.title("Yearly Average Magnitude for Atlantic Earthquakes")
    plt.show()

def plot_frequency(earthquakes):
    freq = earthquakes[2].groupby(by=earthquakes[1]).count()
    plt.bar(freq.index, freq.values)
    plt.xlabel("Year")
    plt.ylabel("Frequency")
    plt.xticks(freq.index,rotation=90)
    plt.title("Yearly Frequency for Atlantic Earthquakes")
    plt.show()

plot_magnitude(earthquakes)
plot_frequency(earthquakes)