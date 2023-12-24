# --- Day 18: Lavaduct Lagoon ---
# Level
# Part 1: 34329
# Part 2:


from typing import List, Tuple
import re


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip().split() for line in f.readlines()]
    return data


def create_mapping(data: List[str]) -> dict[Tuple[int, int], str]:
    """Returns a dict which maps coordinates to values"""
    print("Rows:", len(data), "Cols:", len(data[0]))
    mapping = {}
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            mapping[(j, i)] = val
    return mapping


def dig_outline(instructions: List[str], usehex=False):
    """Returns a mapping with coordinates of trench outline"""
    x, y = (0, 0)
    mapping = {}
    for instruction in instructions:
        direction, length, hexcolor = instruction
        if usehex:
            # print(hexcolor)
            length = int(hexcolor[2:7], 16)
            direction = "RDLU"[int(hexcolor[7])]
            print(length, direction)
        else:
            for i in range(int(length)):
                if direction == "R":
                    x += 1
                if direction == "L":
                    x -= 1
                if direction == "U":
                    y -= 1
                if direction == "D":
                    y += 1
                mapping[(x, y)] = "#"
    return mapping


def get_adjacent(mapping: dict, coordinates_list: List[Tuple[int, int]]):
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


def flood_fill(
    coordinates: Tuple[int, int], mapping: dict, boundary_character: str = "#"
):
    """Updates list of interior points by flooding from a start point"""

    interior_nodes = []
    visited_nodes = []
    nodes = [coordinates]

    while True:
        nodes = [
            node
            for node in get_adjacent(mapping, nodes)
            if node not in interior_nodes and mapping[node] != boundary_character
        ]

        if not nodes:
            return interior_nodes

        interior_nodes.extend(nodes)


def mapping_to_list(mapping):
    """Convert mapping to list. If sparse mapping returns a rectangular dense mapping"""
    output = []
    y_values = sorted(list(set([x[1] for x in mapping.keys()])))
    x_values = sorted(list(set([x[0] for x in mapping.keys()])))

    for y in y_values:
        output.append([mapping[(x, y)] if (x, y) in mapping else "." for x in x_values])

    return output


if __name__ == "__main__":
    instructions = read_text_file("data/day18.txt")

    # Q1 - Dig plan volume
    data = mapping_to_list(dig_outline(instructions))
    mapping = create_mapping(data)

    # outline volume
    outline_volume = len([x for x in mapping.keys() if mapping[x] == "#"])
    print("outline volume", outline_volume)

    # interior volume
    interior_nodes = flood_fill((45, 45), mapping)
    interior_volume = len(interior_nodes)
    print("interior volume", len(interior_nodes))
    print("Cubic Metres:", outline_volume + interior_volume)

    # Q2 - Dig plan hexcodes
    data = mapping_to_list(dig_outline(instructions, usehex=True))
    mapping = create_mapping(data)

    # outline volume
    outline_volume = len([x for x in mapping.keys() if mapping[x] == "#"])
    print("outline volume", outline_volume)

    # # interior volume
    # interior_nodes = flood_fill((45, 45), mapping)
    # interior_volume = len(interior_nodes)
    # print("interior volume", len(interior_nodes))
    # print("Cubic Metres:", outline_volume + interior_volume)
