#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq, Debug

pd = Debug(True)
DAY = 11
SOLVED_1 = True
SOLVED_2 = True


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def parse_cave(lines):
    cave = []
    for line in lines:
        cave.append([int(c) for c in line])
    return cave


def update(cave):
    flashes = []
    for y, row in enumerate(cave):
        for x, octopus in enumerate(row):
            cave[y][x] += 1
            if cave[y][x] == 10:
                flashes.append((y, x))
    return flashes


def do_flashes(cave, flashes):
    neighbors = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        ]
    for y, x in flashes:
        for dy, dx in neighbors:
            nx = x + dx
            ny = y + dy
            if nx < 0 or ny < 0 or nx >= len(cave[y]) or ny >= len(cave):
                continue
            cave[ny][nx] += 1
            if cave[ny][nx] == 10:
                flashes.append((ny, nx))
    return flashes


def reset_flashed(cave, flashes):
    for y, x in flashes:
        cave[y][x] = 0
    return len(flashes)


def step(cave):
    flashes = update(cave)
    flashes = do_flashes(cave, flashes)
    num_flashed = reset_flashed(cave, flashes)
    return num_flashed


def print_cave(cave):
    for row in cave:
        print("".join([str(octopus) for octopus in row]))


def test1(data):
    cave = parse_cave(data)
    flashes = 0
    for i in range(100):
        flashes += step(cave)
    return flashes


def test2(data):
    cave = parse_cave(data)
    i = 1
    while step(cave) < 100:
        i += 1
    return i


def part1(data):
    return None
    return test1(data)


def part2(data):
    return None
    return test2(data)


if __name__ == '__main__':

    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 1656, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 195, test_input_1)
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
