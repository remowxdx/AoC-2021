#!/usr/bin/env python3

from aoc import *
import cairo

pd = Debug(True)
DAY = 6
SOLVED_1 = True
SOLVED_2 = True


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def make_population(data):
    population = [0] * 9
    for fish in data[0].split(','):
        population[int(fish)] += 1
    return population


def step(population):
    new_population = [0] * 9
    for fish in range(9):
        if fish == 0:
            new_population[8] += population[0]
            new_population[6] += population[0]
        else:
            new_population[fish - 1] += population[fish]
    return new_population


def draw_graph(name, graph):
    surface = cairo.SVGSurface(name, 800, 600)
    ctx = cairo.Context(surface)

    scale_x = (800 - 100) / len(graph)
    scale_y = (600 - 100) / max(graph)

# Draw axis
    ctx.move_to(50, 600 - 50)
    ctx.line_to(800 - 50, 600 - 50)
    ctx.stroke()
    ctx.move_to(50, 600 - 50)
    ctx.line_to(50, 50)
    ctx.stroke()

    ctx.set_source_rgb(1.0, 0.0, 0.0)
    ctx.move_to(50, 600 - 50)
    for x, y in enumerate(graph):
        ctx.line_to(50 + x * scale_x, 600 - 50 - y * scale_y)
    ctx.stroke()

    surface.flush()
    surface.finish()


def pop_after(data, days):
    population = make_population(data)
    graph = [sum(population)]
    pd(population)
    for day in range(days):
        population = step(population)
        graph.append(sum(population))
    pd(population)
    draw_graph(f'images/day6_{days}.svg', graph)
    return sum(population)


def test1(data):
    return pop_after(data, 80)


def test2(data):
    return pop_after(data, 256)


def part1(data):
    return pop_after(data, 80)


def part2(data):
    return pop_after(data, 256)


if __name__ == '__main__':

    test_input_1 = get_input('ex6')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 5934, test_input_1)
    print()

    test_input_2 = get_input('ex6')
    print('Test Part 2:')
    test_eq('Test 2.1', test2, 26984457539, test_input_2)
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
