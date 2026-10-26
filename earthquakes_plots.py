"""Plot annual earthquake counts and mean magnitudes from the USGS dataset.

This script reuses get_data() from the companion earthquakes.py exercise.
Before importing, ensure earthquakes.py places its command-line output inside
an `if __name__ == "__main__":` block so imports do not fetch data twice.
"""

from datetime import datetime, timezone
from pathlib import Path
import math

import matplotlib.pyplot as plt

from earthquakes import get_data


def calculate_yearly_statistics(data):
    """Count earthquakes and accumulate valid magnitudes for each UTC year."""
    yearly = {}

    for earthquake in data["features"]:
        properties = earthquake["properties"]
        timestamp_ms = properties.get("time")
        if timestamp_ms is None:
            continue  # An event without a time cannot be assigned to a year.

        # USGS GeoJSON timestamps are milliseconds since the Unix epoch.
        year = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).year

        if year not in yearly:
            yearly[year] = {"count": 0, "magnitude_sum": 0.0, "magnitude_count": 0}

        yearly[year]["count"] += 1

        magnitude = properties.get("mag")
        if isinstance(magnitude, (int, float)) and math.isfinite(magnitude):
            yearly[year]["magnitude_sum"] += magnitude
            yearly[year]["magnitude_count"] += 1

    return yearly


def plot_counts(yearly, output_dir):
    """Save a bar chart showing the number of earthquakes in each year."""
    years = sorted(yearly)
    counts = [yearly[year]["count"] for year in years]

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(years, counts, label="Earthquake count")
    ax.set_title("Number of Earthquakes per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of earthquakes")
    ax.set_xticks(years)
    ax.tick_params(axis="x", labelrotation=45)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "earthquakes_per_year.png", dpi=200)
    plt.close(fig)


def plot_average_magnitude(yearly, output_dir):
    """Save a line chart of mean magnitude by year, excluding missing values."""
    years = sorted(year for year, stats in yearly.items() if stats["magnitude_count"] > 0)
    means = [yearly[year]["magnitude_sum"] / yearly[year]["magnitude_count"] for year in years]

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(years, means, marker="o", label="Mean magnitude")
    ax.set_title("Average Earthquake Magnitude per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average magnitude")
    ax.set_xticks(years)
    ax.tick_params(axis="x", labelrotation=45)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "average_magnitude_per_year.png", dpi=200)
    plt.close(fig)


def main():
    data = get_data()
    yearly = calculate_yearly_statistics(data)
    if not yearly:
        raise ValueError("No earthquake events with valid timestamps were returned.")

    output_dir = Path("plots")
    output_dir.mkdir(exist_ok=True)
    plot_counts(yearly, output_dir)
    plot_average_magnitude(yearly, output_dir)

    print(f"Analysed {sum(stats['count'] for stats in yearly.values())} earthquake events.")
    print(f"Created {output_dir / 'earthquakes_per_year.png'}")
    print(f"Created {output_dir / 'average_magnitude_per_year.png'}")


if __name__ == "__main__":
    main()
