# --- Day 7: Camel Cards ---
# Level
# Part 1: 248217452
# Part 2: 245576185

from typing import List, Tuple
import collections


def read_text_file(filepath: str) -> List[Tuple[str, int]]:
    data = []
    with open(filepath, "r") as f:
        raw = [line.strip() for line in f.readlines()]
        for row in raw:
            hand = row.split()[0]
            bid = int(row.split()[1])
            data.append((hand, bid))
    return data


def is_five_of_kind(hand: str):
    return sorted(collections.Counter(hand).values())[-1] == 5


def is_four_of_kind(hand: str):
    return sorted(collections.Counter(hand).values())[-1] == 4


def is_full_house(hand: str):
    counts = sorted(collections.Counter(hand).values())
    three_of_a_kind = counts[-1] == 3
    two_of_a_kind = counts[0] == 2
    return three_of_a_kind & two_of_a_kind


def is_three_of_kind(hand: str):
    counts = sorted(collections.Counter(hand).values())
    three_of_a_kind = counts[-1] == 3
    not_two_of_a_kind = counts[0] != 2
    return three_of_a_kind & not_two_of_a_kind


def is_two_pair(hand: str):
    counts = sorted(collections.Counter(hand).values())
    two_of_a_kind1 = counts[-1] == 2
    two_of_a_kind2 = counts[-2] == 2
    return two_of_a_kind1 & two_of_a_kind2


def is_one_pair(hand: str):
    counts = sorted(collections.Counter(hand).values())
    two_of_a_kind = counts[-1] == 2
    return two_of_a_kind & (counts[-2] == 1)


def is_high_card(hand: str):
    counts = sorted(collections.Counter(hand).values())
    return counts[-1] == 1


def rank_hand(hand):
    if is_five_of_kind(hand):
        return 7
    if is_four_of_kind(hand):
        return 6
    if is_full_house(hand):
        return 5
    if is_three_of_kind(hand):
        return 4
    if is_two_pair(hand):
        return 3
    if is_one_pair(hand):
        return 2
    if is_high_card(hand):
        return 1


def rank_hand_with_joker(hand):
    if "J" not in hand:
        return rank_hand(hand)
    elif set(hand) == {"J"}:
        return 7
    else:
        possible_joker_options = set(hand.replace("J", ""))
        best_rank = 0
        for option in possible_joker_options:
            new_rank = rank_hand(hand.replace("J", option))
            if new_rank > best_rank:
                best_rank = new_rank
        return best_rank


def flatten(l: List[List]) -> List:
    """Flattens nested list"""
    return [y for x in l for y in x]


if __name__ == "__main__":
    # import data

    data = read_text_file(filepath="data/day7.txt")
    print(data)

    # Q1
    rank_counter = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    for hand, bid in data:
        rank_counter[rank_hand(hand)].append((hand, bid))
    print(rank_counter)

    custom_ordering = "123456789TJQKA"  # AKQJT987654321
    for rank in rank_counter.keys():
        rank_counter[rank] = sorted(
            rank_counter[rank],
            key=lambda x: [custom_ordering.index(i) for i in x[0]],
        )

    # rank_list = []
    total_winnings = 0
    print(flatten(rank_counter.values()))
    for i, val in enumerate(flatten(rank_counter.values())):
        total_winnings += (i + 1) * val[1]

    print("Q1:", total_winnings)

    # Q2
    rank_counter = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    for hand, bid in data:
        rank_counter[rank_hand_with_joker(hand)].append((hand, bid))
    print(rank_counter)

    custom_ordering = "J23456789TQKA"  # AKQJT987654321
    for rank in rank_counter.keys():
        rank_counter[rank] = sorted(
            rank_counter[rank],
            key=lambda x: [custom_ordering.index(i) for i in x[0]],
        )

    total_winnings = 0
    print(flatten(rank_counter.values()))
    for i, val in enumerate(flatten(rank_counter.values())):
        total_winnings += (i + 1) * val[1]

    print("Q2:", total_winnings)
