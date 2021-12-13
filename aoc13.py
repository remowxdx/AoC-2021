#!/usr/bin/env python3

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
            if (x,y) in paper:
                row.append('X')
            else:
                row.append(' ')
        lines.append(row)
    return "\n" + "\n".join(["".join(row) for row in lines]) 


def part2(data):
    paper, instructions = paper_and_instructions(data)
    # print(paper)
    # print(instructions)
    for instruction in instructions:
        if instruction[0] == 'x':
            paper = fold_horiz(paper, instruction[1])
        elif instruction[0] == 'y':
            paper = fold_vert(paper, instruction[1])
        else:
            raise Exception(f'Unknown fold ({instruction[0]}).')
    s = paper_str(paper)
    return s


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 17, test_input_1)
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
    run_part2(False)


if __name__ == '__main__':
    main()
