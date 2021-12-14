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


def fast_polymer(polymer):
    result = {'_' + polymer[0]: 1, polymer[-1] + '_': 1}
    for i in range(len(polymer) - 1):
        pair = polymer[i] + polymer[i + 1]
        if pair not in result:
            result[pair] = 0
        result[pair] += 1
    return result


def apply_rules(polymer, rules):
    new_polymer = {}
    for pair, count in polymer.items():
        if pair in rules:
            first = pair[0]
            second = pair[1]
            middle = rules[pair]
            if first + middle not in new_polymer:
                new_polymer[first + middle] = 0
            if middle + second not in new_polymer:
                new_polymer[middle + second] = 0
            new_polymer[first + middle] += count
            new_polymer[middle + second] += count
        else:
            if pair not in new_polymer:
                new_polymer[pair] = 0
            new_polymer[pair] += count
    return new_polymer


def count_elements(polymer):
    count = {}
    for pair, num in polymer.items():
        for i in range(2):
            if pair[i] == '_':
                continue
            if pair[i] not in count:
                count[pair[i]] = 0
            count[pair[i]] += num
    for element, num in count.items():
        count[element] //= 2
    return count


def part1(data):
    slow_polymer, rules = template_and_rules(data)
    polymer = fast_polymer(slow_polymer)
    for _ in range(10):
        polymer = apply_rules(polymer, rules)
    count = count_elements(polymer)
    return max(count.values()) - min(count.values())


def part2(data):
    slow_polymer, rules = template_and_rules(data)
    polymer = fast_polymer(slow_polymer)
    for _ in range(40):
        polymer = apply_rules(polymer, rules)
    count = count_elements(polymer)
    return max(count.values()) - min(count.values())


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 1588, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 2188189693529, test_input_1)
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
