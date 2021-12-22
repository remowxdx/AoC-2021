#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 22


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def read_instructions(lines):
    instructions = []
    for line in lines:
        instruction, coords = line.split(' ')
        ranges = coords.split(',')
        bounds = [range_.split('=')[1] for range_ in ranges]
        coords = [tuple(int(num) for num in bound.split('..')) for bound in bounds]
        instructions.append((
            instruction,
            coords[0], coords[1], coords[2]))
    return instructions


def execute_instruction(cubes, instruction):
    print('+', instruction)
    if instruction[0] == 'on':
        for x in range(instruction[1][0], instruction[1][1] + 1):
            if abs(x) > 50:
                break
            for y in range(instruction[2][0], instruction[2][1] + 1):
                if abs(y) > 50:
                    break
                for z in range(instruction[3][0], instruction[3][1] + 1):
                    if abs(z) > 50:
                        break
                    cubes.add((x, y, z))
    else:
        for x in range(instruction[1][0], instruction[1][1] + 1):
            if abs(x) > 50:
                break
            for y in range(instruction[2][0], instruction[2][1] + 1):
                if abs(y) > 50:
                    break
                for z in range(instruction[3][0], instruction[3][1] + 1):
                    if abs(z) > 50:
                        break
                    if (x, y, z) in cubes:
                        cubes.remove((x, y, z))
    return cubes


def execute(cubes, instructions):
    for instruction in instructions:
        execute_instruction(cubes, instruction)
    return cubes


def part1(data):
    instructions = read_instructions(data)
    print("\n".join([str(instruction) for instruction in instructions]))
    cubes = execute(set(), instructions)
    return len(cubes)


def part2(data):
    return None


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 590784, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 42, test_input_1)
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
    # run_part2(False)


if __name__ == '__main__':
    main()
