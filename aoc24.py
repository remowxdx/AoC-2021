#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 24


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def read_instructions(lines):
    instructions = []
    for line in lines:
        instructions.append(line.split())
    return instructions


def make_alu(model):
    model_input = []
    for _ in range(14):
        model, rem = divmod(model, 10)
        model_input.append(rem)
    alu = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0,
        'input': model_input,
    }
    return alu


def next_input(alu):
    return alu['input'].pop()


def step(alu, instruction):
    if instruction[0] == 'inp':
        alu[instruction[1]] = next_input(alu)
        return alu

    if instruction[2] in ['w', 'x', 'y', 'z']:
        val = alu[instruction[2]]
    else:
        val = int(instruction[2])

    if instruction[0] == 'add':
        alu[instruction[1]] += val
    elif instruction[0] == 'mul':
        alu[instruction[1]] *= val
    elif instruction[0] == 'div':
        alu[instruction[1]] //= val
    elif instruction[0] == 'mod':
        alu[instruction[1]] %= val
    elif instruction[0] == 'eql':
        if alu[instruction[1]] == val:
            alu[instruction[1]] = 1
        else:
            alu[instruction[1]] = 0
    else:
        raise RuntimeError(f'Unknown instruction {instruction}.')
    return alu


def is_valid(model, program):
    alu = make_alu(model)
    for digit in alu['input']:
        if digit == 0:
            alu['z'] = 99999999999999
            return alu
    for instruction in program:
        step(alu, instruction)
    return alu


def part1(data):
    print()
    monad = read_instructions(data)

    model = 13579246899999
    valid = is_valid(model, monad)
    print(model, valid)

    # model = 99489458991739
    model = 29599469991739
    min_z = 99999999999999
    valid = is_valid(model, monad)
    print(model, valid)

    for p in range(14):
        for q in range(p + 1, 14):
            for d in range(9):
                for e in range(9):
                    model_num = model - d * 10 ** p - e * 10 ** q
                    alu = is_valid(model_num, monad)
                    if min_z is None or alu['z'] < min_z:
                        min_z = alu['z']
                        print(model_num, alu['z'])


    if False:
        # model = 99_999_999_999_999
        # model = 99999984149880
        # model = 88888884148880
        # modelv = 29599458991739
        # modelv = 29599469991739
        model = 77777774148880
        found = False
        min_z = None
        while not found:
            alu = is_valid(model, monad)
            if min_z is None or alu['z'] < min_z:
                min_z = alu['z']
                print(alu, model)

            found = alu['z'] == 0
            if model % 1000 == 0:
                print(model)
            model -= 1
    return model + 1


def part2(data):
    print()
    monad = read_instructions(data)

    # model = 99489458991739
    model = 17153114691118
    valid = is_valid(model, monad)
    print(model, valid)

    for p in range(14):
        for q in range(p + 1, 14):
            for d in range(9):
                for e in range(9):
                    model_num = model - d * 10 ** p - e * 10 ** q
                    alu = is_valid(model_num, monad)
                    if alu['z'] == 0:
                        print(model_num, alu['z'])
    return None


def run_tests():
    test_input_1 = get_input(f'input{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, True, test_input_1)
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
    # run_part1(False)
    # run_part2(False)


if __name__ == '__main__':
    main()
