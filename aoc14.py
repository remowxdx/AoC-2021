#!/usr/bin/env python3

import cairo
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
        result.setdefault(pair, 0)
        result[pair] += 1
    return result


def apply_rules(polymer, rules):
    new_polymer = {}
    for pair, count in polymer.items():
        if pair in rules:
            first = pair[0]
            second = pair[1]
            middle = rules[pair]
            new_polymer.setdefault(first + middle, 0)
            new_polymer.setdefault(middle + second, 0)
            new_polymer[first + middle] += count
            new_polymer[middle + second] += count
        else:
            new_polymer.setdefault(pair, 0)
            new_polymer[pair] += count
    return new_polymer


def count_elements(polymer):
    counts = {}
    for pair, count in polymer.items():
        for i in range(2):
            if pair[i] == '_':
                continue
            counts.setdefault(pair[i], 0)
            counts[pair[i]] += count
    for element in counts:
        counts[element] //= 2
    return counts


def part1(data):
    slow_polymer, rules = template_and_rules(data)
    polymer = fast_polymer(slow_polymer)
    for _ in range(10):
        polymer = apply_rules(polymer, rules)
    counts = count_elements(polymer)
    return max(counts.values()) - min(counts.values())


def add_counts(polymer, counts_history, step):
    counts = count_elements(polymer)
    for element, count in counts.items():
        counts_history.setdefault(element, [0] * step)
        counts_history[element].append(count)


def letter_to_color(letter):
    num = ord(letter) - ord('A')
    intensity, color = divmod(num, 6)
    shade = intensity / 5
    colors = [
        (1.0 - shade, 1.0 - shade, 0.0),
        (1.0 - shade, 0.0, 1.0 - shade),
        (0.0, 1.0 - shade, 1.0 - shade),
        (0.0, 1.0 - shade, 0.0),
        (1.0 - shade, 0.0, 0.0),
        (0.0, 0.0, 1.0 - shade),
    ]
    return colors[color]


def draw_history(ctx, history, element, max_y):
    scale_x = 650 / len(history)
    scale_y = 500 / max_y
    ctx.set_line_width(1)
    ctx.set_source_rgb(*letter_to_color(element))
    ctx.move_to(50, 550 - history[0] * scale_y)
    for step, y in enumerate(history):
        if y == 0:
            y = 1
        ctx.line_to(50 + step * scale_x, 550 - y * scale_y)
    ctx.stroke()
    ctx.move_to(620, 548 - y * scale_y)
    ctx.show_text(f'{element} - {y}')


def max_count(counts_history):
    return max([max(count) for count in counts_history.values()])


def draw_counts(counts_history):
    surface = cairo.SVGSurface('images/day14.svg', 800, 600)
    ctx = cairo.Context(surface)
    ctx.select_font_face(
        'Sans Serif',
        cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(14)

    # Axis
    ctx.set_source_rgb(0.9, 0.9, 0.8)
    ctx.rectangle(40, 40, 670, 520)
    ctx.fill()
    ctx.set_source_rgb(0.0, 0.0, 0.0)
    ctx.move_to(50, 50)
    ctx.line_to(50, 550)
    ctx.line_to(700, 550)
    ctx.stroke()

    max_y = max_count(counts_history)

    for element, history in counts_history.items():
        draw_history(ctx, history, element, max_y)

    surface.flush()
    surface.finish()


def part2(data):
    counts_history = {}
    slow_polymer, rules = template_and_rules(data)
    polymer = fast_polymer(slow_polymer)
    add_counts(polymer, counts_history, 0)
    for step in range(40):
        polymer = apply_rules(polymer, rules)
        add_counts(polymer, counts_history, step + 1)
    counts = count_elements(polymer)
    draw_counts(counts_history)
    return max(counts.values()) - min(counts.values())


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
