#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 21


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def players_start_positions(lines):
    players = []
    for line in lines:
        _, pos = line.split(': ')
        players.append([int(pos), 0])
    return players


def roll(step):
    return 9 * step + 6


def step_player(player, step):
    player[0] = (player[0] + roll(step) - 1) % 10 + 1
    player[1] += player[0]


def part1(data):
    players = players_start_positions(data)
    current_player = 0
    step = 0
    while True:
        step_player(players[current_player], step)
        wins = players[current_player][1] >= 1_000
        current_player = (current_player + 1) % 2
        if wins:
            break
        # print(players)
        step += 1
    return players[current_player][1] * (step + 1) * 3


def part2(data):
    return None


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 739_785, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 42, test_input_1)
    print()


def run_part1(solved):
    data = get_input(f'input{DAY}')

    result1 = part1(data)
    print('Part 1:', result1)
    if solved:
        check_solution(DAY, 1, result1)
    else:
        save_solution(DAY, 1, result1)


def run_part2(solved):
    data = get_input(f'input{DAY}')

    result2 = part2(data)
    print('Part 2:', result2)
    if solved:
        check_solution(DAY, 2, result2)
    else:
        save_solution(DAY, 2, result2)


def main():
    run_tests()
    run_part1(True)
    # run_part2(False)


if __name__ == '__main__':
    main()
