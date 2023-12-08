# --- Day 5: If You Give A Seed A Fertilizer ---
# Level 2
# Part 1: 289863851
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


def create_almanac(data) -> dict:
    """Create almanac from data"""
    almanac = {}
    for val in data:
        almanac[val[0].split(":")[0]] = [int(x) for x in get_all_digits(" ".join(val))]
    return almanac


def get_destination(seed: int, mapping: List[int]):
    """Use mapping to get destination for input seed"""
    for start, end in zip(range(0, len(mapping), 3), range(3, len(mapping) + 1, 3)):
        destination, source, length = mapping[start:end]

        if (seed >= source) & (seed <= source + length - 1):
            output = seed - source + destination
            return output
    return seed


# def get_seeds(seeds: List[int]):
#     """Converts range of seed numbers to list of seeds"""
#     seed_numbers = []
#     for start, end in zip(range(0, len(seeds), 2), range(2, len(seeds) + 1, 2)):
#         start_seed, length = seeds[start:end]
#         seed_numbers.extend(list(range(start_seed, start_seed + length)))
#     return set(seed_numbers)


if __name__ == "__main__":
    # import data
    data = read_text_file_day5(filepath="data/day5.txt")
    almanac = create_almanac(data)

    # Q1 - get location for each seed
    lowest_location = 10e50
    for seed in almanac["seeds"]:
        soil = get_destination(seed, almanac["seed-to-soil map"])
        fert = get_destination(soil, almanac["soil-to-fertilizer map"])
        water = get_destination(fert, almanac["fertilizer-to-water map"])
        light = get_destination(water, almanac["water-to-light map"])
        temp = get_destination(light, almanac["light-to-temperature map"])
        humidity = get_destination(temp, almanac["temperature-to-humidity map"])
        location = get_destination(humidity, almanac["humidity-to-location map"])
        if location < lowest_location:
            lowest_location = location
    print("Q1:", lowest_location)

    # Q2 - get location for seed ranges
    lowest_location = 10e50
    for start, end in zip(
        range(0, len(almanac["seeds"]), 2), range(2, len(almanac["seeds"]) + 1, 2)
    ):
        start_seed, length = almanac["seeds"][start:end]
        for seed in range(start_seed, start_seed + length):
            soil = get_destination(seed, almanac["seed-to-soil map"])
            fert = get_destination(soil, almanac["soil-to-fertilizer map"])
            water = get_destination(fert, almanac["fertilizer-to-water map"])
            light = get_destination(water, almanac["water-to-light map"])
            temp = get_destination(light, almanac["light-to-temperature map"])
            humidity = get_destination(temp, almanac["temperature-to-humidity map"])
            location = get_destination(humidity, almanac["humidity-to-location map"])
            if location < lowest_location:
                lowest_location = location
    print("Q2:", lowest_location)
