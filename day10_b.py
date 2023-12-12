# --- Day 10: Pipe Maze ---
# Level 3
# Part 1: 6823
# Part 2:

from typing import List, Tuple
from tqdm import tqdm
import pickle


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


def get_connected_v2(mapping: dict, coordinates_list: List[Tuple[int, int]]):
    """Returns all adjacent connected coordinates for the input list of coordinates (excludes input coordinates)"""
    adjacent_coordinates_list = []
    for coordinates in coordinates_list:
        x, y = coordinates
        N = (x, y - 1)
        E = (x + 1, y)
        S = (x, y + 1)
        W = (x - 1, y)

        adjacent_coordinates_list.extend(
            (
                N,
                E,
                S,
                W,
            )
        )

    # keep valid coordinates, remove duplicates and original coordinates
    adjacent_coordinates_list = [
        x
        for x in list(set(adjacent_coordinates_list))
        if x in mapping.keys() and x not in coordinates_list
    ]

    return adjacent_coordinates_list


if __name__ == "__main__":
    data = read_text_file("data/day10.txt")
    mapping = create_mapping(data)

    # Get saved longest loop from Q1
    with open("longest_loop.pkl", "rb") as f:
        longest_loop = pickle.load(f)
    print("length longest loop:", len(longest_loop))

    # Visulaize loop
    import matplotlib.pyplot as plt

    longest_loop_plot = [elem for elem in longest_loop if elem != "S"]
    plt.scatter(*zip(*longest_loop_plot), s=0.5)
    plt.savefig("Day10a_loop.png")

    non_loop_plot = [
        elem for elem in mapping.keys() if elem != "S" and elem not in longest_loop
    ]
    # plt.scatter(*zip(*non_loop_plot), s=0.5)
    # plt.savefig("Day10a_nonloop.png")

    # x-beam
    isInterior = False
    interior_points1 = []
    for x in range(len(data[0])):
        for y in range(len(data)):
            if ((x, y) in longest_loop) | (mapping[(x, y)] == "S"):
                isInterior = not isInterior
            if isInterior:
                interior_points1.append((x, y))
    # y-beam
    isInterior = False
    interior_points2 = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            if (x, y) in longest_loop:
                isInterior = not isInterior
            if isInterior:
                interior_points2.append((x, y))

    # interior points - symmetric difference of x-beam and y-beam and exclude pipe co-ordinates
    interior_points = set(interior_points1).intersection(interior_points2)
    interior_points = [x for x in interior_points if x not in longest_loop]
    interior_points = [point for point in interior_points if mapping[point] in ["."]]

    print(len(interior_points))

    plt.scatter(*zip(*interior_points), s=0.5)
    plt.show()
