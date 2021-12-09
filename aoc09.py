#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq, Debug

pd = Debug(True)
DAY = 9
SOLVED_1 = True
SOLVED_2 = True


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def make_map(lines):
    return [[int(num) for num in line] for line in lines]


def risk_level(height_map, points):
    return sum([height_map[point[0]][point[1]] for point in points]) + len(points)


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
            result.append((y, x))
    return result


def test1(data):
    height_map = make_map(data)
    low_points = find_low_points(height_map)
    return risk_level(height_map, low_points)


def find_basin_size(height_map, low_point):
    points = [low_point]
    index = 0
    count = 1
    while index < len(points):
        y, x = points[index]
        index += 1
        if height_map[y][x] == 9:
            count -= 1
            continue
        if y > 0 and (y - 1, x) not in points:
            points.append((y - 1, x))
            count += 1
        if y < len(height_map) - 1 and (y + 1, x) not in points:
            points.append((y + 1, x))
            count += 1
        if x > 0 and (y, x - 1) not in points:
            points.append((y, x - 1))
            count += 1
        if x < len(height_map[y]) - 1 and (y, x + 1) not in points:
            points.append((y, x + 1))
            count += 1
    print('LP:', low_point, count)
    return count


def find_basin_sizes(height_map, low_points):
    result = []
    for low_point in low_points:
        result.append(find_basin_size(height_map, low_point))
    return result


def test2(data):
    height_map = make_map(data)
    low_points = find_low_points(height_map)
    product = 1
    for size in sorted(find_basin_sizes(height_map, low_points))[-3:]:
        product *= size
    return product


def part1(data):
    return test1(data)


def part2(data):
    return test2(data)


if __name__ == '__main__':

    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 15, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 1134, test_input_1)
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
