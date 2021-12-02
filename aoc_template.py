#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = %%day%%
SOLVED_1 = False
SOLVED_2 = False


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def test1(data):
    return 0


def test2(data):
    return 0


def part1(data):
    return None


def part2(data):
    return None


if __name__ == '__main__':

    test_input_1 = [1,2,3]
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 42, test_input_1)
    print()

    test_input_2 = [4,5,6]
    print('Test Part 2:')
    test_eq('Test 2.1', test2, 42, test_input_2)
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
