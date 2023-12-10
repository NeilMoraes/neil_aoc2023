# --- Day 9: Mirage Maintenance ---
# Level 1
# Part 1: 1834108701
# Part 2: 993

from typing import List, Tuple
import re
import numpy as np


def read_text_file(filepath: str) -> Tuple[str, dict]:
    with open(filepath, "r") as f:
        data = [[int(x) for x in line.strip().split()] for line in f.readlines()]
    return data


if __name__ == "__main__":
    # import data
    data = read_text_file(filepath="data/day9.txt")

    # Q1 - Sum of next value (right side)
    sum_of_next_values = 0
    for row in data:
        report = np.array(row)
        is_not_zeros = True
        last_values = []
        while is_not_zeros:
            last_values.append(report[-1])
            report = np.diff(report)
            if all(report == 0):
                is_not_zeros = False
                sum_of_next_values += sum(last_values)
    print("Q1:", sum_of_next_values)

    # Q2 - sum of next value (left side)
    sum_of_previous_values = 0
    for row in data:
        report = np.array(row)
        is_not_zeros = True
        first_values = []
        # print(report)
        while is_not_zeros:
            first_values.append(report[0])
            report = np.diff(report)
            if all(report == 0):
                is_not_zeros = False
                tmp = 0
                for i, val in enumerate(first_values[::-1]):
                    if i == 0:
                        tmp = val
                    else:
                        tmp = val - tmp
                sum_of_previous_values += tmp
    print("Q2:", sum_of_previous_values)
