# --- Day 11: Cosmic Expansion ---
# Level 3
# Part 1: 9599070
# Part 2: 842645913794

from typing import List, Tuple
from tqdm import tqdm


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip() for line in f.readlines()]
    return data


def create_mapping(data: List[str]) -> dict[Tuple[int, int], str]:
    """Returns a dict which maps coordinates to values"""
    mapping = {}
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            mapping[(j, i)] = val
    return mapping


def get_galaxy_coordinates(mapping) -> List[Tuple[int, int]]:
    """Return list of coordinates for all galaxies"""
    return [coordinates for coordinates, value in mapping.items() if value != "."]


def get_empty_space(data) -> Tuple[List[int], List[int]]:
    """Get indexes of empty rows and columns"""
    empty_rows = []
    empty_columns = []

    # empty row indexes
    for i, row in enumerate(data):
        if all([val == "." for val in row]):
            empty_rows.append(i)

    # empty column indexes
    column = []
    for i in range(len(data[0])):
        for row in data:
            column.append(row[i])
        if all([val == "." for val in column]):
            empty_columns.append(i)
        column = []
    return empty_rows, empty_columns


def get_shortest_distance(
    p1: Tuple[int, int],
    p2: Tuple[int, int],
    empty_columns: List[int],
    empty_rows: List[int],
    expansion_factor: int = 2,
):
    """Get shortest distance between p1 and p2, handle extra space"""
    x1, y1 = p1
    x2, y2 = p2

    # group x and y coordinates
    ordered_x = sorted([x1, x2])
    ordered_y = sorted([y1, y2])

    # get expansion along y-axis and x-axis between points p1 and p2
    y_expansion = len(
        [x for x in empty_rows if x < ordered_y[1] and x > ordered_y[0]]
    ) * (expansion_factor - 1)
    x_expansion = len(
        [x for x in empty_columns if x < ordered_x[1] and x > ordered_x[0]]
    ) * (expansion_factor - 1)

    distance = abs(ordered_x[1] - ordered_x[0] + y_expansion) + abs(
        ordered_y[1] - ordered_y[0] + x_expansion
    )
    return distance


if __name__ == "__main__":
    # import data
    data = read_text_file("data/day11.txt")

    # processing
    mapping = create_mapping(data)
    empty_rows, empty_columns = get_empty_space(data)
    galaxy_coordinates = get_galaxy_coordinates(mapping)

    # Q1 - expansion factor = 2
    sum_of_shortest_paths = 0
    visited = []
    for galaxy1 in tqdm(galaxy_coordinates):
        for galaxy2 in galaxy_coordinates:
            if galaxy2 not in visited:
                sum_of_shortest_paths += get_shortest_distance(
                    p1=galaxy1,
                    p2=galaxy2,
                    empty_columns=empty_columns,
                    empty_rows=empty_rows,
                    expansion_factor=2,
                )

        visited.append(galaxy1)
    print("Q1:", sum_of_shortest_paths)

    # Q2 - older universe, expansion factor=1Mil
    sum_of_shortest_paths = 0
    visited = []
    for galaxy1 in tqdm(galaxy_coordinates):
        for galaxy2 in galaxy_coordinates:
            if galaxy2 not in visited:
                sum_of_shortest_paths += get_shortest_distance(
                    p1=galaxy1,
                    p2=galaxy2,
                    empty_columns=empty_columns,
                    empty_rows=empty_rows,
                    expansion_factor=1000000,
                )

        visited.append(galaxy1)
    print("Q2:", sum_of_shortest_paths)
