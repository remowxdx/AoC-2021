#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 2
SOLVED_1 = False
SOLVED_2 = False


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def move_submarine(data):
    position = [0, 0]
    for step in data:
        command, s_length = step.split()
        length = int(s_length)
        if command == 'forward':
            position[0] += length
        elif command == 'down':
            position[1] += length
        elif command == 'up':
            position[1] -= length
        else:
            raise InvalidArgument
    return position


def real_move_submarine(data):
    position = [0, 0, 0]
    for step in data:
        command, s_length = step.split()
        length = int(s_length)
        if command == 'forward':
            position[0] += length
            position[1] += length * position[2]
        elif command == 'down':
            position[2] += length
        elif command == 'up':
            position[2] -= length
        else:
            raise InvalidArgument
    return position


def test1(data):
    result = move_submarine(data)
    return result[0] * result[1]


def test2(data):
    result = real_move_submarine(data)
    return result[0] * result[1]

def part1(data):
    result = move_submarine(data)
    return result[0] * result[1]

def part2(data):
    result = real_move_submarine(data)
    return result[0] * result[1]

if __name__ == '__main__':

    test_input_1 = get_input('ex2')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 150, test_input_1)
    print()

    test_input_2 = get_input('ex2')
    print('Test Part 2:')
    test_eq('Test 2.1', test2, 900, test_input_2)
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
