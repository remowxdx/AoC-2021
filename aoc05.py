#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 5
SOLVED_1 = False
SOLVED_2 = False


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def parse_input(lines):
    result = []
    max_x = 0
    max_y = 0
    for line in lines:
        pos0, pos1 = line.split(' -> ')
        x0, y0 = [int(coord) for coord in pos0.split(',')]
        x1, y1 = [int(coord) for coord in pos1.split(',')]
        max_x = max(max_x, x0)
        max_x = max(max_x, x1)
        max_y = max(max_y, y0)
        max_y = max(max_y, y1)
        result.append(((x0, y0), (x1, y1)))
    return result, max_x, max_y


def is_horizontal(line):
    if line[0][0] == line[1][0]:
        return True
    return False


def is_vertical(line):
    if line[0][1] == line[1][1]:
        return True
    return False


def print_board(board):
    pd("Board:")
    for line in board:
        pd("".join([str(v) for v in line]))


def draw_lines(lines, max_x, max_y):
    board = [[0] * (max_x+1) for y in range(max_y+1)]
    for line in lines:
        if is_vertical(line):
            y = line[0][1]
            x0 = min(line[0][0], line[1][0])
            x1 = max(line[0][0], line[1][0])
            for x in range(x0, x1 + 1):
                board[y][x] += 1
        if is_horizontal(line):
            x = line[0][0]
            y0 = min(line[0][1], line[1][1])
            y1 = max(line[0][1], line[1][1])
            for y in range(y0, y1 + 1):
                board[y][x] += 1
    return board


def count_dangers(board):
    count = 0
    for row in board:
        for vents in row:
            if vents > 1:
                count += 1
    return count


def test1(data):
    vent_lines, max_x, max_y = parse_input(data)
    board = draw_lines(vent_lines, max_x, max_y)
    return count_dangers(board)


def test2(data):
    return 0


def part1(data):
    return test1(data)


def part2(data):
    return None


if __name__ == '__main__':

    test_input_1 = get_input('ex5')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 5, test_input_1)
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
