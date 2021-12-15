#!/usr/bin/env python3

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
    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if new_pos[0] >= 0 and new_pos[1] >= 0:
            if new_pos[0] < len(cavern[0]) and new_pos[1] < len(cavern):
                neighbors.append(new_pos)
    return neighbors


def find_lowest_risks(cavern, start):

    lowest_risks = {}
    to_visit = [(start, 0)]

    while len(to_visit) > 0:
        pos, total_risk = to_visit.pop(0)
        # pos_risk = cavern[pos[0]][pos[1]]

        for neighbor in find_neighbors(cavern, pos):
            neighbor_risk = cavern[neighbor[0]][neighbor[1]]
            if neighbor not in lowest_risks or lowest_risks[neighbor] > neighbor_risk + total_risk:
                lowest_risks[neighbor] = neighbor_risk + total_risk
                to_visit.append((neighbor, neighbor_risk + total_risk))
    return lowest_risks


def part1(data):
    cavern = make_cavern(data)
    lowest_risks = find_lowest_risks(cavern, (0, 0))
    return lowest_risks[len(cavern) - 1, len(cavern[0]) - 1]


def part2(data):
    return None


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 40, test_input_1)
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
