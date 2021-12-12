#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 12


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def part1(data):
    return None


def part2(data):
    return None


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    test_input_2 = get_input(f'ex{DAY}b')
    test_input_3 = get_input(f'ex{DAY}c')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 10, test_input_1)
    test_eq('Test 1.2', part1, 19, test_input_2)
    test_eq('Test 1.3', part1, 226, test_input_3)
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
    # run_part1(False)
    # run_part2(False)


if __name__ == '__main__':
    main()
