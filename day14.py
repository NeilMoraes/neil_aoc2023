# --- Day 14: Parabolic Reflector Dish ---
# Level
# Part 1: 107142
# Part 2:

from typing import List, Tuple
import re
from tqdm import tqdm


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


def roll_left(data):
    """Returns updated data after tilting platform to the left"""
    updated_data = []
    for row in data:
        updated_row = []
        row_split = row.split("#")
        for chunk in row_split:
            count_boulders = len(re.findall("O", chunk))
            updated_row.append(
                "O" * count_boulders + "." * (len(chunk) - count_boulders)
            )
        updated_data.append("#".join(updated_row))
    return updated_data


def tilt_platform(data, direction: str):
    """Return updated data after tilting platfrom in particular direction"""
    if direction == "N":
        return transpose(roll_left(transpose(data)))

    if direction == "E":
        return reversed(roll_left(reversed(data)))

    if direction == "W":
        return roll_left(data)

    if direction == "S":
        return transpose(reversed(roll_left(reversed(transpose(data)))))


def transpose(l: List):
    return ["".join(x) for x in list(map(list, zip(*l)))]


def reversed(l: List):
    return [row[::-1] for row in l]


def calc_total_load(data):
    """Total load on north beam"""
    total_load = 0
    for i, row in enumerate(data):
        value = len(data) - i
        count_boulders = len(re.findall("O", row))
        total_load += count_boulders * value
    return total_load


def get_adjacent_coordinates(mapping: dict, coordinates_list: List[Tuple[int, int]]):
    """Returns all adjacent coordinates for the input list of coordinates (excludes input coordinates)"""
    adjacent_coordinates_list = []
    for coordinates in coordinates_list:
        x, y = coordinates
        N = (x, y - 1)
        E = (x + 1, y)
        S = (x, y + 1)
        W = (x - 1, y)
        adjacent_coordinates_list.extend((N, NE, E, SE, S, SW, W, NW))

    # keep valid coordinates, remove duplicates and original coordinates
    adjacent_coordinates_list = [
        x
        for x in list(set(adjacent_coordinates_list))
        if x in mapping.keys() and x not in coordinates_list
    ]
    return adjacent_coordinates_list


if __name__ == "__main__":
    data = read_text_file("data/day14_test.txt")

    # Q1 - Total load after rollin north
    total_load = calc_total_load(tilt_platform(data, "N"))
    print("Total Load", total_load)

    # Q2 - Total load after 1000000000 cycles cycle = (N,W, S, E)
    # i = 0
    # notConverged = True
    # t0 = data
    # while notConverged:
    #     # cycle
    #     t1 = tilt_platform(t0, "N")
    #     t2 = tilt_platform(t1, "W")
    #     t3 = tilt_platform(t2, "S")
    #     t4 = tilt_platform(t3, "E")

    #     if t4 == t0:  # cycle has converged
    #         notConverged = False
    #     i += 1
    t0 = data
    cycles = []
    for i in tqdm(range(1000)):
        # cycle
        t1 = tilt_platform(t0, "N")
        t2 = tilt_platform(t1, "W")
        t3 = tilt_platform(t2, "S")
        t4 = tilt_platform(t3, "E")

        l1 = calc_total_load(t1)
        l2 = calc_total_load(t2)
        l3 = calc_total_load(t3)
        l4 = calc_total_load(t4)

        t0 = t4

        tmp = [str(l1), str(l2), str(l3), str(l4)]
        cycles.append("_".join(tmp))

        if i > 1000: # run for 1k cycles
        if len(set(cycles)) == (0.5 * len(cycles)):
            break

    print(len(cycles))
    print(cycles)
    # print(cycles[-1])
