# --- Day 3: Gear Ratios ---
# Level 3
# Part 1: 519444
# Part 2: 74528807

from typing import List, Tuple
import re
from functools import reduce

NON_SYMBOLS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ".",
]


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip() for line in f.readlines()]
    return data


def create_mapping(schematic: List[str]) -> dict[Tuple[int, int], str]:
    """Returns a dict which maps coordinates to values"""
    mapping = {}
    for i, row in enumerate(schematic):
        for j, val in enumerate(row):
            mapping[(j, i)] = val
    return mapping


def row_to_idx(row_number: int, row: str) -> List[Tuple[str, int, int, int]]:
    """
    Returns a list of idx for the input schematic row.

    Each idx is a tuple containing (number, row_number, starting position and length)
    and represents a continuous block of numbers in the input schematic row.
    """
    idx_list = []
    numbers = re.findall("[0-9]+", row)

    # Get starting index and length for each number, offset to handle duplicated numbers
    offset = 0
    for number in numbers:
        idx_list.append(
            (number, row_number, row[offset:].find(number) + offset, len(number))
        )
        x = row[offset:].find(number)
        offset = row[offset:].find(number) + offset + len(number)
    return idx_list


def schematic_to_idx(schematic: List[str]) -> List[Tuple[str, int, int, int]]:
    """Converts input schematic into a list of idx"""
    schematic_idx_list = []
    for row_number, row in enumerate(schematic):
        idx_list = row_to_idx(row_number, row)
        schematic_idx_list.append(idx_list)
    return flatten(schematic_idx_list)


def flatten(l: List[List]) -> List:
    """Flattens nested list"""
    return [y for x in l for y in x]


def idx_to_coordinates(idx: Tuple[str, int, int, int]) -> List[Tuple[int, int]]:
    """
    Convert idx to coordinates.

    So an idx for a 3-digit number will return 3 pairs of coordinates.
    """
    coordinates_list = []
    value, y, x, length_of_number = idx

    for i in range(length_of_number):
        coordinates_list.append((x + i, y))

    return coordinates_list


def get_adjacent_coordinates(mapping: dict, coordinates_list: List[Tuple[int, int]]):
    """Returns all adjacent coordinates for the input list of coordinates (excludes input coordinates)"""
    adjacent_coordinates_list = []
    for coordinates in coordinates_list:
        x, y = coordinates
        N = (x, y - 1)
        NE = (x + 1, y - 1)
        E = (x + 1, y)
        SE = (x + 1, y + 1)
        S = (x, y + 1)
        SW = (x - 1, y + 1)
        W = (x - 1, y)
        NW = (x - 1, y - 1)
        adjacent_coordinates_list.extend((N, NE, E, SE, S, SW, W, NW))

    # keep valid coordinates, remove duplicates and original coordinates
    adjacent_coordinates_list = [
        x
        for x in list(set(adjacent_coordinates_list))
        if x in mapping.keys() and x not in coordinates_list
    ]
    return adjacent_coordinates_list


def is_symbol(mapping: dict, coordinates_list: List[Tuple[int, int]]) -> bool:
    """Returns True if input list of coordinates contain values outside [0-9, .]"""
    tmp = []
    for coordinates in coordinates_list:
        # tmp.extend(mapping[coordinates])
        if mapping[coordinates] not in NON_SYMBOLS:
            # print(tmp)
            return True
    # print(tmp)
    return False


def get_coordinates_of_star_symbols(mapping):
    """List of coordinates for all * symbols"""
    symbol_coordinates = []
    for coordinates, val in mapping.items():
        if val in "*":
            symbol_coordinates.append(coordinates)
    return symbol_coordinates


if __name__ == "__main__":
    valid_part_numbers = []
    sum_of_part_numbers = 0

    # import data
    schematic = read_text_file(filepath="data/day3.txt")

    # create mapping
    mapping = create_mapping(schematic)

    # convert schematic into idx list
    idx_list = schematic_to_idx(schematic)

    # Q1
    for idx in idx_list:
        coordinates_list = idx_to_coordinates(idx)
        adjacent_coordinates_list = get_adjacent_coordinates(mapping, coordinates_list)
        if is_symbol(mapping, adjacent_coordinates_list):
            sum_of_part_numbers += int(idx[0])

    # Q2
    symbol_coordinates = get_coordinates_of_star_symbols(mapping)
    sum_of_gear_products = 0
    for coordinates in symbol_coordinates:
        gears = []
        for idx in idx_list:
            coordinates_list = idx_to_coordinates(idx)
            adjacent_coordinates_list = get_adjacent_coordinates(
                mapping, coordinates_list
            )
            if coordinates in adjacent_coordinates_list:
                gears.append(int(idx[0]))

        if len(gears) > 1:
            sum_of_gear_products += reduce(lambda x, y: x * y, gears)

    # print(idx)
    # print(coordinates_list)
    # print(adjacent_coordinates_list)
    # print(sum_of_part_numbers)
    # print()
    print("Q1:", sum_of_part_numbers)
    print("Q2:", sum_of_gear_products)
