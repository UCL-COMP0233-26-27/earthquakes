import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import requests


def get_data():
    """Read local earthquake data, or download it if needed."""
    data_file = Path(__file__).with_name("earthquakes.json")

    if data_file.exists():
        with data_file.open("r", encoding="utf-8") as file:
            return json.load(file)

    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            "starttime": "2000-01-01",
            "endtime": "2018-10-11",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "orderby": "time-asc",
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    with data_file.open("w", encoding="utf-8") as file:
        json.dump(data, file)

    return data


def get_year(earthquake):
    """Extract the year of an earthquake."""
    timestamp = earthquake["properties"]["time"]
    return datetime.fromtimestamp(
        timestamp / 1000, tz=timezone.utc
    ).year


def get_magnitude(earthquake):
    """Extract the magnitude of an earthquake."""
    return earthquake["properties"]["mag"]


def get_magnitudes_per_year(earthquakes):
    """Group earthquake magnitudes by year."""
    magnitudes_per_year = {}

    for earthquake in earthquakes:
        year = get_year(earthquake)
        magnitude = get_magnitude(earthquake)

        if year not in magnitudes_per_year:
            magnitudes_per_year[year] = []

        magnitudes_per_year[year].append(magnitude)

    return magnitudes_per_year


def plot_number_per_year(magnitudes_per_year):
    """Plot the number of earthquakes in each year."""
    observed_years = sorted(magnitudes_per_year)
    years = list(range(observed_years[0], observed_years[-1] + 1))

    counts = [
        len(magnitudes_per_year.get(year, []))
        for year in years
    ]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(years, counts)

    ax.set_xlabel("Year")
    ax.set_ylabel("Number of earthquakes")
    ax.set_title("Earthquakes per year in the selected dataset")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    fig.tight_layout()
    fig.savefig(
        Path(__file__).with_name("earthquake_counts.png"),
        dpi=200,
    )
    plt.show()
    plt.close(fig)


def plot_average_magnitude_per_year(magnitudes_per_year):
    """Plot the average earthquake magnitude in each year."""
    years = []
    averages = []

    for year in sorted(magnitudes_per_year):
        magnitudes = [
            magnitude
            for magnitude in magnitudes_per_year[year]
            if magnitude is not None
        ]

        if magnitudes:
            years.append(year)
            averages.append(sum(magnitudes) / len(magnitudes))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(years, averages, "o-")

    ax.set_xlabel("Year")
    ax.set_ylabel("Average magnitude")
    ax.set_title("Average earthquake magnitude per year")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(
        Path(__file__).with_name("earthquake_average_magnitude.png"),
        dpi=200,
    )
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    data = get_data()
    earthquakes = data["features"]

    if not earthquakes:
        raise ValueError("The dataset contains no earthquakes.")

    magnitudes_per_year = get_magnitudes_per_year(earthquakes)

    plot_number_per_year(magnitudes_per_year)
    plot_average_magnitude_per_year(magnitudes_per_year)