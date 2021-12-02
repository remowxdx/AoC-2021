#!/usr/bin/env python3

from aoc import *

import cairo

pd = Debug(True)
DAY = 2
SOLVED_1 = True
SOLVED_2 = True


class Command:
    def __init__(self, command):
        self.command = command
        direction, s_length = command.split()
        self.direction = direction
        self.length = int(s_length)


class Submarine:
    def __init__(self):
        self.horizontal = 0
        self.depth = 0
        self.history = [(0, 0)]

    def do_step(self, command):
        if command.direction == 'forward':
            self.horizontal += command.length
        elif command.direction == 'down':
            self.depth += command.length
        elif command.direction == 'up':
            self.depth -= command.length
        else:
            raise InvalidArgument
        self.history.append((self.horizontal, self.depth))

    def summary(self):
        return self.depth * self.horizontal

    def __str__(self):
        return f'Submarine is at position {self.horizontal} and depth {self.depth}'

    def __rshift__(self, step):
        self.do_step(step)


class RealSubmarine(Submarine):
    def __init__(self):
        super().__init__()
        self.aim = 0

    def do_step(self, command):
        if command.direction == 'forward':
            self.horizontal += command.length
            self.depth += self.aim * command.length
        elif command.direction == 'down':
            self.aim += command.length
        elif command.direction == 'up':
            self.aim -= command.length
        else:
            raise InvalidArgument
        self.history.append((self.horizontal, self.depth))


class SubmarineTracer:
    def __init__(self, name):
        self.name = name

    def paint(self, points):
        xs = [x for x, y in points]
        ys = [y for x, y in points]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)

        surface = cairo.SVGSurface(f"{self.name}.svg", max_x - min_x, max_y - min_y)
        context = cairo.Context(surface)
        context.set_line_width(1.0)
        context.move_to(xs[0], ys[0])
        for x, y in points:
            context.line_to(x, y)
        context.stroke()


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def test1(data):
    s = Submarine()
    for line in data:
        s >> Command(line)
    return s.summary()


def test2(data):
    s = RealSubmarine()
    for line in data:
        s >> Command(line)
    return s.summary()


def part1(data):
    s = Submarine()
    for line in data:
        s >> Command(line)
    st = SubmarineTracer("day2_1")
    st.paint(s.history)
    return s.summary()


def part2(data):
    s = RealSubmarine()
    for line in data:
        s >> Command(line)
    st = SubmarineTracer("day2_2")
    st.paint(s.history)
    return s.summary()


if __name__ == '__main__':

    test_input_1 = get_input('ex2')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 150, test_input_1)
    print()

    test_input_2 = get_input('ex2')
    print('Test Part 2:')
    test_eq('Test 2.1', test2, 900, test_input_2)
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
