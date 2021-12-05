#!/usr/bin/env python3

from aoc import *
import cairo

pd = Debug(True)
DAY = 1
SOLVED_1 = True
SOLVED_2 = True

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return [int(line) for line in lines.splitlines()]

def test1(data):
    return part1(data)

def test2(data):
    return part2(data)

def part1(data):
    increments = 0
    prev_depth = data[0]
    for depth in data:
        if depth > prev_depth:
            increments += 1
        prev_depth = depth
    return increments

def part2(data):
    window_width = 3
    increments = 0
    prev_depth_sum = 0
    depth_sum = 0
    for i, depth in enumerate(data):
        if i < window_width:
            depth_sum += depth
            continue
        depth_sum += depth - data[i - window_width]
        if depth_sum > prev_depth_sum:
            increments += 1
        prev_depth_sum = depth_sum
    return increments


def draw(depths, img):
    surface = cairo.SVGSurface(img, len(depths) + 1, max(depths))
    ctx = cairo.Context(surface)

    ctx.set_line_width(1)
    ctx.move_to(0, depths[0])
    for x, depth in enumerate(depths):
        ctx.line_to(x, depth)
    ctx.stroke()

    ctx.set_source_rgba(0, 1.0, 0, 0.7)
    ctx.move_to(0, depths[0])
    for x in range(1, len(depths) - 1):
        ctx.line_to(x, sum(depths[x-1:x+2]) / 3)
    ctx.stroke()

    surface.finish()


if __name__ == '__main__':

    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 7, test_input_1)
    print()

    test_input_2 = get_input(f'ex{DAY}')
    print('Test Part 2:')
    test_eq('Test 2.1', test2, 5, test_input_2)
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

    draw(data, 'images/day1.svg')
