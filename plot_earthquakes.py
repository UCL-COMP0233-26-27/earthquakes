from earthquakes import get_data, get_magnitude
from datetime import date
import matplotlib.pyplot as plt

def get_year(earthquake):
    timestamp = earthquake["properties"]["time"]
    year = date.fromtimestamp(timestamp / 1000).year
    return year

quakes = get_data()["features"]

years = [get_year(earthquake) for earthquake in quakes]

plot_years = list(range(2000, 2019))
counts = {year: years.count(year) for year in plot_years}

averages = {}
for year in plot_years:
    magnitudes = [
        get_magnitude(earthquake)
        for earthquake in quakes
        if get_year(earthquake) == year
    ]
    if magnitudes:
        averages[year] = sum(magnitudes) / len(magnitudes)

    else:
        averages[year] = float("nan")  # or some other value to indicate no data

print(averages)

print(years)
print(get_year(quakes[0]))
print(plot_years)
print(counts)

plt.bar(counts.keys(), counts.values())

plt.xlabel("Year")
plt.ylabel("Number of earthquakes")
plt.title("Earthquakes per year")

plt.xticks(plot_years, rotation=45)
plt.yticks(range(0, max(counts.values()) + 5, 5))
plt.tight_layout()
plt.savefig("earthquakes_per_year.png")

plt.figure()

plt.plot(averages.keys(), averages.values(), marker="o")

plt.xlabel("Year")
plt.ylabel("Average magnitude")
plt.title("Average earthquake magnitude per year")

plt.xticks(plot_years, rotation=45)
plt.tight_layout()
plt.savefig("average_magnitude_per_year.png")

plt.show()