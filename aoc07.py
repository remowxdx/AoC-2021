#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 7
SOLVED_1 = True
SOLVED_2 = False


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def get_positions(lines):
    return [int(pos) for pos in lines[0].split(',')]


def fuel_cost(target, positions):
    result = 0
    for position in positions:
        result += abs(position - target)
    return result


def fuel_cost2(target, positions):
    result = 0
    for position in positions:
        dist = abs(position - target)
        result += dist * (dist + 1) // 2
    return result


def test1(data):
    positions = get_positions(data)
    costs = [fuel_cost(x, positions) for x in range(max(positions))]
    return min(costs)


def test2(data):
    positions = get_positions(data)
    costs = [fuel_cost2(x, positions) for x in range(max(positions))]
    return min(costs)


def part1(data):
    positions = get_positions(data)
    costs = [fuel_cost(x, positions) for x in range(max(positions))]
    return min(costs)


def part2(data):
    positions = get_positions(data)
    costs = [fuel_cost2(x, positions) for x in range(max(positions))]
    return min(costs)


if __name__ == '__main__':

    test_input_1 = get_input('ex7')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 37, test_input_1)
    print()

    test_input_2 = get_input('ex7')
    print('Test Part 2:')
    test_eq('Test 2.1', test2, 168, test_input_2)
    print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        if SOLVED_1:
            check_solution(DAY, 1, r)
        else:
            save_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        if SOLVED_2:
            check_solution(DAY, 2, r)
        else:
            save_solution(DAY, 2, r)
