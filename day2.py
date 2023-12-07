# --- Day 2: Cube Conundrum ---
# Level 2
# Part 1: 2551
# Part 2: 62811

from typing import List, Tuple

STARTING_CUBES = {"red": 12, "green": 13, "blue": 14}


def read_text_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        data = [line.strip() for line in f.readlines()]
    return data


def analyse_game(text: str) -> Tuple[str, List[str]]:
    """Split text into game and rounds"""
    game = text.split(":")[0]
    rounds = text.split(":")[1].split(";")
    return game, rounds


def aggregate_round(round_text: str) -> dict[str, int]:
    """Returns aggregated totals for a round for each color"""
    round_totals = {"red": 0, "green": 0, "blue": 0}

    for color in round_totals.keys():
        if round_text.find(color) != -1:
            draws = round_text.split(",")

            if isinstance(draws, list):
                round_totals[color] = sum(
                    [
                        int(draw.strip().split()[0])
                        for draw in draws
                        if draw.find(color) != -1
                    ]
                )
            else:
                round_totals[color] = int(draws.split()[0])
    return round_totals


def is_valid_round(round_totals: dict) -> bool:
    """Checks if totals for a round are valid (as specified in STARTING_CUBES)"""
    for color, total in round_totals.items():
        if total > STARTING_CUBES[color]:
            return False
    return True


def is_valid_game(rounds) -> bool:
    """Checks if game is valid"""
    for round in rounds:
        round_totals = aggregate_round(round)
        if not is_valid_round(round_totals):
            return False
    return True


def calc_power_of_cubes(rounds) -> bool:
    """Calculates power for minimum required cubes, red * blue * green"""
    min_required_cubes = {"red": 0, "green": 0, "blue": 0}
    for round in rounds:
        round_totals = aggregate_round(round)
        for color in min_required_cubes.keys():
            min_required_cubes[color] = max(
                [min_required_cubes[color], round_totals[color]]
            )
    return (
        min_required_cubes["red"]
        * min_required_cubes["green"]
        * min_required_cubes["blue"]
    )


if __name__ == "__main__":
    valid_games = []
    sum_of_valid_game_ids = 0
    sum_of_power_of_cubes = 0

    # import data
    data = read_text_file(filepath="data/day2.txt")

    # process games
    for text in data:
        game, rounds = analyse_game(text)
        if is_valid_game(rounds):
            valid_games.append(game)

        sum_of_power_of_cubes += calc_power_of_cubes(rounds)

    # Q1 - sum of valid games
    sum_of_valid_game_ids = sum([int(game.split()[1]) for game in valid_games])
    print("Q1:", sum_of_valid_game_ids)

    # Q2 - power of minimum cubes required to play
    print("Q2:", sum_of_power_of_cubes)
