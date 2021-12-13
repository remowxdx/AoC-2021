#!/usr/bin/env python3

import cairo
from aoc import check_solution, save_solution, test_eq

DAY = 13


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def paper_and_instructions(lines):
    paper = set()
    instructions = []
    status = 'dots'
    for line in lines:
        if len(line) == 0:
            status = 'folds'
            continue

        if status == 'dots':
            x_s, y_s = line.split(',')
            paper.add((int(x_s), int(y_s)))

        elif status == 'folds':
            direction, n_s = line[11:].split('=')
            instructions.append((direction, int(n_s)))
    return paper, instructions


def fold_vert(paper, y_fold):
    folded_paper = set()
    for x, y in paper:
        if y > y_fold:
            folded_paper.add((x, 2 * y_fold - y))
        else:
            folded_paper.add((x, y))
    return folded_paper


def fold_horiz(paper, x_fold):
    folded_paper = set()
    for x, y in paper:
        if x > x_fold:
            folded_paper.add((2 * x_fold - x, y))
        else:
            folded_paper.add((x, y))
    return folded_paper


def part1(data):
    paper, instructions = paper_and_instructions(data)
    # print(paper)
    # print(instructions)
    for instruction in instructions[:1]:
        if instruction[0] == 'x':
            paper = fold_horiz(paper, instructions[0][1])
        elif instruction[0] == 'y':
            paper = fold_vert(paper, instructions[0][1])
        else:
            raise Exception(f'Unknown fold ({instruction[0]}).')
    return len(paper)


def paper_str(paper):
    max_x = max_y = 0
    for x, y in paper:
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    lines = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            if (x, y) in paper:
                row.append('X')
            else:
                row.append(' ')
        lines.append(row)
    return "\n" + "\n".join(["".join(row) for row in lines])


def paper_size(paper):
    max_x = max_y = 0
    for x, y in paper:
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    return max_x, max_y


def draw_paper(ctx, offset_x, offset_y, scale, paper, instruction):
    width, height = paper_size(paper)

    ctx.set_source_rgb(0.9, 0.9, 0.7)
    ctx.rectangle(
        offset_x * scale,
        offset_y * scale,
        (width + 1) * scale,
        (height + 1) * scale)
    ctx.fill()

    ctx.set_source_rgb(1.0, 0.0, 0.0)
    for x, y in paper:
        ctx.rectangle(
            (offset_x + x) * scale,
            (offset_y + y) * scale,
            scale,
            scale)
    ctx.fill()

    if instruction:
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        if instruction[0] == 'x':
            for y in range(1, height + 1, 2):
                ctx.rectangle(
                    (offset_x + instruction[1]) * scale + 1,
                    (offset_y + y) * scale + 1,
                    scale - 2,
                    scale - 2)
        if instruction[0] == 'y':
            for x in range(1, width + 1, 2):
                ctx.rectangle(
                    (offset_x + x) * scale + 1,
                    (offset_y + instruction[1]) * scale + 1,
                    scale - 2,
                    scale - 2)
        ctx.fill()

    ctx.set_line_width(1)
    ctx.set_source_rgb(0.0, 0.0, 0.0)
    ctx.rectangle(
        offset_x * scale,
        offset_y * scale,
        (width + 1) * scale,
        (height + 1) * scale)
    ctx.stroke()
    return width, height


def draw_instructions(folding, instructions):
    scale = 8
    size = [0, 0]
    for paper in folding:
        max_x, max_y = paper_size(paper)
        size[0] += max_x + 3
        size[1] = max(max_y + 2, size[1])
    surface = cairo.SVGSurface(
        'images/day13.svg',
        size[0] * scale,
        (size[1] + 2) * scale)
    ctx = cairo.Context(surface)
    offset_x = 1
    step = 0
    instructions.append(None)
    for paper in folding:
        delta_x, _ = draw_paper(
            ctx,
            offset_x, 1,
            scale,
            paper,
            instructions[step])
        offset_x += delta_x + 3
        step += 1
    surface.flush()
    surface.finish()


def part2(data):
    paper, instructions = paper_and_instructions(data)
    # print(paper)
    # print(instructions)
    folding = [paper, ]
    for instruction in instructions:
        if instruction[0] == 'x':
            folding.append(fold_horiz(folding[-1], instruction[1]))
        elif instruction[0] == 'y':
            folding.append(fold_vert(folding[-1], instruction[1]))
        else:
            raise Exception(f'Unknown fold ({instruction[0]}).')

    draw_instructions(folding, instructions)

    return paper_str(folding[-1])


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 17, test_input_1)
    print()

    print('Test Part 2:')
    result = '''
XXXXX
X   X
X   X
X   X
XXXXX'''
    test_eq('Test 2.1', part2, result, test_input_1)
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
    # run_part1(True)
    run_part2(True)


if __name__ == '__main__':
    main()
