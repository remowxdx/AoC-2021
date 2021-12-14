#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 14


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def template_and_rules(lines):
    template = list(lines[0])

    rules = {}
    skip = True
    for line in lines:
        if skip:
            if len(line) == 0:
                skip = False
            continue

        pair, insertion = line.split(' -> ')
        rules[pair] = insertion

    return template, rules


def apply_rules(polymer, rules):
    new_polymer = []
    for i in range(len(polymer) - 1):
        new_polymer.append(polymer[i])
        pair = polymer[i] + polymer[i + 1]
        if pair in rules:
            new_polymer.append(rules[pair])
    new_polymer.append(polymer[i + 1])
    return new_polymer


def count_elements(polymer):
    count = {}
    for element in polymer:
        if element not in count:
            count[element] = 0
        count[element] += 1
    return count


def part1(data):
    polymer, rules = template_and_rules(data)
    for _ in range(10):
        polymer = apply_rules(polymer, rules)
    count = count_elements(polymer)
    return max(count.values()) - min(count.values())


def part2(data):
    return None


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 1588, test_input_1)
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
