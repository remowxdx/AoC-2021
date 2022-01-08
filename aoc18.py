#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 18


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def add_raw(num1, num2):
    return f'[{num1},{num2}]'


def split(num):
    prev = 0
    value = None
    for i, char in enumerate(num):
        if char in ['[', ',', ']']:
            if value is not None and value > 9:
                half = value // 2
                second_half = value - half
                pair = f'[{half},{second_half}]'
                return num[:i - prev] + pair + num[i:]
            prev = 0
            value = None
        elif char.isdigit():
            prev += 1
            if value is None:
                value = int(char)
            else:
                value = value * 10 + int(char)
        else:
            raise ValueError(f'Unexpected character "{char}".')
    return num


def get_pair_rest(num):
    i = 0
    if num[i] != '[':
        raise ValueError(f'Expected "[", found "{num[i]}".')
    i += 1

    if not num[i].isdigit():
        raise ValueError(f'Expected digit, found "{num[i]}".')
    first = int(num[i])
    i += 1
    while num[i].isdigit():
        first = first * 10 + int(num[i])
        i += 1

    if num[i] != ',':
        raise ValueError(f'Expected ",", found "{num[i]}".')
    i += 1

    if not num[i].isdigit():
        raise ValueError(f'Expected digit, found "{num[i]}".')
    second = int(num[i])
    i += 1
    while num[i].isdigit():
        second = second * 10 + int(num[i])
        i += 1

    if num[i] != ']':
        raise ValueError(f'Expected "]", found "{num[i]}".')
    i += 1

    result = first, second, num[i:]
    # print('get_pair_rest', result, num)
    return result


def add_before(value, num):
    # print('add_before(', value, ', "', num, '")', sep='')
    val = None
    start = len(num)
    for i in reversed(range(len(num))):
        char = num[i]
        if char in ['[', ',', ']']:
            if val is not None:
                return num[:i + 1] + str(val + value) + num[start:]
            start = i
        elif char.isdigit():
            if val is None:
                val = int(char)
            else:
                val = val + int(char) * 10 ** (start - i - 1)
        else:
            raise ValueError(f'Unexpected character "{char}".')
    return num


def add_after(value, num):
    # print('add_after(', value, ', "', num, '")', sep='')
    val = None
    start = 0
    for i, char in enumerate(num):
        if char in ['[', ',', ']']:
            if val is not None:
                return num[:start + 1] + str(val + value) + num[i:]
            start = i
        elif char.isdigit():
            if val is None:
                val = int(char)
            else:
                val = val * 10 + int(char)
        else:
            raise ValueError(f'Unexpected character "{char}".')
    return num


def explode(num):
    level = 0
    for i, char in enumerate(num):
        if char == '[':
            level += 1
        elif char == ']':
            level -= 1
        if level > 4:
            first, second, rest = get_pair_rest(num[i:])
            before = add_before(first, num[:i])
            after = add_after(second, rest)
            return before + '0' + after
    return num


def magnitude(num):
    result, _ = magn_and_rest(num)
    return result


def magn_and_rest(num):
    char = num[0]
    if char == '[':
        first, rest = magn_and_rest(num[1:])
        if rest[0] != ',':
            raise ValueError('Expected ",", but found' + rest[0])
        second, rest = magn_and_rest(rest[1:])
        if rest[0] != ']':
            raise ValueError('Expected "]", but found' + rest[0])
        return 3 * first + 2 * second, rest[1:]
    if char.isdigit():
        return int(char), num[1:]
    raise ValueError(f'Unexpected character "{char}".')


def reduce(num):
    while True:
        # print('->', num)
        exploded = explode(num)
        if exploded != num:
            num = exploded
            continue
        splitted = split(exploded)
        if splitted != exploded:
            num = splitted
            continue
        return splitted


def add(*nums):
    result = nums[0]
    for num in nums[1:]:
        result = reduce(add_raw(result, num))
        # print(result)
    return result


def part1(data):
    sum_ = add(*data)
    return magnitude(sum_)


def part2(data):
    max_sum = 0
    for first in data:
        for second in data:
            if first == second:
                continue
            sum_ = add(first, second)
            magn = magnitude(sum_)
            max_sum = max(max_sum, magn)
    return max_sum


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test raw addition:')
    test_eq('Test ar.1', add_raw, '[[1,2],[[3,4],5]]', '[1,2]', '[[3,4],5]')
    print('Test explode:')
    test_eq('Test e.1', explode, '[[[[0,9],2],3],4]', '[[[[[9,8],1],2],3],4]')
    test_eq('Test e.2', explode, '[7,[6,[5,[7,0]]]]', '[7,[6,[5,[4,[3,2]]]]]')
    test_eq('Test e.3', explode, '[[6,[5,[7,0]]],3]', '[[6,[5,[4,[3,2]]]],1]')
    test_eq('Test e.4', explode, '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]',
            '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
    test_eq('Test e.5', explode, '[[3,[2,[8,0]]],[9,[5,[7,0]]]]',
            '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    print('Test split:')
    test_eq('Test s.1', split, '[[5,5],11]', '[10,11]')
    test_eq('Test s.2', split, '[[5,6],11]', '[11,11]')
    test_eq('Test s.3', split, '[1,[5,6]]', '[1,11]')
    test_eq('Test s.4', split, '[1,[5,6]]', '[1,[5,6]]')
    print('Test magnitude:')
    test_eq('Test m.0', magnitude, 29, '[9,1]')
    test_eq('Test m.1', magnitude, 143, '[[1,2],[[3,4],5]]')
    test_eq('Test m.2', magnitude, 1384, '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
    test_eq('Test m.3', magnitude, 445, '[[[[1,1],[2,2]],[3,3]],[4,4]]')
    test_eq('Test m.4', magnitude, 791, '[[[[3,0],[5,3]],[4,4]],[5,5]]')
    test_eq('Test m.5', magnitude, 1137, '[[[[5,0],[7,4]],[5,5]],[6,6]]')
    test_eq('Test m.6', magnitude, 3488,
            '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] ')
    print('Test reduce:')
    test_eq('Test r.0', reduce, '[9,1]', '[9,1]')
    print('Test addition:')
    test_eq('Test a.0', add, '[[1,2],[[3,4],5]]', '[1,2]', '[[3,4],5]')
    test_eq('Test a.1', add, '[[[[1,1],[2,2]],[3,3]],[4,4]]',
            '[1,1]', '[2,2]', '[3,3]', '[4,4]')
    test_eq('Test a.2', add, '[[[[3,0],[5,3]],[4,4]],[5,5]]',
            '[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]')
    test_eq('Test a.3', add, '[[[[5,0],[7,4]],[5,5]],[6,6]]',
            '[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]', '[6,6]')
    test_eq('Test a.4', add, '[[[[5,0],[7,4]],[5,5]],[6,6]]',
            '[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]', '[6,6]')
    test_eq('Test a.5', add,
            '[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]',
            '[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]',
            '[2,9]')
    test_input_a6 = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''.splitlines()
    # print(test_input_a6)
    test_eq('Test a.6', add,
            '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]',
            *test_input_a6)
    test_input_a7 = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''.splitlines()
    # print(test_input_a7)
    test_eq('Test a.7', add,
            '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]',
            *test_input_a7)

    print('Test Part 1:')
    test_eq('Test 1.1', part1, 4140, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 3993, test_input_1)
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
