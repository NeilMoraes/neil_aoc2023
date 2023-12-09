# --- Day 8: Haunted Wasteland ---
# Level
# Part 1: 22411
# Part 2:

from typing import List, Tuple
import re


def read_text_file(filepath: str) -> Tuple[str, dict]:
    with open(filepath, "r") as f:
        raw = [line.strip() for line in f.readlines()]
    instructions = raw[0]

    nodes = {}
    for val in raw[2:]:
        start_node, left_node, right_node = re.findall(r"[A-Z1-9]+", val)
        nodes[start_node] = (left_node, right_node)
    return (instructions, nodes)


def step_generator(instructions):
    yield from insructions


if __name__ == "__main__":
    # import data
    insructions, nodes = read_text_file(filepath="data/day8_test.txt")

    # # Q1 - number of steps to ZZZ
    # current_node = "AAA"
    # step_counter = 0
    # step = step_generator(insructions)
    # i = 0
    # while current_node != "ZZZ":
    #     try:
    #         next_step = next(step)
    #     except:
    #         step = step_generator(insructions)
    #         next_step = next(step)

    #     if next_step == "L":
    #         current_node = nodes[current_node][0]
    #     else:
    #         current_node = nodes[current_node][1]
    #     step_counter += 1
    # print("Q1:", step_counter)

    # Q2 - simulataneous steps from **A to **Z
    print(nodes)
    current_node = [x for x in nodes.keys() if x.endswith("A")]  # all starting nodes
    step_counter = 0
    step = step_generator(insructions)
    print(current_node)
    not_converged = True
    while not_converged:
        try:
            next_step = next(step)
        except:
            step = step_generator(insructions)
            next_step = next(step)

        if next_step == "L":
            for i, node in enumerate(current_node):
                current_node[i] = nodes[node][0]
        else:
            for i, node in enumerate(current_node):
                current_node[i] = nodes[node][1]
        step_counter += 1
        if all([node[-1] == "Z" for node in current_node]):
            not_converged = False
        print(next_step, current_node, [node[-1] == "Z" for node in current_node])
    print("Q2:", step_counter)
