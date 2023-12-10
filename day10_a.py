# --- Day 10: Pipe Maze ---
# Level 3
# Part 1: 6823
# Part 2:

from typing import List, Tuple
import random
from tqdm import tqdm
import pickle

DEBUG = False


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


def get_connected(mapping: dict, coordinates_list: List[Tuple[int, int]]):
    """Returns all adjacent connected coordinates for the input list of coordinates (excludes input coordinates)"""
    adjacent_coordinates_list = []
    for coordinates in coordinates_list:
        x, y = coordinates
        N = (x, y - 1)
        if N in mapping:
            if mapping[N] not in ["|", "F", "7"]:
                N = (-1, -1)

        E = (x + 1, y)
        if E in mapping:
            if mapping[E] not in ["-", "J", "7"]:
                E = (-1, -1)

        S = (x, y + 1)
        if S in mapping:
            if mapping[S] not in ["|", "L", "J"]:
                S = (-1, -1)

        W = (x - 1, y)
        if W in mapping:
            if mapping[W] not in ["-", "L", "F"]:
                W = (-1, -1)

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
        if x in mapping.keys() and x not in coordinates_list and x != (-1, -1)
    ]

    return adjacent_coordinates_list


if __name__ == "__main__":
    data = read_text_file("data/day10.txt")
    mapping = create_mapping(data)

    # initialise variables
    visited_nodes = []
    dead_ends = []
    loops = []
    longest_failed_path = []

    # initial step
    S = list({k: v for k, v in mapping.items() if v == "S"}.keys())
    print("S", S)
    next = S
    visited_nodes.append("S")

    # heuristic to find longest loop
    for i in tqdm(range(500)):
        notConverged = True
        if DEBUG:
            print("i", i)

        # random walk till dead-end or loop is found
        while notConverged:
            # get valid moves from current node
            next = [
                node
                for node in get_connected(mapping, next)
                if node not in (visited_nodes + dead_ends)
            ]
            if DEBUG:
                print("next options", next)

            # convergence criteria for longest loop with S
            if (visited_nodes[-1] in get_connected(mapping, S)) & (
                len(visited_nodes) > 2
            ):
                loops.append(visited_nodes)
                notConverged = False
                print("Found Loop!!")
                visited_nodes = ["S"]
            # random walk to next valid node
            elif next:
                next = [random.choice(next)]
                if DEBUG:
                    print("random choice", next)
                visited_nodes.append(next[0])
                if DEBUG:
                    print("visited nodes", visited_nodes)
            # dead end - no valid moves
            else:
                if visited_nodes:
                    if visited_nodes[-1] != "S":
                        dead_ends.append(visited_nodes[-1])
                    if dead_ends:
                        if DEBUG:
                            print("dead ends:", dead_ends)
                            print("Reached Dead End: Try Again")
                longest_failed_path.append(len(visited_nodes))
                next = S
                visited_nodes = ["S"]
                # dead_ends = []
                notConverged = False

    # output results
    longest_loop = []
    for i, loop in enumerate(loops):
        if len(loop) > len(longest_loop):
            longest_loop = loop
    # print("dead ends:", dead_ends)
    print("max loop length", len(longest_loop))

    # save to file
    with open("longest_loop.pkl", "wb") as f:  # open a text file
        pickle.dump(longest_loop, f)  # serialize the list
