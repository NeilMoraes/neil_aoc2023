from typing import List, Tuple
import re


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip().split(",") for line in f.readlines()]
    return flatten([x for x in data if x != ""])


def flatten(l: List[List]) -> List:
    """Flattens nested list"""
    return [y for x in l for y in x]


def HASH(text: str, multiple: int = 17):
    """Return HASH result for input text"""
    result = 0
    for char in text:
        ascii_code = ord(char)
        result += ascii_code
        result = (result * multiple) % 256
    return result


def HASHMAP(text: str, boxes: dict):
    """Returns all boxes and lenses"""

    # add lens (=)
    if text.find("=") != -1:
        label = text.split("=")[0]
        box = HASH(label)
        focal_length = text.split("=")[1]

        print(label, box, focal_length)

        if box in boxes:
            if label in boxes[box]["label_list"]:
                idx = boxes[box]["label_list"].index(label)
                boxes[box]["focal_list"][idx] = focal_length
            else:
                boxes[box]["label_list"] = boxes[box]["label_list"] + [label]
                boxes[box]["focal_list"] = boxes[box]["focal_list"] + [focal_length]
        else:
            boxes[box] = {
                "label_list": [label],
                "focal_list": [focal_length],
            }

    # remove lens (-)
    if text.find("-") != -1:
        label = text.split("-")[0]
        box = HASH(label)
        print(label, box)

        if box in boxes:
            if label in boxes[box]["label_list"]:
                idx = boxes[box]["label_list"].index(label)

                # remove from labels
                tmp = boxes[box]["label_list"]
                tmp.pop(idx)
                boxes[box]["label_list"] = tmp

                # remove from lens
                tmp = boxes[box]["focal_list"]
                tmp.pop(idx)
                boxes[box]["focal_list"] = tmp

    return boxes


def calc_focusing_power(boxes: dict):
    """Calculates focusing power for boxes from HASHMAP"""
    focusing_power = 0
    for box in boxes.keys():
        for i, focal_length in enumerate(boxes[box]["focal_list"]):
            tmp = (box + 1) * (i + 1) * int(focal_length)
            # print(tmp)
            focusing_power += tmp
    return focusing_power


if __name__ == "__main__":
    data = read_text_file("data/day15.txt")
    print(data)

    # Q1 - sum of hashes
    sum_of_hashes = 0
    for row in data:
        sum_of_hashes += HASH(row, multiple=17)
    print("sum of hashes:", sum_of_hashes)

    # Q2
    boxes = {}
    for row in data:
        print(row)
        boxes = HASHMAP(row, boxes)
        # print(boxes)
    focusing_power = calc_focusing_power(boxes)
    print("focusing power:", focusing_power)
