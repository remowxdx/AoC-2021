#!/usr/bin/env python3

import cairo
from aoc import check_solution, save_solution, test_eq, Debug

pd = Debug(True)
DAY = 8
SOLVED_1 = True
SOLVED_2 = True


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
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


def draw_digit(ctx, digit, x, y):
    segments = {
        'a': ((1, 0), (9, 0)),
        'b': ((0, 1), (0, 9)),
        'c': ((10, 1), (10, 9)),
        'd': ((1, 10), (9, 10)),
        'e': ((0, 11), (0, 19)),
        'f': ((10, 11), (10, 19)),
        'g': ((1, 20), (9, 20)),
    }

    ctx.set_line_width(1)
    for segment in digit:
        line = segments[segment]
        ctx.move_to(x + line[0][0], y + line[0][1])
        ctx.line_to(x + line[1][0], y + line[1][1])
        ctx.stroke()
    return x + 14, y


def draw_display(ctx, display, x, y):
    pos = (x, y)
    for digit in display:
        pos = draw_digit(ctx, digit, pos[0], pos[1])
    return pos


def draw_arrow(ctx, x, y):
    ctx.move_to(x + 1, y + 10)
    ctx.line_to(x + 16, y + 10)
    ctx.move_to(x + 5, y + 5)
    ctx.line_to(x + 16, y + 10)
    ctx.line_to(x + 5, y + 15)
    ctx.stroke()
    return x + 20, y


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
    for _, outputs in notes:
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


def perm_wirings(base, rests):
    if len(rests) == 0:
        return [base]

    result = []
    for rest in rests:
        next_base = base[:]
        next_base.append(rest)
        next_rests = rests[:]
        next_rests.remove(rest)
        result.extend(perm_wirings(next_base, next_rests))
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
    count = count_output_digits_with_len(notes, [
        lens[1],
        lens[4],
        lens[7],
        lens[8]
    ])
    return count


def test2(data):
    notes = parse_notes(data)
    total = 0
    x = 10
    y = 10
    surface = cairo.SVGSurface('images/day8_2.svg', 150, 24 * len(notes) + 20)
    ctx = cairo.Context(surface)
    for signals, digits in notes:
        wiring = find_wiring(signals)
        real_digits = decode_display(digits, wiring)
        ctx.set_source_rgb(1.0, 0.0, 0.0)
        x, y = draw_display(ctx, digits, x, y)
        ctx.set_source_rgb(0.0, 0.0, 0.0)
        x, y = draw_arrow(ctx, x, y)
        ctx.set_source_rgb(0.0, 1.0, 0.0)
        x, y = draw_display(ctx, real_digits, x, y)
        total += to_number(real_digits)
        y += 24
        x = 10
    surface.flush()
    surface.finish()
    return total


def part1(data):
    return test1(data)


def part2(data):
    return test2(data)


def run_tests():
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


def run_days(input_file):
    data = get_input(input_file)

    result = part1(data)
    if result is not None:
        print('Part 1:', result)
        if SOLVED_1:
            check_solution(DAY, 1, result)
        else:
            save_solution(DAY, 1, result)

    result = part2(data)
    if result is not None:
        print('Part 2:', result)
        if SOLVED_2:
            check_solution(DAY, 2, result)
        else:
            save_solution(DAY, 2, result)


if __name__ == '__main__':

    run_tests()

    run_days(f'input{DAY}')
