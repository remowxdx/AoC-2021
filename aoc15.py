#!/usr/bin/env python3

import cairo
from heapq import heappush, heappop
from aoc import check_solution, save_solution, test_eq

DAY = 15


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def make_cavern(lines):
    cavern = []
    for row in lines:
        cavern.append([int(risk_level) for risk_level in row])
    return cavern


def risk_of(cavern, path):
    total_risk = 0
    for pos in path:
        total_risk += cavern[pos[0]][pos[1]]
    return total_risk


def find_neighbors(cavern, pos):
    neighbors = []
    end = (len(cavern) - 1, len(cavern[0]) - 1)
    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        neighbor = (pos[0] + direction[0], pos[1] + direction[1])
        if neighbor[0] >= 0 and neighbor[1] >= 0:
            if neighbor[0] <= end[0] and neighbor[1] <= end[1]:
                neighbors.append((
                    (end[0] - neighbor[0]) ** 2 + (end[1] - neighbor[1]) ** 2,
                    neighbor))
    return [pos for dist, pos in sorted(neighbors, key=lambda el: el[0])]


def find_lowest_risk_neighbor(lowest_risks, pos):
    neighbors = []
    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        neighbor = (pos[0] + direction[0], pos[1] + direction[1])
        if neighbor[0] >= 0 and neighbor[1] >= 0:
            if neighbor in lowest_risks:
                neighbors.append(neighbor)
    return min(neighbors, key=lambda nb: lowest_risks[nb])


def find_lowest_risks(cavern, start):

    lowest_risks = {start: 0}
    to_visit = []
    heappush(to_visit, (0, start))

    while len(to_visit) > 0:
        total_risk, pos = heappop(to_visit)
        for neighbor in find_neighbors(cavern, pos):
            neighbor_total_risk = cavern[neighbor[0]][neighbor[1]] + total_risk
            if neighbor not in lowest_risks:
                lowest_risks[neighbor] = neighbor_total_risk
                heappush(to_visit, (neighbor_total_risk, neighbor))
                continue
            if lowest_risks[neighbor] > neighbor_total_risk:
                lowest_risks[neighbor] = neighbor_total_risk
                heappush(to_visit, (neighbor_total_risk, neighbor))
                continue
    return lowest_risks


def make_big_cavern(small_cavern):
    cavern = []
    for j in range(5):
        for row in small_cavern:
            cavern_row = []
            for i in range(5):
                for risk in row:
                    cavern_row.append((risk + i + j - 1) % 9 + 1)
            cavern.append(cavern_row)
    return cavern


def draw_cavern(cavern, lowest_risks):
    width, height = len(cavern[0]), len(cavern)
    surface = cairo.SVGSurface('images/day15.svg', width, height)
    ctx = cairo.Context(surface)

    max_risk = max(lowest_risks.values())
    for y in range(height):
        for x in range(width):
            risk = lowest_risks[(y, x)] / max_risk
            ctx.set_source_rgb(risk, 0.0, 1.0 - risk)
            ctx.rectangle(x, y, 1, 1)
            ctx.fill()

    ctx.set_source_rgb(0.0, 0.0, 0.0)
    pos = (height - 1, width - 1)
    while pos != (0, 0):
        ctx.rectangle(pos[1], pos[0], 1, 1)
        pos = find_lowest_risk_neighbor(lowest_risks, pos)
    ctx.fill()


    surface.write_to_png('images/day15.png')
    surface.flush()
    surface.finish()


def part1(data):
    cavern = make_cavern(data)
    lowest_risks = find_lowest_risks(cavern, (0, 0))
    return lowest_risks[len(cavern) - 1, len(cavern[0]) - 1]


def part2(data):
    small_cavern = make_cavern(data)
    cavern = make_big_cavern(small_cavern)
    lowest_risks = find_lowest_risks(cavern, (0, 0))
    draw_cavern(cavern, lowest_risks)
    return lowest_risks[len(cavern) - 1, len(cavern[0]) - 1]


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 40, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 315, test_input_1)
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
    run_part2(True)


if __name__ == '__main__':
    main()
