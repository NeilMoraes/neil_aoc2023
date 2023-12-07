# --- Day 4: Scratchcards ---
# Level 2
# Part 1: 24733
# Part 2: 5422730

from typing import List


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip() for line in f.readlines()]
    return data


def get_valid_card_numbers(scratchcards: List[str]) -> List[int]:
    """Return list of valid card numbers"""
    valid_numbers = []
    for scratchcard in scratchcards:
        valid_numbers.append(int(scratchcard.split(":")[0].split()[1]))
    return valid_numbers


def get_winning_numbers(scratchcard: str) -> List[int]:
    """Return list of winning numbers from scratchcard"""
    return [int(x) for x in scratchcard.split(":")[1].split("|")[0].split()]


def get_selected_numbers(scratchcard: str) -> List[int]:
    """Return list of selected numbers from scratchcard"""
    return [int(x) for x in scratchcard.split(":")[1].split("|")[1].split()]


def calc_score(winning_numbers: List[int], selected_numbers: List[int]) -> int:
    count_winning_numbers = len(set(winning_numbers).intersection(selected_numbers))

    if count_winning_numbers == 0:
        score = 0
    elif count_winning_numbers == 1:
        score = 1
    else:
        score = 2 ** (count_winning_numbers - 1)
    return score


def calc_score_v2(winning_numbers: List[int], selected_numbers: List[int]) -> int:
    count_winning_numbers = len(set(winning_numbers).intersection(selected_numbers))
    return count_winning_numbers


if __name__ == "__main__":
    total_score = 0
    total_cards = 0

    # import data
    scratchcards = read_text_file(filepath="data/day4.txt")

    # Q1
    for scratchcard in scratchcards:
        winning_numbers = get_winning_numbers(scratchcard)
        selected_numbers = get_selected_numbers(scratchcard)
        score = calc_score(winning_numbers, selected_numbers)
        total_score += score

    # Q2
    valid_cards = get_valid_card_numbers(scratchcards)
    copied_cards = {}

    # play original cards
    for counter, scratchcard in enumerate(scratchcards):
        card_number = counter + 1
        winning_numbers = get_winning_numbers(scratchcard)
        selected_numbers = get_selected_numbers(scratchcard)
        num_copies_won = calc_score_v2(winning_numbers, selected_numbers)

        # update copied cards (after playing original)
        for i in range(1, num_copies_won + 1):
            if (card_number + i) in valid_cards:
                if (card_number + i) in copied_cards:
                    copied_cards[card_number + i] = copied_cards[card_number + i] + 1
                else:
                    copied_cards[card_number + i] = 1

        # play all copies of the original card
        if card_number in copied_cards:
            for play_number in range(copied_cards[card_number]):
                winning_numbers = get_winning_numbers(scratchcard)
                selected_numbers = get_selected_numbers(scratchcard)
                num_copies_won = calc_score_v2(winning_numbers, selected_numbers)

                # update copied cards (after playing copy)
                for i in range(1, num_copies_won + 1):
                    if (card_number + i) in valid_cards:
                        if (card_number + i) in copied_cards:
                            copied_cards[card_number + i] = (
                                copied_cards[card_number + i] + 1
                            )
                        else:
                            copied_cards[card_number + i] = 1

    # total cards - original + copies
    total_cards = len(valid_cards) + sum(copied_cards.values())

    print("Q1:", total_score)
    print("Q2:", total_cards)
