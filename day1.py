# --- Day 1: Trebuchet?! ---
# Level 1
# Part 1: 55208
# Part 2: 54578

import re
from typing import List


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip() for line in f.readlines()]
    return data


def get_first_digit(text: str, reversed=True) -> str:
    """
    Returns first numeric value in `text`
    Checks for numeric numbers only
    """
    if reversed:
        text = text[::-1]
    digit = re.search(r"\d", text).group()
    return digit


def get_first_digit_v2(text: str, reversed=False) -> str:
    """
    Returns first numeric value in `text`
    Checks for numeric and spelled numbers
    """

    SPELLED_NUMBERS = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    if reversed:
        text = text[::-1]
        SPELLED_NUMBERS = {k[::-1]: v for k, v in SPELLED_NUMBERS.items()}

    # get first numeric digit
    digit1 = re.search(r"\d", text).group()
    index1 = text.find(digit1)

    # get first spelled digit
    index2 = 1000
    for spelled_number in SPELLED_NUMBERS.keys():
        if (text.find(spelled_number) != -1) & (text.find(spelled_number) < index2):
            index2 = text.find(spelled_number)
            digit2 = SPELLED_NUMBERS[spelled_number]

    # return numeric or spelled digit
    if (index1 < index2) & (index1 != -1):
        return digit1
    else:
        return digit2


if __name__ == "__main__":
    sum_calibration_values = 0

    # import data
    data = read_text_file(filepath="data/day1.txt")

    # process data
    for line in data:
        # get calibration value
        value1 = get_first_digit_v2(line)
        value2 = get_first_digit_v2(line, reversed=True)
        calibration_value = int(value1 + value2)

        # running sum of calibration values
        sum_calibration_values += calibration_value

    print(sum_calibration_values)
