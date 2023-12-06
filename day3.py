# --- Day 3: Gear Ratios ---
# Part 1:
# Part 2:

from typing import List, Tuple
import re


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip() for line in f.readlines()]
    return data


def create_schematic(data: List[str]) -> dict[Tuple[int, int], str]:
    """Returns a dict which maps coordinates to values"""
    schematic = {}
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            schematic[(i, j)] = val
    return schematic


def parse_row(row_number: int, row: str) -> List[Tuple[int, int, int]]:
    """Return row_number, starting position and length for all numbers in row"""
    idx = []
    numbers = re.findall("[0-9]+", row)

    # Get starting index and length for each number, offset to handle duplicated numbers
    offset = 0
    for number in numbers:
        idx.append((number, row_number, row.find(number, offset) + offset, len(number)))
        offset = row.find(number, offset) + offset + len(number)

    return idx


def idx_to_coordinates(id: List[Tuple[int, int]]):
    """Convert idx to coordinates"""
    for id in idx:
        coordinates = []


if __name__ == "__main__":
    valid_part_numbers = []

    # import data
    data = read_text_file(filepath="data/day3.txt")

    # create schematic mapping
    schematic = create_schematic(data)

    #
    for row_number, row in enumerate(data[:10]):
        idx = parse_row(row_number, row)
        print(idx)
