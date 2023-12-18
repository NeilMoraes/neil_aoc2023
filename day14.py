# --- Day 14: Parabolic Reflector Dish ---
# Level 3
# Part 1: 107142
# Part 2: 104815

from typing import List, Tuple
import re


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip() for line in f.readlines()]
    return data


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


if __name__ == "__main__":
    data = read_text_file("data/day14.txt")

    # Q1 - Total load after rollin north
    total_load = calc_total_load(tilt_platform(data, "N"))
    print("Total Load", total_load)

    # Q2 - Total north load after 1000000000 cycles, 1 cycle = (N, W, S, E)
    SPIN_CYCLES = 1000000000
    t0 = data
    loads = []  # each value is the data state after a full cycle
    notConverged = True
    while notConverged:
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

        # check for loop
        if t0 in loads:
            num_cycles_before_loop_begins = loads.index(t0)
            num_cycles_in_loop = len(loads) - num_cycles_before_loop_begins
            notConverged = False
        else:
            loads.append(t0)

    print(
        "num_cycles_before_loop_begins:",
        num_cycles_before_loop_begins,
        "\nnum_cycles_in_loop:",
        num_cycles_in_loop,
    )

    # determine expected rock layout after 1000000000 cycles
    id_at_spin_cycle = (
        SPIN_CYCLES - num_cycles_before_loop_begins
    ) % num_cycles_in_loop - 1
    expected_data = loads[num_cycles_before_loop_begins + id_at_spin_cycle]

    # expect load after 1000000000 cycles
    print("Expected load at 1000000000 cycles:", calc_total_load(expected_data))
