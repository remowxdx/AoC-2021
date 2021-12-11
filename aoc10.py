#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq, Debug

pd = Debug(True)
DAY = 10
SOLVED_1 = True
SOLVED_2 = True


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


ENCLOSERS = {'(': ')', '[': ']', '{': '}', '<': '>'}


def parse_chunk(text):
    chunk_stack = []
    for char in text:
        if char in ENCLOSERS.keys():
            chunk_stack.append(char)
            continue
        if char in ENCLOSERS.values():
            last = chunk_stack.pop()
            if char == ENCLOSERS[last]:
                continue
            return chunk_stack, char, f'Mismatch'
        return chunk_stack, char, 'Illegal'
    if len(chunk_stack) == 0:
        return chunk_stack, None, 'OK'
    return chunk_stack, None, 'Incomplete'


def test1(data):
    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    score = 0
    for line in data:
        chunk_stack, char, msg = parse_chunk(line)
        if msg == 'Mismatch':
            score += points[char]
    return score


def test2(data):
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    scores = []
    for line in data:
        chunk_stack, _, msg = parse_chunk(line)
        if msg == 'Incomplete':
            score = 0
            while len(chunk_stack) > 0:
                closer = ENCLOSERS[chunk_stack.pop()]
                score = score * 5 + points[closer]
            scores.append(score)
    sorted_scores = list(sorted(scores))
    return sorted_scores[(len(scores) - 1) // 2]


def part1(data):
    return test1(data)


def part2(data):
    return test2(data)


if __name__ == '__main__':

    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 26397, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 288957, test_input_1)
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
