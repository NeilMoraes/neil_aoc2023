from typing import List, Tuple
from tqdm import tqdm


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip() for line in f.readlines()]

    data = number_galaxies(data)
    data = expand_space(data)
    return data


def number_galaxies(data):
    """Number galaxies"""
    num = 1
    numbered_data = []
    for row in data:
        while row.find("#") != -1:
            row = row.replace("#", str(num), 1)
            num += 1
        numbered_data.append(row)
    return numbered_data


def expand_space(data):
    """Add rows and columns to data to represent empty space"""
    empty_rows = []
    empty_columns = []
    # empty rows
    for i, row in enumerate(data):
        if all([val == "." for val in row]):
            empty_rows.append(i)
    for offset, i in enumerate(empty_rows):
        data.insert(i + 1 + offset, data[i + offset])

    # empty columns
    column = []
    for i in range(len(data[0])):
        for row in data:
            column.append(row[i])
        if all([val == "." for val in column]):
            empty_columns.append(i)
        column = []
    for offset, i in enumerate(empty_columns):
        for j, row in enumerate(data):
            data[j] = data[j][: (i + offset)] + "." + data[j][(i + offset) :]
    return data


def create_mapping(data: List[str]) -> dict[Tuple[int, int], str]:
    """Returns a dict which maps coordinates to values"""
    mapping = {}
    for i, row in enumerate(data):
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


def get_shortest_paths(mapping, starting_point):
    distances = {}
    num_steps = 1
    next_steps = starting_point
    distances[starting_point[0]] = 0

    while len(distances) != len(mapping):
        next_steps = get_connected_v2(mapping, next_steps)
        for step in next_steps:
            if step not in distances:
                distances[step] = num_steps
        num_steps += 1
    return distances


def get_shortest_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def get_galaxy_coordinates(mapping):
    return {k: v for k, v in mapping.items() if v != "."}


if __name__ == "__main__":
    data = read_text_file("data/day11_test.txt")
    mapping = create_mapping(data)
    galaxy_coordinates = get_galaxy_coordinates(mapping)
    # distances = get_shortest_paths(mapping, [(0, 0)])
    print(galaxy_coordinates)
    # Q1 - sum of shortest paths
    sum_of_shortest_paths = 0
    visited = []
    for galaxy1 in tqdm(galaxy_coordinates):
        for galaxy2 in galaxy_coordinates:
            if galaxy2 not in visited:
                sum_of_shortest_paths += get_shortest_distance(galaxy1, galaxy2)
                print(galaxy1, galaxy2, get_shortest_distance(galaxy1, galaxy2))
        visited.append(galaxy1)

    print("Q1:", sum_of_shortest_paths)

    # # Q1 - sum of shortest paths
    # sum_of_shortest_paths = 0
    # galaxy_distances = {}
    # visited = []
    # for galaxy in tqdm(galaxy_coordinates):
    #     distances = get_shortest_paths(mapping, [galaxy])
    #     galaxy_distances = {
    #         k: v
    #         for k, v in distances.items()
    #         if k in galaxy_coordinates and k not in visited
    #     }
    #     visited.append(galaxy)
    #     print(galaxy_distances)
    #     sum_of_shortest_paths += sum(galaxy_distances.values())
    # print("Q1:", sum_of_shortest_paths)
