import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import requests


YEARS = list(range(2000, 2019))
DATA_FILE = Path(__file__).with_name("earthquakes.json")
PLOT_DIR = Path(__file__).with_name("plots")


def get_data():
    """Read the saved data, or download it from USGS."""
    if DATA_FILE.exists():
        with DATA_FILE.open(encoding="utf-8") as f:
            return json.load(f)

    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query",
        params={
            "format": "geojson",
            "starttime": "2000-01-01",
            "endtime": "2018-10-11",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "orderby": "time-asc",
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return data


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake["properties"]["time"]

    # Convert milliseconds to seconds and use UTC.
    return datetime.fromtimestamp(
        timestamp / 1000, tz=timezone.utc
    ).year


def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_magnitudes_per_year(earthquakes):
    """Return a dictionary of years and lists of magnitudes."""
    magnitudes_per_year = {year: [] for year in YEARS}

    for earthquake in earthquakes:
        year = get_year(earthquake)
        magnitude = get_magnitude(earthquake)

        if magnitude is not None:
            magnitudes_per_year[year].append(magnitude)

    return magnitudes_per_year


def plot_average_magnitude_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    averages = []

    for year in YEARS:
        magnitudes = magnitudes_per_year[year]

        if magnitudes:
            averages.append(sum(magnitudes) / len(magnitudes))
        else:
            # Zero is a plotting placeholder, not a measured mean.
            averages.append(0)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        YEARS,
        averages,
        marker="o",
        color="darkorange",
        linewidth=2,
    )

    ax.set_title("Average earthquake magnitude per year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Mean magnitude")
    ax.set_xticks(YEARS)
    ax.tick_params(axis="x", labelrotation=45)

    # Leave space below zero so the zero markers remain visible.
    ax.set_ylim(bottom=-0.15)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.3)

    fig.text(
        0.5,
        0.02,
        "2018 ends at 11 Oct 00:00 UTC. "
        "Zero is a placeholder for years with no valid magnitudes.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))

    PLOT_DIR.mkdir(exist_ok=True)
    fig.savefig(
        PLOT_DIR / "average_magnitude_per_year.png",
        dpi=200,
    )


def plot_number_per_year(earthquakes):
    counts_per_year = {year: 0 for year in YEARS}

    for earthquake in earthquakes:
        year = get_year(earthquake)
        counts_per_year[year] += 1

    counts = [counts_per_year[year] for year in YEARS]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        YEARS,
        counts,
        color="steelblue",
        width=0.75,
    )

    ax.set_title("Number of earthquakes per year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of earthquakes")
    ax.set_xticks(YEARS)
    ax.tick_params(axis="x", labelrotation=45)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, max(max(counts), 1) * 1.15)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.3)

    for year, count in zip(YEARS, counts):
        ax.text(
            year,
            count + 0.25,
            str(count),
            ha="center",
            fontsize=9,
        )

    fig.text(
        0.5,
        0.02,
        "2018 data end at 11 Oct 00:00 UTC.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))

    PLOT_DIR.mkdir(exist_ok=True)
    fig.savefig(
        PLOT_DIR / "number_per_year.png",
        dpi=200,
    )


if __name__ == "__main__":
    quakes = get_data()["features"]
    print(f"Loaded {len(quakes)} earthquakes")

    plot_number_per_year(quakes)
    plot_average_magnitude_per_year(quakes)

    print(f"Saved both plots in: {PLOT_DIR}")
    plt.show()
