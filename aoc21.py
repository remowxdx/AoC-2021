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
    player[0] = (player[0] + step - 1) % 10 + 1
    player[1] += player[0]


def roll_player(player, step):
    step_player(player, roll(step))


def player_wins_1000(player):
    return player[1] >= 1_000


def next_player(cur_player):
    return 1 - cur_player


def step_dirac(game, step):
    player = game[4]
    np = 1 - player
    if player == 0:
        npos = (game[0] + step) % 10 + 1
        return (npos, game[1], game[2] + npos, game[3], np)
    npos = (game[1] + step) % 10 + 1
    return (game[0], npos, game[2], game[3] + npos, np)


def add_state(states, game, num):
    if game not in states:
        states[game] = 0
    states[game] += num


def won(game):
    return game[2] >= 21 or game[3] >= 21


def count_wins(states):
    wins1 = wins2 = 0
    for game in states:
        if game[2] >= 21:
            wins1 += states[game]
        if game[3] >= 21:
            wins2 += states[game]
    return wins1, wins2


def dirac(start_game):
    states = {}
    todo = set()
    add_state(states, start_game, 1)
    todo.add(start_game)
    while len(todo) > 0:
        # print(len(todo), len(states))
        game = todo.pop()
        num_state = states[game]
        states[game] = 0
        for roll1 in range(3):
            for roll2 in range(3):
                for roll3 in range(3):
                    next_game = step_dirac(game, roll1 + roll2 + roll3 + 2)
                    add_state(states, next_game, num_state)
                    if not won(next_game):
                        todo.add(next_game)
    # print(sorted(states.items(), key=lambda x: x[1]))
    return count_wins(states)


def part1(data):
    players = players_start_positions(data)
    current_player = 0
    step = 0
    print(players)
    while True:
        roll_player(players[current_player], step)
        wins = player_wins_1000(players[current_player])
        current_player = next_player(current_player)
        step += 1
        if wins:
            break
        print(players)
    return players[current_player][1] * step * 3


def part2(data):
    players = players_start_positions(data)
    game = (players[0][0], players[1][0], players[0][1], players[1][1], 0)
    print(game)
    wins = dirac(game)
    print(wins)
    return max(wins)


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 739_785, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 444356092776315, test_input_1)
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
    run_part2(True)


if __name__ == '__main__':
    main()
