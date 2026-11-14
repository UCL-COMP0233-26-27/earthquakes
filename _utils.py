"""This file contains some supporting utility functions for the `earthquakes.py` script.

In general, if you are finding that you need to split up your scripts into multiple files
because they're too long, or they use the same individual "pieces" of code, you would
consider writing a package containing the common functionality.
We will see how to do this later in the course (and in the assignment)!.

Since this repository is fairly small, we'll just use a couple of auxiliary files - like
this one - to store our 'helper' functions.
This is mainly so tha the `earthquakes.py` file only contains code that's actually
relevant to what we want to do in the exercises / homework / pre-reading.

This file contains the functionality to have the earthquake data be saved to the local
machine, and also outlines the structure of the data so Python can give typehints.
"""

import argparse
from pathlib import Path
from typing import TypedDict


def read_cli_args() -> argparse.Namespace:
    """Creates the command-line interface for the `earthquakes.py` script,
    and parses the arguments.

    The CLI just adds an option to have the script save the data to a `.json` file
    when it fetches it from the internet.
    """
    parser = argparse.ArgumentParser(
        description="Fetches US geological survey earthquake data from 2000-01-01 to 2018-10-11."
    )
    parser.add_argument("-s", "--save", nargs=1, type=str, default=None)

    args = parser.parse_args()
    if args.save is not None:
        args.save = Path(args.save[0])

    return args


# What follows below is some type-hint setup for interpreting the data.
# The data that we fetch comes in JSON format, which means that Python will
# represent it as a sequence of (possibly nested) dictionaries and lists.
#
# We can optionally choose to inform the Python type-hinter of the data
# structure ahead of time, which can be handy for you when you're writing
# your analysis!
# This is what we're doing below.
# Don't forget that the general structure of the data that we get back from
# the US Geological Survey site has the format:
# {
#   "type": text noting the type of query we sent to the website,
#   "metadata": dictionary of metadata information,
#   "features": list of earthquake objects - each earthquake is a dictionary,
#   "bbox": list of floats defining the bounding box of the earthquake locations
# }
#
# Since the data uses a fixed set of keys, we can use the `TypedDict` class to
# create our type-hints. The `TypedDict` class allows us to create a type-hint
# to tell Python we expect to find a dictionary with a fixed set of keys, which
# tools like VSCode can pick up on to help us write our Python code.
# `TypedDict` is not actually used when we _run_ our Python code, it is just
# scanned by the Python type-hinter to resolve argument types and values!


class EQProperties(TypedDict):
    """The `'properties'` key of a single earthquake entry.

    Note that some fields in the earthquake data we extract always return `None`
    values. This is unlikely to be true of the entire, unfiltered dataset (we
    are only looking at 2000-2018 after all).
    """

    mag: float
    place: str
    time: int
    updated: int
    tz: None
    url: str
    detail: str
    felt: int
    cdi: int
    mmi: float
    alert: None
    status: str
    tsunami: int
    sig: int
    net: str
    code: str
    ids: str
    sources: str
    types: str
    nst: int
    dmin: float
    rms: float
    gap: float
    magType: str
    type: str
    title: str


class EQGeometry(TypedDict):
    """The `'geometry'` key of a single earthquake entry.

    Each earthquake's geometry field consists of its `type`, and the
    coordinates (lat, long, alt) of where it was recorded.
    """

    type: float
    coordinates: list[float]


class Earthquake(TypedDict):
    """How a single earthquake is represented in the dataset.

    Note that we can nest our type-hints to save on a compound definition.
    """

    type: str
    properties: EQProperties
    geometry: EQGeometry
    id: str


class EQMetadata(TypedDict):
    """The `'metadata'` key of the dataset."""

    generated: int
    url: str
    title: str
    status: int
    api: str
    count: int


class EQDataset(TypedDict):
    """The US Geological Survey dataset format."""

    type: str
    metadata: EQMetadata
    features: list[Earthquake]
    bbox: list[float]
