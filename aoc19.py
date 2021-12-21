#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 19

ROTATIONS = [
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
    [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
    [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],

    [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
    [[0, -1, 0], [0, 0, -1], [1, 0, 0]],
    [[0, 1, 0], [0, 0, -1], [-1, 0, 0]],
    [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],

    [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
    [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],
    [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
    [[0, 0, -1], [1, 0, 0], [0, -1, 0]],

    [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
    [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
    [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
    [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],

    [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
    [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
    [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
    [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],

    [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
    [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
    [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
    [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
    ]


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def read_scanners(lines):
    scanners = []
    scanner = None
    for line in lines:
        if line.startswith('---'):
            scanner = int(line.split()[2])
            scanners.append([])
            continue
        if len(line) == 0:
            scanner = None
            continue
        coords = tuple(int(num) for num in line.split(','))
        scanners[scanner].append(coords)
    return scanners


def rotate(beacons, rotation):
    rot_beacons = []
    for beacon in beacons:
        rot_beacon = [0, 0, 0]
        for y in range(3):
            for x in range(3):
                rot_beacon[y] += rotation[y][x] * beacon[x]
        rot_beacons.append(rot_beacon)
    return rot_beacons


def translate(beacons, delta):
    trans_beacons = []
    for beacon in beacons:
        trans_beacon = (
            beacon[0] + delta[0],
            beacon[1] + delta[1],
            beacon[2] + delta[2],
            )
        trans_beacons.append(trans_beacon)
    return trans_beacons


def overlapping_beacons(beacons1, beacons2):
    for beacon1 in beacons1:
        for beacon2 in beacons2:
            delta = (
                beacon1[0] - beacon2[0],
                beacon1[1] - beacon2[1],
                beacon1[2] - beacon2[2],
                )
            matchings = []
            for i, beacon in enumerate(beacons1):
                for j, other_beacon in enumerate(translate(beacons2, delta)):
                    if beacon == other_beacon:
                        matchings.append((i, j))
            if len(matchings) >= 12:
                return delta, matchings
    return None


def find_overlapping(beacons1, beacons2):
    for r in ROTATIONS:
        rot_beacons = rotate(beacons2, r)
        overlap = overlapping_beacons(beacons1, rot_beacons)
        if overlap is not None:
            return r, overlap[0]
    return None, None


def test_rotations():
    beacons = [(-1, -1, 1), (-2, -2, 2), (-3, -3, 3),
               (-2, -3, 1), (5, 6, -4), (8, 0, 7)]
    for r in ROTATIONS:
        print(rotate(beacons, r))


def part1(data):
    return None
    scanners = read_scanners(data)
    beacons = scanners[0][:]
    print(scanners)
    overlappings = []
    done = [0]
    completed = []
    while len(done) < len(scanners):
        for i in range(len(scanners)):
            if len(done) == len(scanners):
                break
            if i in completed or i not in done:
                continue
            for j in range(len(scanners)):
                if len(done) == len(scanners):
                    break
                if j in completed or j in done:
                    continue
                print(i, j, completed, done)
                rotation, delta = find_overlapping(scanners[i], scanners[j])
                if rotation is not None:
                    overlappings.append((i, j, rotation, delta))
                    scanners[j] = translate(rotate(scanners[j], rotation), delta)
                    done.append(j)
                    print('Overlap')
                else:
                    print('No')
            print(i, "complete")
            completed.append(i)
    print("\n".join([str(overlap) for overlap in overlappings]))

    all_beacons = set()
    for beacons in scanners:
        for beacon in beacons:
            all_beacons.add(beacon)
    print(len(all_beacons))
    return len(all_beacons)


def manhattan_distance(scanner1, scanner2):
    return sum([abs(scanner1[i] - scanner2[i]) for i in range(3)])

def part2(data):
    scanners_str = get_input('output19')
    scanners = [tuple([int(n) for n in line.split(', ')]) for line in scanners_str]
    print(scanners)
    max_md = 0
    for i in range(len(scanners) - 1):
        for j in range(i + 1, len(scanners)):
            md = manhattan_distance(scanners[i], scanners[j])
            max_md = max(md, max_md)
    return max_md


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 79, test_input_1)
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
