#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 25


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def read_map(lines):
    east = set()
    south = set()
    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            if cell == 'v':
                south.add((x, y))
            elif cell == '>':
                east.add((x, y))
    return len(lines[0]), len(lines), east, south


def print_map(width, height, east, south):
    for y in range(height):
        for x in range(width):
            if (x, y) in east:
                print('>', end='')
            elif (x, y) in south:
                print('v', end='')
            else:
                print('.', end='')
        print()
    print()


def step_east(width, east, south):
    moved = False
    next_east = set()
    for x, y in east:
        next_pos = ((x + 1) % width, y)
        if next_pos not in east and next_pos not in south:
            next_east.add(next_pos)
            moved = True
        else:
            next_east.add((x, y))

    return moved, next_east


def step_south(height, east, south):
    moved = False
    next_south = set()
    for x, y in south:
        next_pos = (x, (y + 1) % height)
        if next_pos not in east and next_pos not in south:
            next_south.add(next_pos)
            moved = True
        else:
            next_south.add((x, y))

    return moved, next_south


def step(width, height, east, south):
    moved_east, next_east = step_east(width, east, south)
    moved_south, next_south = step_south(height, next_east, south)
    return moved_east or moved_south, next_east, next_south


def part1(data):
    width, height, east, south = read_map(data)
    print(width, height, east, south)
    print_map(width, height, east, south)
    step_num = 0
    moved = True
    while moved:
        step_num += 1
        moved, east, south = step(width, height, east, south)
        # print_map(width, height, east, south)
    return step_num


def part2(data):
    return None


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 58, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 42, test_input_1)
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
    # run_part2(False)


if __name__ == '__main__':
    main()
