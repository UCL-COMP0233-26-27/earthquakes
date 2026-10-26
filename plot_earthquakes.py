
from collections import Counter
from datetime import datetime, timezone

import matplotlib.pyplot as plt

from earthquakes import get_data


def get_year(earthquake):
    timestamp = earthquake["properties"]["time"]
    return datetime.fromtimestamp(
        timestamp / 1000, tz=timezone.utc
    ).year


def plot_number_per_year(earthquakes):
    counts = Counter(get_year(eq) for eq in earthquakes)

    years = list(range(2000, 2019))
    numbers = [counts.get(year, 0) for year in years]

    plt.figure(figsize=(10, 5))
    plt.bar(years, numbers)

    plt.xlabel("Year")
    plt.ylabel("Number of earthquakes")
    plt.title("Earthquakes per year")
    plt.xticks(years, rotation=45)
    plt.tight_layout()

    plt.savefig("earthquakes_per_year.png", dpi=150)
    plt.show()


def plot_average_magnitude_per_year(earthquakes):
    magnitudes = {}

    for eq in earthquakes:
        year = get_year(eq)
        magnitude = eq["properties"]["mag"]

        if magnitude is not None:
            if year not in magnitudes:
                magnitudes[year] = []
            magnitudes[year].append(magnitude)

    years = sorted(magnitudes)
    averages = [
        sum(magnitudes[year]) / len(magnitudes[year])
        for year in years
    ]

    plt.figure(figsize=(10, 5))
    plt.plot(years, averages, marker="o")

    plt.xlabel("Year")
    plt.ylabel("Average magnitude")
    plt.title("Average earthquake magnitude per year")
    plt.xticks(range(2000, 2019), rotation=45)
    plt.tight_layout()

    plt.savefig("average_magnitude_per_year.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    data = get_data()

    plot_number_per_year(data["features"])
    plot_average_magnitude_per_year(data["features"])
