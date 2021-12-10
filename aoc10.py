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


class IncompleteChunk(Exception):
    def __init__(self, msg, missing_closer):
        super().__init__(self, msg)
        self.missing_closer = missing_closer


class IllegalCloser(Exception):
    def __init__(self, msg, illegal_closer):
        super().__init__(self, msg)
        self.illegal_closer = illegal_closer


def parse_chunk_list(text):
    if len(text) == 0:
        return [], None, []

    if text[0] not in ENCLOSERS.keys():
        raise Exception(f'Expected opener, found {text[0]}.')

    chunk = {}
    chunk['opener'] = text[0]
    closer = ENCLOSERS[text[0]]
    chunk['content'] = []
    completed = []

    rest = text[1:]

    if len(rest) == 0:
        chunk['closer'] = closer
        completed.append(closer)
        return chunk, rest, completed

    while rest[0] in ENCLOSERS.keys():
        content, rest, compl = parse_chunk_list(rest)
        completed.extend(compl)
        chunk['content'].append(content)
        if len(rest) == 0:
            chunk['closer'] = closer
            completed.append(closer)
            return chunk, rest, completed

    if rest[0] == closer:
        chunk['closer'] = rest[0]
        return chunk, rest[1:], completed
    if rest[0] in ENCLOSERS.values():
        raise IllegalCloser(
            f"Expected {ENCLOSERS[chunk['opener']]}, found {rest[0]} {rest}.",
            rest[0])
    raise Exception('Invalid character')


def test1(data):
    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    score = 0
    for line in data:
        try:
            chunk, rest, completed = parse_chunk_list(line)
        except IllegalCloser as e:
            score += points[e.illegal_closer]
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
        try:
            completed = []
            rest = line
            while len(rest) > 0:
                chunk, rest, compl = parse_chunk_list(rest)
                completed.extend(compl)
            print(line, completed)
            score = 0
            for closer in completed:
                score = score * 5 + points[closer]
            scores.append(score)
        except IllegalCloser as e:
            pass
    sorted_scores = sorted(scores)
    print(scores)
    print(sorted_scores)
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
