#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 4
SOLVED_1 = True
SOLVED_2 = True


def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    return lines.splitlines()


def drawn_numbers(line):
    return [int(num) for num in line.split(',')]


def given_boards(data):
    boards = []
    board = []
    for line in data:
        if line == '':
            boards.append(board)
            board = []
            continue
        board.append([int(num) for num in line.split()])
    boards.append(board)
    # print(boards)
    return boards


def play(draws, boards):
    for num in draws:
        # print(num)
        for board in boards:
            if mark_number(board, num):
                return board, num
    return 0


def play2(draws, boards):
    remaining = len(boards)
    winner = set()
    for num in draws:
        print(num)
        for b, board in enumerate(boards):
            if b in winner:
                continue
            if mark_number(board, num):
                remaining -= 1
                winner.add(b)
                if remaining == 0:
                    return board, num
    return 0


def winner(board, row, col):
    row_win = True
    for n in board[row]:
        if n != -1:
            row_win = False
            break
    if row_win:
        return True

    col_win = True
    for line in board:
        if line[col] != -1:
            col_win = False
            break
    return col_win


def calc_result(board):
    total = 0
    for line in board:
        for num in line:
            if num != -1:
                total += num
    return total


def mark_number(board, num):
    for row, line in enumerate(board):
        for col, n in enumerate(line):
            if n == num:
                line[col] = -1
                if winner(board, row, col):
                    return True
            
    return False


def test1(data):
    nums = drawn_numbers(data[0])
    boards = given_boards(data[2:])
    board, num = play(nums, boards)
    # print(board, num)
    # print(boards)
    return calc_result(board) * num


def test2(data):
    nums = drawn_numbers(data[0])
    boards = given_boards(data[2:])
    remaining = len(boards)
    board, num = play2(nums, boards)
    print(board, num)
    # print(boards)
    return calc_result(board) * num


def part1(data):
    return test1(data)


def part2(data):
    return test2(data)


if __name__ == '__main__':

    test_input_1 = get_input('ex4')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 4512, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 1924, test_input_1)
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
