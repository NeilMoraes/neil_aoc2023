# --- Day 19: Aplenty ---
# Level
# Part 1: 476889
# Part 2:


from typing import List, Tuple
import re


def read_text_file(filepath: str) -> List[str]:
    workflows = []
    parts = []
    with open(filepath, "r") as f:
        data = [line.strip() for line in f.readlines()]

    idx = data.index("")
    workflows = data[:idx]
    parts = [x[:-1] for x in data[idx + 1 :]]
    return parse_workflows(workflows), parse_parts(parts)


def parse_workflows(workflows: List[str]) -> dict:
    mapping = {}
    for row in workflows:
        workflow = row.split("{")[0]
        rules = re.findall(r"\{(.*?)\}", row)[0].split(",")
        mapping[workflow] = rules
    return mapping


def parse_parts(parts: List[str]) -> List[List[int]]:
    out = []
    for part in parts:
        out.append([int(x.split("=")[1]) for x in part.split(",")])
    return out


def process(part, workflow: str, workflows: dict):
    rules = workflows[workflow]
    isNotProcessed = True
    i = 0
    accept_list = []
    while isNotProcessed:
        rule = rules[i]
        if rule.find(":") != -1:
            category, sign, value, next_workflow = (
                rule[0],
                rule[1],
                int(rule.split(":")[0][2:]),
                rule.split(":")[1],
            )
            print(category, sign, value, next_workflow)
            print(part)
            if sign == "<":
                if part["xmas".find(category)] < value:
                    if next_workflow == "A":
                        return True
                    elif next_workflow == "R":
                        return False
                    else:
                        return process(part, next_workflow, workflows)
                else:
                    i += 1
            elif sign == ">":
                if part["xmas".find(category)] > value:
                    if next_workflow == "A":
                        return True
                    elif next_workflow == "R":
                        return False
                    else:
                        return process(part, next_workflow, workflows)
                else:
                    i += 1

        elif rule == "R":
            return False
        elif rule == "A":
            return True
        else:
            return process(part, rule, workflows)


if __name__ == "__main__":
    workflows, parts = read_text_file("data/day19_test.txt")

    print(workflows, parts)
    # accepted_sum = 0
    # for i, part in enumerate(parts):
    #     if process(part, "in", workflows):
    #         accepted_sum += sum(part)
    # print("Q1 Sum accepted parts:", accepted_sum)
