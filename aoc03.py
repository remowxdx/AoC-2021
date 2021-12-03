#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 3
SOLVED_1 = True
SOLVED_2 = False


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def rates(lines):
    one_counts = [0] * len(lines[0])
    for line in lines:
        for i, digit in enumerate(line):
            if digit == '1':
                one_counts[i] += 1
    print(one_counts)

    gamma_rate = [0] * len(lines[0])
    epsilon_rate = [0] * len(lines[0])
    for i, count in enumerate(one_counts):
        if count > len(lines) / 2:
            gamma_rate[i] = 1
        else:
            epsilon_rate[i] = 1

    gr = 0
    for digit in gamma_rate:
        gr = gr * 2 + digit

    er = 0
    for digit in epsilon_rate:
        er = er * 2 + digit

    return gr, er


def test1(data):
    gamma_rate, epsilon_rate = rates(data)
    return gamma_rate * epsilon_rate


def test2(data):
    return 0


def part1(data):
    gamma_rate, epsilon_rate = rates(data)
    return gamma_rate * epsilon_rate


def part2(data):
    return None


if __name__ == '__main__':

    test_input_1 = get_input('ex3')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 198, test_input_1)
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
