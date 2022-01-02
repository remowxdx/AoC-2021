#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 23


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def read_positions(lines):
    pos = [(a, b) for b in range(2) for a in range(4)]
    pos_index = 0
    positions = {}
    to_map = {(1, i + 1): (4, i) for i in range(11)}
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell in ['A', 'B', 'C', 'D']:
                positions[pos[pos_index]] = cell
                to_map[(y, x)] = pos[pos_index]
                pos_index += 1
    print('To map:', to_map)
    return positions, to_map


def make_map():
    hallway = {
        (4, 0): [
            (0, 0, 3), (0, 1, 4), (1, 0, 5), (1, 1, 6),
            (2, 0, 7), (2, 1, 8), (3, 0, 9), (3, 1, 10)],
        (4, 1): [
            (0, 0, 2), (0, 1, 3), (1, 0, 4), (1, 1, 5),
            (2, 0, 6), (2, 1, 7), (3, 0, 8), (3, 1, 9)],
        (4, 2): [],
        (4, 3): [
            (0, 0, 2), (1, 0, 2), (0, 1, 3), (1, 1, 3),
            (2, 0, 4), (2, 1, 5), (3, 0, 6), (3, 1, 7)],
        (4, 4): [],
        (4, 5): [
            (1, 0, 2), (2, 0, 2), (1, 1, 3), (2, 1, 3),
            (0, 0, 4), (3, 0, 4), (0, 1, 5), (3, 1, 5)],
        (4, 6): [],
        (4, 7): [
            (2, 0, 2), (3, 0, 2), (2, 1, 3), (3, 1, 3),
            (1, 0, 4), (1, 1, 5), (0, 0, 6), (0, 1, 7)],
        (4, 8): [],
        (4, 9): [
            (3, 0, 2), (3, 1, 3), (2, 0, 4), (2, 1, 5),
            (1, 0, 6), (1, 1, 7), (0, 0, 8), (0, 1, 9)],
        (4, 10): [
            (3, 0, 3), (3, 1, 4), (2, 0, 5), (2, 1, 6),
            (1, 0, 7), (1, 1, 8), (0, 0, 9), (0, 1, 10)],
    }
    burrow = hallway.copy()
    for pos, costs in hallway.items():
        # print(pos, costs)
        for y, x, cost in costs:
            if (y, x) not in burrow:
                print('->', y, x)
                burrow[(y, x)] = []
            burrow[(y, x)].append((pos[0], pos[1], cost))
    print('Burrow:', burrow)
    return burrow


def is_reachable(amphipods, start, end):
    if end in amphipods:
        return False
    if start[0] == 4:
        start, end = end, start

    if start[1] == 1:  # inner
        if (start[0], 0) in amphipods:
            return False

    burrow_to_hallway = [2, 4, 6, 8, ]
    for i in range(
            min(burrow_to_hallway[start[0]], end[1]),
            max(burrow_to_hallway[start[0]], end[1]) + 1):
        if (4, i) == end:
            continue
        if (4, i) in amphipods:
            return False
    return True


def print_map(_burrow, amphipods, to_map):
    for y in range(5):
        for x in range(13):
            if (y, x) in to_map:
                pos = to_map[(y, x)]
                if pos in amphipods:
                    print(amphipods[pos], end='')
                else:
                    print('.', end='')
            else:
                neighbors = [
                    (y + 1, x + 1),
                    (y - 1, x - 1),
                    (y + 1, x - 1),
                    (y - 1, x + 1),
                    (y, x + 1),
                    (y, x - 1),
                    (y + 1, x),
                    (y - 1, x),
                    ]
                for pos in neighbors:
                    if pos in to_map:
                        print('#', end='')
                        break
                else:
                    print(' ', end='')
        print()


def map_printer(burrow, to_map):
    def partial_map_printer(amphipods):
        print_map(burrow, amphipods, to_map)
    return partial_map_printer


def is_at_home(amphipod, pos):
    if pos[0] == 4:
        return False
    if pos[0] == ord(amphipod) - ord('A'):
        return True
    return False


def move_out(burrow, amphipods, start, end, prev_energy):
    # print('Move out', start)
    if not is_reachable(amphipods, start, end):
        return None, amphipods
    return move_amphipod(burrow, amphipods, start, end, prev_energy)


def moves_out(burrow, amphipods, start, prev_energy):
    moves = []
    for i in range(11):
        end = (4, i)
        energy, new_amphipods = move_out(
            burrow, amphipods, start, end, prev_energy)
        if energy is None:
            continue
        moves.append((energy, new_amphipods))
    return moves


def move_amphipod(burrow, amphipods, start, end, prev_energy):
    amphipod = amphipods[start]
    for candidate in burrow[start]:
        if (candidate[0], candidate[1]) == end:
            new_amphipods = amphipods.copy()
            del new_amphipods[start]
            new_amphipods[end] = amphipod
            energy = candidate[2] * 10 ** (ord(amphipod) - ord('A'))
            return prev_energy + energy, new_amphipods
    return None, None


def move_home(burrow, amphipods, start, prev_energy):
    # print('Move home', start)
    amphipod = amphipods[start]
    home = ord(amphipod) - ord('A')
    inner_pos = (home, 1)
    if inner_pos not in amphipods:
        if is_reachable(amphipods, start, inner_pos):
            return move_amphipod(
                burrow, amphipods, start, inner_pos, prev_energy)
        return None, amphipods
    outer_pos = (home, 0)
    if is_at_home(amphipods[inner_pos], inner_pos):
        if is_reachable(amphipods, start, outer_pos):
            return move_amphipod(
                burrow, amphipods, start, outer_pos, prev_energy)
    return None, amphipods


def amphipods_at_home(amphipods):
    for pos, amphipod in amphipods.items():
        if not is_at_home(amphipod, pos):
            return False
    return True


def all_amphipod_moves(burrow, amphipods, amphipod, start, prev_energy):
    if is_at_home(amphipod, start):
        if start[1] == 1:
            return []
        inner_pos = (start[0], 1)
        if inner_pos in amphipods:
            inner_amphi = amphipods[inner_pos]
            if is_at_home(inner_amphi, inner_pos):
                return []
            return moves_out(burrow, amphipods, start, prev_energy)
        raise ValueError('Hole.')

    if start[0] < 4:
        return moves_out(burrow, amphipods, start, prev_energy)

    energy, new_amphipods = move_home(
        burrow, amphipods, start, prev_energy)

    if energy is None or new_amphipods is None:
        return []

    return [(energy, new_amphipods)]


def all_amphipods_moves(burrow, amphipods, prev_energy):
    moves = []
    for start, amphipod in amphipods.items():
        if is_at_home(amphipod, start):
            if start[1] == 1:
                continue
            inner_pos = (start[0], 1)
            if inner_pos in amphipods:
                inner_amphi = amphipods[inner_pos]
                if is_at_home(inner_amphi, inner_pos):
                    continue
                moves.extend(moves_out(burrow, amphipods, start, prev_energy))
            else:
                raise ValueError('Hole.')
        else:
            if start[0] < 4:
                moves.extend(moves_out(burrow, amphipods, start, prev_energy))
            else:
                energy, new_amphipods = move_home(
                    burrow, amphipods, start, prev_energy)
                if energy is None or new_amphipods is None:
                    continue
                moves.append((energy, new_amphipods))
    return moves


def find_min_energy(burrow, initial_amphipods, printer):
    print(initial_amphipods)

    moves = []
    moves.append((0, initial_amphipods))
    ends = []

    count = 0

    # while count < 4:
    while True:
        count += 1
        if len(moves) == 0:
            break

        if count % 100_000 == 0:
            for cost, status in moves[-1:]:
                printer(status)
                print(cost)
            print(count, len(moves), len(ends), ends[-1][0])

        energy, amphipods = moves.pop()
        if len(ends) > 0 and energy > ends[-1][0]:
            continue

        if energy is None:
            raise ValueError('Energy is None.')
        if len(amphipods) != 8:
            raise ValueError('Lost amphipod!')

        if amphipods_at_home(amphipods):
            if len(ends) == 0:
                ends.append((energy, amphipods))
            min_energy = min(ends, key=lambda el: el[0])
            if energy < min_energy[0]:
                ends.append((energy, amphipods))
                print(energy, amphipods)
            continue

        moves.extend(all_amphipods_moves(burrow, amphipods, energy))

    # print(moves)

    if len(ends) == 0:
        return 0

    min_energy = min(ends, key=lambda el: el[0])
    printer(min_energy[1])

    return min_energy[0]


def part1(data):
    print()
    print('Input:')
    print("\n".join(data))
    burrow = make_map()
    amphipods, to_map = read_positions(data)
    print('Parsed:')
    printer = map_printer(burrow, to_map)
    printer(amphipods)
    result = find_min_energy(burrow, amphipods, printer)
    return result


def part2(data):
    return data


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    test_input_2 = get_input(f'ex{DAY}_2')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 12521, test_input_1)
    test_eq('Test 1.2', part1, 46, test_input_2)
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
    # run_part1(True)
    # run_part2(False)


if __name__ == '__main__':
    main()
