#!/usr/bin/env python3

import math
from aoc import check_solution, save_solution, test_eq

DAY = 17


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def read_target_area(lines):
    _, area = lines[0].split(': ')
    xx_range, yy_range = area.split(', ')
    _, x_range = xx_range.split('=')
    left_s, right_s = x_range.split('..')
    left, right = int(left_s), int(right_s)

    _, y_range = yy_range.split('=')
    bottom_s, top_s = y_range.split('..')
    bottom, top = int(bottom_s), int(top_s)
    return left, top, right, bottom


def step(x, y, vx, vy):
    x += vx
    y += vy
    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1
    vy -= 1
    return x, y, vx, vy


def hits(vx, vy, area):
    x, y = 0, 0
    max_y = 0
    while x <= area[2] and y >= area[3]:
        if x >= area[0] and y <= area[1]:
            return True, max_y
        x, y, vx, vy = step(x, y, vx, vy)
        if y > max_y:
            max_y = y
    return False, max_y


def part1(data):
    area = read_target_area(data)
    max_y = 0
# v_x² + v_x - 2*a_0 >= 0
# (-v_x +- sqrt(v_x² - 4*2*a_0)) / 2
    min_vx = math.floor((-1 + math.sqrt(1 + 4 * 2 * area[0])) / 2)
    print(min_vx, area[2] + 1, area[1] - area[3])
    for vx in range(min_vx, area[2] + 1):
        for vy in range(0, -area[3]):
            ok, cur_max_y = hits(vx, vy, area)
            if ok and cur_max_y > max_y:
                max_y = cur_max_y
            print(vx, vy, cur_max_y)
    return max_y


def part2(data):
    return None


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 45, test_input_1)
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
