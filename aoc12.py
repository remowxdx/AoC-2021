#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 12


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def make_caves(lines):
    caves = {}
    for line in lines:
        from_, to = line.split('-')
        if from_ not in caves:
            caves[from_] = []
        if to not in caves:
            caves[to] = []
        caves[from_].append(to)
        caves[to].append(from_)
    return caves


def find_paths(caves, from_, to, visited):

    if from_ == to:
        return [[from_, ], ]

    if from_.islower():
        new_visited = visited.copy()
        new_visited.add(from_)
    else:
        new_visited = visited

    new_paths = []
    for next_ in caves[from_]:

        if next_ in visited:
            continue

        for path in find_paths(caves, next_, to, new_visited):
            new_path = path[:]
            new_path.append(from_)
            new_paths.append(new_path)
    return new_paths


def find_paths_2(caves, from_, to, visited, jolly):

    if from_ == to:
        return [[from_, ], ]

    if from_.islower():
        new_visited = visited.copy()
        new_visited.add(from_)
    else:
        new_visited = visited

    new_paths = []
    for next_ in caves[from_]:
        new_jolly = jolly
        if next_ in visited:
            if new_jolly is None and next_ not in ['start', 'end']:
                new_jolly = next_
            else:
                continue

        for path in find_paths_2(caves, next_, to, new_visited, new_jolly):
            new_path = path[:]
            new_path.append(from_)
            new_paths.append(new_path)

    return new_paths


def part1(data):
    caves = make_caves(data)
    paths = find_paths(caves, 'start', 'end', set())
    return len(paths)


def part2(data):
    caves = make_caves(data)
    paths = find_paths_2(caves, 'start', 'end', set(), None)
    # print("\n".join(sorted([",".join(reversed(path)) for path in paths])))
    return len(paths)


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
    test_eq('Test 2.1', part2, 36, test_input_1)
    test_eq('Test 2.2', part2, 103, test_input_2)
    test_eq('Test 2.3', part2, 3509, test_input_3)
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
