#!/usr/bin/env python3


def get_input(filename):
    with open(filename, 'r') as in_file:
        depths = [int(depth) for depth in in_file.readlines()]
    return depths


def part1(depths):
    incr = 0
    prev_depth = depths[0]
    for depth in depths:
        if depth > prev_depth:
            incr += 1
        prev_depth = depth
    print(incr)


def part2(depths):
    incr = 0
    prev_depth_sum = depths[0] + depths[1] + depths[2]
    for i in range(len(depths)):
        if i < 3:
            continue
        depth_sum = prev_depth_sum - depths[i - 3] + depths[i]
        if depth_sum > prev_depth_sum:
            incr += 1
        prev_depth_sum = depth_sum
    print(incr)

if __name__ == '__main__':
    i = get_input('input1')
    # i = get_input('ex1')
    part1(i)
    part2(i)
