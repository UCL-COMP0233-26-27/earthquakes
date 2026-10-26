from datetime import datetime, timezone
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from earthquakes import get_data, get_magnitude


def get_year(earthquake: dict) -> int:
    """Get the year of an earthquake."""
    timestamp = earthquake["properties"]["time"] / 1000
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).year


def get_years(data: dict) -> list[int]:
    """Get the years of all earthquakes."""
    return [get_year(e) for e in data["features"]]


def get_avg_magnitudes(data: dict) -> dict[int, float]:
    """Get average magnitude for each year."""
    totals = defaultdict(float)
    counts = defaultdict(int)

    for e in data["features"]:
        magnitude = get_magnitude(e)
        if magnitude is not None:
            year = get_year(e)
            totals[year] += magnitude
            counts[year] += 1

    return {year: totals[year] / counts[year] for year in totals}


def plot_frequency(years: list[int]) -> None:
    """Plot yearly earthquake counts."""
    frequency = Counter(years)
    plt.figure(figsize=(8, 5))
    plt.bar(frequency.keys(), frequency.values())
    plt.xlabel("Year")
    plt.ylabel("Number of earthquakes")
    plt.title("Earthquake Frequency per Year")
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()


def plot_avg_magnitudes(averages: dict[int, float]) -> None:
    """Plot yearly average magnitudes."""
    plt.figure(figsize=(8, 5))
    plt.plot(averages.keys(), averages.values(), marker="o")
    plt.xlabel("Year")
    plt.ylabel("Average magnitude")
    plt.title("Average Earthquake Magnitude per Year")
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = get_data()
    plot_frequency(get_years(data))
    plot_avg_magnitudes(get_avg_magnitudes(data))