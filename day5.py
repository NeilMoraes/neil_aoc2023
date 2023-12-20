# --- Day 5: If You Give A Seed A Fertilizer ---
# Level 2
# Part 1: 289863851
# Part 2: -

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


def remove_overlap(range1, range2):
    range1_start = range1[0]
    range1_end = range1[0] + range1[1] - 1
    range2_start = range2[0]
    range2_end = range2[0] + range2[1] - 1

    issubset = (range2_start >= range1_start) & (range2_end <= range1_end)
    issuperset = (range2_start <= range1_start) & (range2_end >= range1_end)
    isoverlap1 = (range2_start >= range1_start) & (range2_start <= range1_end)
    isoverlap2 = (range1_start >= range2_start) & (range1_start <= range2_end)

    # range2 is subset of range1
    if issubset:
        return []
    elif issuperset:
        return [
            range2_start,
            range1_start - range2_start,
            range1_end,
            range2_end - range1_end,
        ]
    # partial overlap
    elif isoverlap1:
        return [range1_end, range2_end - range1_end]
    elif isoverlap2:
        return [range2_start, range1_start - range2_start]
    # no overlap
    else:
        return range2


def flatten(l: List[List]) -> List:
    """Flattens nested list"""
    return [y for x in l for y in x]


def dedupe_seed_range(seed_ranges: List[int]):
    """Remove duplicates in seed ranges for Q2 to speed up computation?"""
    deduped_seed_ranges = []
    for start, end in zip(
        range(0, len(seed_ranges), 2), range(2, len(seed_ranges) + 1, 2)
    ):
        current_seed_range = seed_ranges[start:end]
        if not deduped_seed_ranges:
            deduped_seed_ranges.append(current_seed_range)
        else:
            new_range = current_seed_range
            for i, rng in enumerate(deduped_seed_ranges):
                if (
                    len(remove_overlap(rng, new_range)) > 2
                ):  # happens when range2 is superset of range1
                    deduped_seed_ranges[i - 1] = new_range
                else:
                    new_range = remove_overlap(rng, new_range)
            if new_range:
                deduped_seed_ranges.append(new_range)

    return flatten(deduped_seed_ranges)


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

    # Q2 - get location for seed ranges (brute force)
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

    # Q2 - get location for seed ranges (deduped seed ranges)
    # lowest_location = 10e50
    # print(almanac["seeds"])
    # print(dedupe_seed_range(almanac["seeds"]))
    # for start, end in zip(
    #     range(0, len(almanac["seeds"]), 2), range(2, len(almanac["seeds"]) + 1, 2)
    # ):
    #     start_seed, length = almanac["seeds"][start:end]
    #     for seed in range(start_seed, start_seed + length):
    #         soil = get_destination(seed, almanac["seed-to-soil map"])
    #         fert = get_destination(soil, almanac["soil-to-fertilizer map"])
    #         water = get_destination(fert, almanac["fertilizer-to-water map"])
    #         light = get_destination(water, almanac["water-to-light map"])
    #         temp = get_destination(light, almanac["light-to-temperature map"])
    #         humidity = get_destination(temp, almanac["temperature-to-humidity map"])
    #         location = get_destination(humidity, almanac["humidity-to-location map"])
    #         if location < lowest_location:
    #             lowest_location = location
    # print("Q2:", lowest_location)

    # print(remove_overlap(range1=[10, 10], range2=[15, 10]))
    # print(dedupe_seed_range([10, 10, 15, 10]))
