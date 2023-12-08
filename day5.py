# --- Day 5: If You Give A Seed A Fertilizer ---
# Level
# Part 1:
# Part 2:

from typing import List, Tuple
import re
from functools import reduce


def read_text_file_day5(filepath: str) -> List[str]:
    """Modified Read data file"""
    data = []
    with open(filepath, "r") as f:
        raw_text = f.readlines()
        chunk = []
        for i, row in enumerate(raw_text):
            if (row == "\n") | (len(raw_text) == (i + 1)):
                data.append(chunk)
                chunk = []
            else:
                chunk.append(row)
    return data


def get_all_digits(text: str) -> List[int]:
    """
    Returns list of numbers in `text`
    """
    numbers = re.findall(r"\d+", text)
    return numbers


def flatten(l: List[List]) -> List:
    """Flattens nested list"""
    return [y for x in l for y in x]


def create_almanac(data) -> dict:
    almanac = {}
    for val in data:
        almanac[val[0].split(":")[0]] = [int(x) for x in get_all_digits(" ".join(val))]
    return almanac


def create_mappings(almanac: dict) -> dict:
    mapping = {}
    for key, val in almanac.items():
        if key == "seeds":
            mapping[key] = val
        else:
            sources = flatten(
                list(range(start, start + length))
                for start, length in zip(val[1::3], val[2::3])
            )
            destinations = flatten(
                list(range(start, start + length))
                for start, length in zip(val[::3], val[2::3])
            )

            mapping[key] = {k: v for k, v in zip(sources, destinations)}
    return mapping


if __name__ == "__main__":
    # import data
    data = read_text_file_day5(filepath="data/day5.txt")
    almanac = create_almanac(data)
    mapping = create_mappings(almanac)

    # Q1 - get location for each seed
    location_list = []
    for seed in mapping["seeds"]:
        # seed to soil
        if seed in mapping["seed-to-soil map"].keys():
            soil = mapping["seed-to-soil map"][seed]
        else:
            soil = seed
        # soil to fertiliser
        if soil in mapping["soil-to-fertilizer map"].keys():
            fert = mapping["soil-to-fertilizer map"][soil]
        else:
            fert = soil

        # fert to water
        if fert in mapping["fertilizer-to-water map"].keys():
            water = mapping["fertilizer-to-water map"][fert]
        else:
            water = fert

        # water to light
        if water in mapping["water-to-light map"].keys():
            light = mapping["water-to-light map"][water]
        else:
            light = water

        # light to temp
        if light in mapping["light-to-temperature map"].keys():
            temp = mapping["light-to-temperature map"][light]
        else:
            temp = light

        # temp to humidity
        if temp in mapping["temperature-to-humidity map"].keys():
            humidity = mapping["temperature-to-humidity map"][temp]
        else:
            humidity = temp

        # humidity to location
        if humidity in mapping["humidity-to-location map"].keys():
            location = mapping["humidity-to-location map"][humidity]
        else:
            location = humidity

        location_list.append(location)

    # Q1
    print("Q1:", min(location_list))
    # print(data)
    # print(almanac)
    # print(mapping)
