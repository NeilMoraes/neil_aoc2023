# --- Day 6: Wait For It ---
# Level 0
# Part 1: 3316275
# Part 2: 27102791

from functools import reduce


def count_ways_to_win(time, distance):
    wins = 0
    for time_charged in range(1, time):
        if ((time - time_charged) * time_charged) > distance:
            wins += 1
    return wins


if __name__ == "__main__":
    # Q1
    data = [(40, 233), (82, 1011), (84, 1110), (92, 1487)]
    wins_list = []
    for race in data:
        time, distance = race
        wins = count_ways_to_win(time, distance)
        wins_list.append(wins)
    print("Q1:", reduce(lambda x, y: x * y, wins_list))

    # Q2
    data = [(40828492, 233101111101487)]
    wins_list = []
    for race in data:
        time, distance = race
        wins = count_ways_to_win(time, distance)
        wins_list.append(wins)
    print("Q2:", reduce(lambda x, y: x * y, wins_list))
