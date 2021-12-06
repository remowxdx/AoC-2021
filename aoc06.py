#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 6
SOLVED_1 = True
SOLVED_2 = False


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def make_population(data):
    population = [0] * 9
    for fish in data[0].split(','):
        population[int(fish)] += 1
    return population


def step(population):
    new_population = [0] * 9
    for fish in range(9):
        if fish == 0:
            new_population[8] += population[0]
            new_population[6] += population[0]
        else:
            new_population[fish - 1] += population[fish]
    return new_population


def test1(data):
    population = make_population(data)
    pd(population)
    for day in range(80):
        population = step(population)
    pd(population)
    return sum(population)


def test2(data):
    return 0


def part1(data):
    return test1(data)


def part2(data):
    return None


if __name__ == '__main__':

    test_input_1 = get_input('ex6')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 5934, test_input_1)
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
