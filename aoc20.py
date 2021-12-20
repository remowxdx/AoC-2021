#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 20


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


def make_image(outside):
    image = {
        'pixels': set(),
        'top': 0,
        'left': 0,
        'right': 0,
        'bottom': 0,
        'outside': outside,
    }
    return image


def read_algorithm_and_image(lines):
    algo = lines[0]

    image = make_image('.')
    for y, line in enumerate(lines[2:]):
        for x, pixel in enumerate(line):
            if pixel == '#':
                image_set_pixel(image, (x, y), pixel)
    return algo, image


def count_light_pixels(image):
    return len(image['pixels'])


def count_light_pixels_2(image):
    count = 0
    for y in range(image['top'], image['bottom']):
        for x in range(image['left'], image['right']):
            if (x, y) in image['pixels']:
                count += 1
    return count


def image_pixel(image, coord):
    x, y = coord
    if image['left'] <= x <= image['right'] and image['top'] <= y <= image['bottom']:
        if coord in image['pixels']:
            return '#'
        return '.'
    return image['outside']


def image_set_pixel(image, coord, pixel):
    x, y = coord
    if image['left'] <= x <= image['right'] and image['top'] <= y <= image['bottom']:
        if pixel == '#':
            image['pixels'].add(coord)
        else:
            if coord in image['pixels']:
                image['pixels'].remove(coord)
    else:
        if pixel == image['outside']:
            pass
        else:
            if x < image['left']:
                e_x = image['left']
                image['left'] = x
                for xx in range(x, e_x):
                    for yy in range(image['top'], image['bottom'] + 1):
                        image_set_pixel(image, (xx, yy), image['outside'])
            elif x > image['right']:
                s_x = image['right']
                image['right'] = x
                for xx in range(s_x + 1, x + 1):
                    for yy in range(image['top'], image['bottom'] + 1):
                        image_set_pixel(image, (xx, yy), image['outside'])
            if y < image['top']:
                e_y = image['top']
                image['top'] = y
                for yy in range(y, e_y):
                    for xx in range(image['left'], image['right'] + 1):
                        image_set_pixel(image, (xx, yy), image['outside'])
            elif y > image['bottom']:
                s_y = image['bottom']
                image['bottom'] = y
                for yy in range(s_y + 1, y + 1):
                    for xx in range(image['left'], image['right'] + 1):
                        image_set_pixel(image, (xx, yy), image['outside'])
            image_set_pixel(image, (x, y), pixel)


def enhanced_pixel(algo, image, coord):
    pos = 0
    for y in range(-1, 2):
        for x in range(-1, 2):
            pixel = image_pixel(image, (coord[0] + x, coord[1] + y))
            pos = pos * 2
            if pixel == '#':
                pos += 1
    return algo[pos]


def image_bounding(image):
    return image['left'], image['top'], image['right'], image['bottom']


def str_image(image):
    min_x, min_y, max_x, max_y = image_bounding(image)

    image_str = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            row.append(image_pixel(image, (x, y)))
        image_str.append("".join(row))
    return "\n".join(image_str)


def enhance_image(image, algo):
    new_outside = '.'
    if algo[0] == '#':
        if image['outside'] == '.':
            new_outside = '#'
    new_image = make_image(new_outside)

    for y in range(image['top'] - 1, image['bottom'] + 2):
        for x in range(image['left'] - 1, image['right'] + 2):
            pixel = enhanced_pixel(algo, image, (x, y))
            image_set_pixel(new_image, (x, y), pixel)
    return new_image


def part1(data):
    algo, image = read_algorithm_and_image(data)
    new_image = image.copy()
    print()
    # print(str_image(new_image))
    # print(new_image)
    for step in range(2):
        new_image = enhance_image(new_image, algo)

    # print(str_image(new_image))
    # print(new_image)

    return count_light_pixels(new_image)


def part2(data):
    algo, new_image = read_algorithm_and_image(data)
    image = new_image.copy()
    for step in range(50):
        print("Step", step)
        new_image = enhance_image(new_image, algo)

    # print(str_image(new_image))
    # print(new_image)
    return count_light_pixels(new_image)


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 35, test_input_1)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 3351, test_input_1)
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
