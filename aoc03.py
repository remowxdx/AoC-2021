#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 3
SOLVED_1 = True
SOLVED_2 = True


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def most_common(lines):
    most_commons = [0] * len(lines[0])
    one_counts = [0] * len(lines[0])
    for line in lines:
        for i, digit in enumerate(line):
            if digit == '1':
                one_counts[i] += 1

    for i, count in enumerate(one_counts):
        if count > len(lines) / 2:
            most_commons[i] = 1
    return most_commons


def most_common_2(remaining, bit):
    one_count = 0
    for line in remaining:
        if line[bit] == '1':
            one_count += 1
    if one_count >= len(remaining) / 2:
        return '1'
    return '0'


def rates(lines):
    gamma_rate = most_common(lines)

    epsilon_rate = [0] * len(lines[0])
    for i, most_comm in enumerate(gamma_rate):
        epsilon_rate[i] = 1 - most_comm

    gr = 0
    for digit in gamma_rate:
        gr = gr * 2 + digit

    er = 0
    for digit in epsilon_rate:
        er = er * 2 + digit

    return gr, er


def count_bit(num1, num2):
    count = 0
    while int(num1[count]) == num2[count]:
        count += 1
    return count


def test1(data):
    gamma_rate, epsilon_rate = rates(data)
    return gamma_rate * epsilon_rate


def oxy_rate(data):
    remaining = data[:]
    bit = 0
    while len(remaining) > 1:
        next_round = []
        most_comm = most_common_2(remaining, bit)
        for line in remaining:
            if line[bit] == most_comm:
                next_round.append(line)
        bit += 1
        remaining = next_round
    oxy = 0
    for digit in remaining[0]:
        oxy *= 2
        if digit == '1':
            oxy += 1
    return oxy


def co2_rate(data):
    remaining = data[:]
    bit = 0
    while len(remaining) > 1:
        next_round = []
        most_comm = most_common_2(remaining, bit)
        for line in remaining:
            if line[bit] != most_comm:
                next_round.append(line)
        bit += 1
        remaining = next_round
    co2 = 0
    for digit in remaining[0]:
        co2 *= 2
        if digit == '1':
            co2 += 1
    return co2


def test2(data):
    oxy = oxy_rate(data)
    co2 = co2_rate(data)
    print(oxy, co2)
    return oxy * co2


def part1(data):
    gamma_rate, epsilon_rate = rates(data)
    return gamma_rate * epsilon_rate


def part2(data):
    return test2(data)


if __name__ == '__main__':

    test_input_1 = get_input('ex3')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 198, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 230, test_input_1)
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
