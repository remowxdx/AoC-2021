#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 11
SOLVED_1 = True
SOLVED_2 = True


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


class OctopusCave:
    """
        The Octupus Cave
    """

    def __init__(self, lines):
        self.cave = self.parse(lines)
        self.flashes = 0
        self.num_step = 0

    @staticmethod
    def parse(lines):
        cave = []
        for line in lines:
            cave.append([int(c) for c in line])
        return cave

    def update(self):
        flashes = []
        for y, row in enumerate(self.cave):
            for x, _energy in enumerate(row):
                self.cave[y][x] += 1
                if self.cave[y][x] == 10:
                    flashes.append((y, x))
        return flashes

    def neighbors(self, y, x):
        for neighbor_y in range(y - 1, y + 2):
            for neighbor_x in range(x - 1, x + 2):
                if neighbor_x == x and neighbor_y == y:
                    continue
                if neighbor_y < 0 or neighbor_y >= len(self.cave):
                    continue
                if neighbor_x < 0 or neighbor_x >= len(self.cave[neighbor_y]):
                    continue
                yield neighbor_y, neighbor_x

    def do_flashes(self, flashes):
        for y, x in flashes:
            for neighbor_y, neighbor_x in self.neighbors(y, x):
                self.cave[neighbor_y][neighbor_x] += 1
                if self.cave[neighbor_y][neighbor_x] == 10:
                    flashes.append((neighbor_y, neighbor_x))
        return flashes

    def reset_flashed(self, flashes):
        for y, x in flashes:
            self.cave[y][x] = 0
        self.flashes += len(flashes)
        return len(flashes)

    def step(self):
        self.num_step += 1
        flashes = self.update()
        flashes = self.do_flashes(flashes)
        num_flashed = self.reset_flashed(flashes)
        return num_flashed

    def __str__(self):
        return f'Step {self.num_step}:\n' + "\n".join(
            ["".join(
                [str(octopus) for octopus in row]
            ) for row in self.cave])


def test1(data):
    cave = OctopusCave(data)
    while cave.num_step < 100:
        cave.step()
    return cave.flashes


def test2(data):
    cave = OctopusCave(data)
    while cave.step() < 100:
        pass
    return cave.num_step


def part1(data):
    return test1(data)
    # return None


def part2(data):
    return test2(data)
    # return None


def main():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 1656, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 195, test_input_1)
    print()

    data = get_input(f'input{DAY}')

    result1 = part1(data)
    if result1 is not None:
        print('Part 1:', result1)
        if SOLVED_1:
            check_solution(DAY, 1, result1)
        else:
            save_solution(DAY, 1, result1)

    result2 = part2(data)
    if result2 is not None:
        print('Part 2:', result2)
        if SOLVED_2:
            check_solution(DAY, 2, result2)
        else:
            save_solution(DAY, 2, result2)


if __name__ == '__main__':
    main()
