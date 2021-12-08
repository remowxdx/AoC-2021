#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 8
SOLVED_1 = True
SOLVED_2 = True


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


DIGITS = [
    'abcefg',  # 0
    'cf',  # 1
    'acdeg',  # 2
    'acdfg',  # 3
    'bcdf',  # 4
    'abdfg',  # 5
    'abdefg',  # 6
    'acf',  # 7
    'abcdefg',  # 8
    'abcdfg',  # 9
    ]


def digit_lens():
    return [len(digit) for digit in DIGITS]


def parse_notes(lines):
    result = []
    for line in lines:
        signal, output = line.split(' | ')
        signals = signal.split()
        outputs = output.split()
        result.append((signals, outputs))
    return result


def count_output_digits_with_len(notes, lens):
    count = 0
    for signals, outputs in notes:
        for digit in outputs:
            if len(digit) in lens:
                count += 1
    return count


def decode(signal, wiring):
    result = []
    for digit in signal:
        result.append(wiring[ord(digit) - ord('a')])
    return ''.join(sorted(result))


def try_wiring(wiring, signals):
    for signal in signals:
        if decode(signal, wiring) not in DIGITS:
            return False
    return True


def perm_wirings(base, rest):
    if len(rest) == 0:
        return [base]

    result = []
    for r in rest:
        next_base = base[:]
        next_base.append(r)
        next_rest = rest[:]
        next_rest.remove(r)
        result.extend(perm_wirings(next_base, next_rest))
    return result


def make_wirings():
    digits = list('abcdefg')
    return perm_wirings([], digits)


def find_wiring(signals):
    wirings = make_wirings()
    for wiring in wirings:
        if try_wiring(wiring, signals):
            return wiring
    return 'No'


def decode_display(outputs, wiring):
    display = []
    for output in outputs:
        display.append(decode(output, wiring))
    return display


def to_number(digits):
    number = 0
    for digit in digits:
        for num, repre in enumerate(DIGITS):
            if digit == repre:
                number = number * 10 + num
    return number


def test1(data):
    notes = parse_notes(data)
    lens = digit_lens()
    count = count_output_digits_with_len(notes, [lens[1], lens[4], lens[7], lens[8]])
    return count


def test2(data):
    notes = parse_notes(data)
    total = 0
    for signals, digits in notes:
        wiring = find_wiring(signals)
        real_digits = decode_display(digits, wiring)
        total += to_number(real_digits)
    return total


def part1(data):
    return test1(data)


def part2(data):
    return test2(data)


if __name__ == '__main__':

    test_input_1 = get_input('ex8_1')
    test_input_2 = get_input('ex8_2')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 0, test_input_1)
    test_eq('Test 1.2', test1, 26, test_input_2)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 5353, test_input_1)
    test_eq('Test 2.1', test2, 61229, test_input_2)
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
