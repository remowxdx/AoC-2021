#!/usr/bin/env python3

import cairo
import math

from aoc import check_solution, save_solution, test_eq

DAY = 12


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def make_caves(lines):
    caves = {}
    for line in lines:
        from_, to = line.split('-')
        if from_ not in caves:
            caves[from_] = []
        if to not in caves:
            caves[to] = []
        caves[from_].append(to)
        caves[to].append(from_)
    return caves


def link_force(caves_pos, from_, to):
    from_pos = caves_pos[from_][0]
    to_pos = caves_pos[to][0]
    delta_pos = (from_pos[0] - to_pos[0], from_pos[1] - to_pos[1])
    d = math.sqrt(delta_pos[0] ** 2 + delta_pos[1] ** 2)

    if d == 0:
        return (0, 0)

    g = 1.0
    l = 40
    k = 0.1
    pos_force = (delta_pos[0] / d ** 1 * g, delta_pos[1] / d ** 1 * g)

    if to in caves_pos[from_][2]:
        link_force = (k * delta_pos[0] * (l - d) / d, k * delta_pos[1] * (l - d) / d)
    else:
        link_force = (0, 0)

    force = sum_forces(pos_force, link_force)
    return force


def sum_forces(force1, force2):
    return (force1[0] + force2[0], force1[1] + force2[1])


def move_caves(caves):
    caves_pos = {}
    cols = int(math.sqrt(len(caves)))
    x = 0
    y = 0
    for cave, links in caves.items():
        if cave == 'start':
            caves_pos[cave] = ((50, 300), (0, 0), links)
        elif cave == 'end':
            caves_pos[cave] = ((750, 300), (0, 0), links)
        else:
            caves_pos[cave] = ((100 + x * 50, 50 + y * 50), (0.1, 0), links)
        y += 1
        if y > cols:
            y = 0
            x += 1

    moving = True
    while moving:
        moving = False
        new_caves_pos = {}
        for cave, pos_links in caves_pos.items():
            if cave in ['start', 'end']:
                new_caves_pos[cave] = pos_links
                continue
            pos, vel, links = pos_links
            force = (0, 0)
            for cave_1 in caves:
                if cave == cave_1:
                    continue
                force = sum_forces(force, link_force(caves_pos, cave, cave_1))
            dt = 0.1
            damp = 0.99
            if vel[0] ** 2 + vel[1] ** 2 > 0.001:
                moving = True
            new_vel = (damp * vel[0] + force[0] * dt, damp * vel[1] + force[1] * dt)
            new_pos = (pos[0] + new_vel[0] * dt, pos[1] + new_vel[1] * dt)
            new_caves_pos[cave] = (new_pos, new_vel, links)
        caves_pos = new_caves_pos

    return caves_pos


def draw_caves(caves):
    surface = cairo.SVGSurface('images/day12.svg', 800, 600)
    ctx = cairo.Context(surface)

    ctx.select_font_face("Sans Serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(10)

    caves_pos = move_caves(caves)
    left = right = caves_pos['start'][0][0]
    top = bottom = caves_pos['start'][0][1]
    for cave, pos_links in caves_pos.items():
        pos, _vel, links = pos_links
        if pos[0] < left:
            left = pos[0]
        if pos[0] > right:
            right = pos[0]
        if pos[1] < top:
            top = pos[1]
        if pos[1] > bottom:
            bottom = pos[1]
    print(left, right, top, bottom)

    ctx.set_source_rgb(0.0, 0.0, 1.0)
    for cave, pos_links in caves_pos.items():
        pos, vel, links = pos_links
        for link in links:
            ctx.move_to(pos[0], pos[1])
            ctx.line_to(caves_pos[link][0][0], caves_pos[link][0][1])
        ctx.stroke()

    ctx.set_source_rgb(1.0, 0.0, 0.0)
    for cave, pos_links in caves_pos.items():
        pos, vel, links = pos_links
        if cave.islower():
            radius = 10
        else:
            radius = 20
        ctx.arc(pos[0], pos[1], radius, 0, 2 * math.pi)
        ctx.fill()

    ctx.set_source_rgb(1.0, 0.0, 0.0)
    for cave, pos_links in caves_pos.items():
        pos, vel, links = pos_links
        ctx.set_source_rgb(0.0, 0.0, 0.0)
        if cave.islower():
            up = 12
        else:
            up = 20
        ctx.move_to(pos[0] - 8, pos[1] - up)
        ctx.show_text(cave)

    surface.flush()
    surface.finish()


def find_paths(caves, from_, to, visited):

    if from_ == to:
        return [[from_, ], ]

    if from_.islower():
        new_visited = visited.copy()
        new_visited.add(from_)
    else:
        new_visited = visited

    new_paths = []
    for next_ in caves[from_]:

        if next_ in visited:
            continue

        for path in find_paths(caves, next_, to, new_visited):
            new_path = path[:]
            new_path.append(from_)
            new_paths.append(new_path)
    return new_paths


def find_paths_2(caves, from_, to, visited, jolly):

    if from_ == to:
        return [[from_, ], ]

    if from_.islower():
        new_visited = visited.copy()
        new_visited.add(from_)
    else:
        new_visited = visited

    new_paths = []
    for next_ in caves[from_]:
        new_jolly = jolly
        if next_ in visited:
            if new_jolly is None and next_ not in ['start', 'end']:
                new_jolly = next_
            else:
                continue

        for path in find_paths_2(caves, next_, to, new_visited, new_jolly):
            new_path = path[:]
            new_path.append(from_)
            new_paths.append(new_path)

    return new_paths


def part1(data):
    caves = make_caves(data)
    draw_caves(caves)
    paths = find_paths(caves, 'start', 'end', set())
    return len(paths)


def part2(data):
    caves = make_caves(data)
    paths = find_paths_2(caves, 'start', 'end', set(), None)
    # print("\n".join(sorted([",".join(reversed(path)) for path in paths])))
    return len(paths)


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    test_input_2 = get_input(f'ex{DAY}b')
    test_input_3 = get_input(f'ex{DAY}c')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 10, test_input_1)
    test_eq('Test 1.2', part1, 19, test_input_2)
    test_eq('Test 1.3', part1, 226, test_input_3)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 36, test_input_1)
    test_eq('Test 2.2', part2, 103, test_input_2)
    test_eq('Test 2.3', part2, 3509, test_input_3)
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
