from datetime import datetime, timezone
from pathlib import Path

import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


START_DATE = "2000-01-01"
END_DATE = "2018-10-11"

YEARS = list(range(int(START_DATE[:4]), int(END_DATE[:4]) + 1))
OUTPUT_DIR = Path(__file__).resolve().parent / "plots"


def get_data():
    """Retrieve earthquake data using the exercise's search parameters."""
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            "starttime": START_DATE,
            "endtime": END_DATE,
            "minlatitude": 50.008,
            "maxlatitude": 58.723,
            "minlongitude": -9.756,
            "maxlongitude": 1.67,
            "minmagnitude": 1,
            "orderby": "time-asc",
        },
        timeout=60,
    )

    response.raise_for_status()
    return response.json()


def get_year(earthquake):
    """Extract the earthquake's year in UTC."""
    timestamp = earthquake["properties"]["time"]

    # USGS uses milliseconds; Python expects seconds.
    return datetime.fromtimestamp(
        timestamp / 1000,
        tz=timezone.utc,
    ).year


def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_magnitudes_per_year(earthquakes):
    """Return years as keys and lists of available magnitudes as values."""
    magnitudes_per_year = {year: [] for year in YEARS}

    for earthquake in earthquakes:
        year = get_year(earthquake)
        magnitude = get_magnitude(earthquake)

        # Exclude missing magnitudes from the average.
        if magnitude is not None:
            magnitudes_per_year[year].append(magnitude)

    return magnitudes_per_year


def save_plot(fig, ax, filename):
    """Format and save a figure in the plots folder."""
    ax.set_xlabel("Year (UTC)")
    ax.set_xticks(YEARS)
    ax.tick_params(axis="x", labelrotation=45)
    ax.set_xlim(YEARS[0] - 0.7, YEARS[-1] + 0.7)

    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    fig.text(
        0.5,
        0.02,
        f"Query: {START_DATE} to {END_DATE} (UTC); magnitude >= 1. "
        "2018 is a partial year.",
        ha="center",
        fontsize=9,
    )

    fig.tight_layout(rect=(0, 0.07, 1, 1))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename

    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    print("Saved:", output_path)


def plot_average_magnitude_per_year(earthquakes):
    """Plot the arithmetic mean of available magnitudes for each year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    averages = []

    for year in YEARS:
        magnitudes = magnitudes_per_year[year]

        if magnitudes:
            average = sum(magnitudes) / len(magnitudes)
        else:
            # An undefined average is shown as a gap, not zero.
            average = float("nan")

        averages.append(average)

    fig, ax = plt.subplots(figsize=(10, 5.5))

    ax.plot(
        YEARS,
        averages,
        marker="o",
        color="darkorange",
    )

    ax.set_title(
        "Average Earthquake Magnitude per Year\n"
        "Exercise search region"
    )
    ax.set_ylabel("Average magnitude")

    save_plot(fig, ax, "average_magnitude_per_year.png")
    return fig


def plot_number_per_year(earthquakes):
    """Plot the number of earthquake records for every year."""
    counts = {year: 0 for year in YEARS}

    # Count all records, including those with a missing magnitude.
    for earthquake in earthquakes:
        year = get_year(earthquake)
        counts[year] += 1

    fig, ax = plt.subplots(figsize=(10, 5.5))

    ax.bar(
        YEARS,
        [counts[year] for year in YEARS],
        color="steelblue",
    )

    ax.set_title(
        "Number of Earthquakes per Year\n"
        "Exercise search region"
    )
    ax.set_ylabel("Number of earthquakes")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    save_plot(fig, ax, "number_of_earthquakes_per_year.png")
    return fig


if __name__ == "__main__":
    quakes = get_data()["features"]

    if not quakes:
        raise ValueError(
            "No earthquakes were returned. Check the query parameters."
        )

    print("Number of earthquakes:", len(quakes))
    print("Query period:", START_DATE, "to", END_DATE, "(UTC)")
    print("Note: 2018 is a partial year.")

    plot_number_per_year(quakes)
    plot_average_magnitude_per_year(quakes)

    plt.show()