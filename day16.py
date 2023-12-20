# # --- Day 16: The Floor Will Be Lava ---
# # Level 2
# # Part 1: 7185
# # Part 2: 7616

from typing import List, Tuple
import re
from functools import reduce


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


def get_beam_path(start_coordinates: tuple[int, int], direction: str):
    """Get all coordinates in direction of beam path excluding start_coordinates"""
    x, y = start_coordinates
    if direction == "E":
        coordinates = [
            coord for coord in mapping.keys() if (coord[1] == y) and (coord[0] > x)
        ]
    elif direction == "W":
        coordinates = [
            coord for coord in mapping.keys() if (coord[1] == y) and (coord[0] < x)
        ]
        coordinates = sorted(coordinates, key=lambda x: -x[0])
    elif direction == "N":
        # get coordinates across which bean is fired
        coordinates = [
            coord for coord in mapping.keys() if (coord[1] < y) and (coord[0] == x)
        ]
        coordinates = sorted(coordinates, key=lambda x: -x[1])
    elif direction == "S":
        coordinates = [
            coord for coord in mapping.keys() if (coord[1] > y) and (coord[0] == x)
        ]
    return coordinates


def energise_tiles(
    splits, mapping: dict
) -> Tuple[List[Tuple[int, int]], List[Tuple[Tuple[int, int], str]]]:
    """Fires beam for specified splits. Returns energised coordinates and starting coordinates + direction for any splits"""

    # track energised tiles, new beams createdby splits
    energised_tiles = []
    new_splits = []

    for split in splits:
        start_coordinates, direction = split
        energised_tiles.append(start_coordinates)
        if direction == "E":
            beam_path = get_beam_path(start_coordinates, direction)
            for coord in beam_path:
                energised_tiles.append(coord)
                if mapping[coord] == "|":
                    new_splits.append([coord, "N"])
                    new_splits.append([coord, "S"])
                    break
                elif mapping[coord] == "/":
                    new_splits.append([coord, "N"])
                    break
                elif mapping[coord] == "\\":
                    new_splits.append([coord, "S"])
                    break

        elif direction == "W":
            beam_path = get_beam_path(start_coordinates, direction)
            for coord in beam_path:
                energised_tiles.append(coord)
                if mapping[coord] == "|":
                    new_splits.append([coord, "N"])
                    new_splits.append([coord, "S"])
                    break
                elif mapping[coord] == "/":
                    new_splits.append([coord, "S"])
                    break
                elif mapping[coord] == "\\":
                    new_splits.append([coord, "N"])
                    break

        elif direction == "N":
            beam_path = get_beam_path(start_coordinates, direction)
            for coord in beam_path:
                energised_tiles.append(coord)
                if mapping[coord] == "-":
                    new_splits.append([coord, "E"])
                    new_splits.append([coord, "W"])
                    break
                elif mapping[coord] == "/":
                    new_splits.append([coord, "E"])
                    break
                elif mapping[coord] == "\\":
                    new_splits.append([coord, "W"])
                    break

        elif direction == "S":
            beam_path = get_beam_path(start_coordinates, direction)
            for coord in beam_path:
                energised_tiles.append(coord)
                if mapping[coord] == "-":
                    new_splits.append([coord, "E"])
                    new_splits.append([coord, "W"])
                    break
                elif mapping[coord] == "/":
                    new_splits.append([coord, "W"])
                    break
                elif mapping[coord] == "\\":
                    new_splits.append([coord, "E"])
                    break

    return energised_tiles, new_splits


def flatten(l: List[List]) -> List:
    """Flattens nested list"""
    return [y for x in l for y in x]


def fire_beam(splits, mapping):
    # track splits and energised tiles
    all_splits = []
    all_energised = []

    # Q1 - Fire initial beam
    notConverged = True
    while notConverged:
        energised, splits = energise_tiles(
            splits=splits,
            mapping=mapping,
        )

        # keep splits which have not been seen before
        splits = [x for x in splits if x not in all_splits]
        all_splits.extend(splits)
        all_energised.extend(energised)

        # print("######################")
        # print("Iteration:", i)
        # print("new splits", splits)
        # print("all splits", all_splits)
        # print("all energised:", all_energised)
        # print()
        # print()
        # print(len(set(all_energised)), len(splits))

        if not splits:
            notConverged = False
    return len(set(all_energised))


if __name__ == "__main__":
    # import data
    data = read_text_file(filepath="data/day16.txt")
    mapping = create_mapping(data)

    # starting beam (sneaky!!)
    starting_split = [[(0, 0), "S"]]

    # Q1 - Number energised tiles
    print("Energised Tiles:", fire_beam(starting_split, mapping))

    # Q2
    top_tiles = [coord for coord in mapping.keys() if coord[1] == 0]
    right_tiles = [coord for coord in mapping.keys() if coord[0] == len(data[0]) - 1]
    left_tiles = [coord for coord in mapping.keys() if coord[0] == 0]
    bottom_tiles = [coord for coord in mapping.keys() if coord[1] == len(data) - 1]

    # max_energised = 0
    # for i, start in enumerate(top_tiles):
    #     count_energised = fire_beam([[start, "S"]], mapping)
    #     if count_energised > max_energised:
    #         max_energised = count_energised
    # print("Max Energised (TOP)", max_energised)

    max_energised = 0
    for i, start in enumerate(right_tiles):
        count_energised = fire_beam([[start, "W"]], mapping)
        if count_energised > max_energised:
            max_energised = count_energised
    print("Max Energised (RIGHT)", max_energised)

    # max_energised = 0
    # for i, start in enumerate(left_tiles):
    #     count_energised = fire_beam([[start, "E"]], mapping)
    #     if count_energised > max_energised:
    #         max_energised = count_energised
    # print("Max Energised (LEFT)", max_energised)

    max_energised = 0
    for i, start in enumerate(bottom_tiles):
        count_energised = fire_beam([[start, "N"]], mapping)
        if count_energised > max_energised:
            max_energised = count_energised
    print("Max Energised (BOTTOM)", max_energised)
