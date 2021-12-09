#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq, Debug

pd = Debug(True)
DAY = 9
SOLVED_1 = True
SOLVED_2 = False


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def make_map(lines):
    return [[int(num) for num in line] for line in lines]


def risk_level(points):
    return sum(points) + len(points)


def find_low_points(height_map):
    result = []
    for y, row in enumerate(height_map):
        for x, height in enumerate(row):
            if y > 0 and height_map[y - 1][x] <= height:
                continue
            if y < len(height_map) - 1 and height_map[y + 1][x] <= height:
                continue
            if x > 0 and height_map[y][x - 1] <= height:
                continue
            if x < len(row) - 1 and height_map[y][x + 1] <= height:
                continue
            result.append(height)
    return result


def test1(data):
    height_map = make_map(data)
    low_points = find_low_points(height_map)
    return risk_level(low_points)


def test2(data):
    return 0


def part1(data):
    return test1(data)


def part2(data):
    return None


if __name__ == '__main__':

    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 15, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 42, test_input_1)
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
