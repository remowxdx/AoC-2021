#!/usr/bin/env python3

import cairo
import math
from aoc import check_solution, save_solution, test_eq

DAY = 16


def get_input(filename):
    with open(filename, 'r') as input_file:
        lines = input_file.read()
    return lines.splitlines()


HEX_TO_BIN = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def to_binary(packet):
    binary = []
    print(packet)
    for char in packet:
        binary.append(HEX_TO_BIN[char])
    return "".join(binary)


def to_num(binary):
    num = 0
    for bit in binary:
        num *= 2
        if bit == '1':
            num += 1
    return num


def parse_literal(bmsg, pos):
    last = False
    literal_value = []
    while not last:
        if bmsg[pos] == '0':
            last = True
        literal_value.append(bmsg[pos+1:pos+5])
        pos += 5
    return to_num("".join(literal_value)), pos


def parse_operator(bmsg, pos, packet):
    packet['lenght_type_id'] = to_num(bmsg[pos])
    if packet['lenght_type_id'] == 0:
        packet['subpackets_bit_length'] = to_num(bmsg[pos + 1:pos + 16])
        pos += 16
        parse_to = pos + packet['subpackets_bit_length']
        # print(pos, parse_to)
        while pos < parse_to:
            subpacket, pos = parse_packet(bmsg, pos)
            packet['subpackets'].append(subpacket)
            # print(pos, parse_to)
    else:
        packet['subpackets_num'] = to_num(bmsg[pos + 1:pos + 12])
        # print(bmsg[pos + 1:pos + 12])
        pos += 12
        for _ in range(packet['subpackets_num']):
            subpacket, pos = parse_packet(bmsg, pos)
            packet['subpackets'].append(subpacket)
            # print(pos, num_packet)

    calc_value(packet)
    return packet['value'], pos


def multiply_packet_values(packets):
    prod = 1
    for packet in packets:
        prod *= packet['value']
    return prod


def packet_greater(packets):
    if packets[0]['value'] > packets[1]['value']:
        return 1
    return 0


def packet_less(packets):
    if packets[0]['value'] < packets[1]['value']:
        return 1
    return 0


def packet_equal(packets):
    if packets[0]['value'] == packets[1]['value']:
        return 1
    return 0


def calc_value(packet):
    packet_type_operation = {
        0: lambda packets: sum([packet['value'] for packet in packets]),
        1: multiply_packet_values,
        2: lambda packets: min([packet['value'] for packet in packets]),
        3: lambda packets: max([packet['value'] for packet in packets]),
        5: packet_greater,
        6: packet_less,
        7: packet_equal,
    }
    subpackets = packet['subpackets']
    packet['value'] = packet_type_operation[packet['type_id']](subpackets)
    return packet['value']


def parse_packet(bmsg, pos):
    packet = {'subpackets': []}
    packet['version'] = to_num(bmsg[pos:pos + 3])
    packet['type_id'] = to_num(bmsg[pos + 3:pos + 6])
    pos += 6
    if packet['type_id'] == 4:
        packet['value'], pos = parse_literal(bmsg, pos)
    else:
        _value, pos = parse_operator(bmsg, pos, packet)
    return packet, pos


def sum_versions(packet):
    versions = packet['version']
    for subpacket in packet['subpackets']:
        versions += sum_versions(subpacket)
    return versions


def draw_packets(packet):
    surface = cairo.SVGSurface('images/day16.svg', 1900, 1800)
    ctx = cairo.Context(surface)
    ctx.select_font_face('Sans Serif')
    ctx.set_font_size(12)

    ctx.set_source_rgb(0.9, 0.9, 0.8)
    ctx.rectangle(1, 1, 1899, 1299)
    ctx.fill()
    draw_packet(ctx, packet, 950, 30, 1800)

    surface.flush()
    surface.finish()


def draw_packet(ctx, packet, x, y, width):
    num_sp = len(packet['subpackets'])
    if num_sp != 0:
        ctx.set_source_rgb(0.0, 0.0, 0.0)
        ctx.set_line_width(1)
        step_len = width / (num_sp + 1)
        for i, subpacket in enumerate(packet['subpackets']):
            ctx.move_to(x, y)
            next_x = x - (num_sp / 2 - i) * step_len
            next_y = y + math.pow(width, 0.3) * 50
            ctx.line_to(next_x, next_y)
            ctx.stroke()
            draw_packet(ctx, subpacket, next_x, next_y, step_len)
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.arc(x, y, 20, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(0.0, 0.0, 0.0)
    ctx.arc(x, y, 20, 0, 2 * math.pi)
    ctx.stroke()
    ctx.move_to(x - 10, y - 2)
    type_sym = ['+', '*', 'mn', 'mx', 'v', '>', '<', '=']
    ctx.show_text(f"{type_sym[packet['type_id']]}")
    ctx.move_to(x - 17, y + 10)
    ctx.show_text(f"{packet['value']}")


def part1(data):
    binary = to_binary(data[0])
    packet, _pos = parse_packet(binary, 0)
    # print(packet, pos, binary[pos:])
    return sum_versions(packet)


def part2(data):
    binary = to_binary(data[0])
    packet, _pos = parse_packet(binary, 0)
    draw_packets(packet)
    return packet['value']


def run_tests():
    test_input_1 = get_input(f'ex{DAY}')
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 6, test_input_1)
    test_eq('Test 1.2', part1, 9, get_input('ex16_2'))
    test_eq('Test 1.3', part1, 14, get_input('ex16_22'))
    test_eq('Test 1.4', part1, 16, get_input('ex16_3'))
    test_eq('Test 1.5', part1, 12, get_input('ex16_4'))
    test_eq('Test 1.6', part1, 23, get_input('ex16_5'))
    test_eq('Test 1.7', part1, 31, get_input('ex16_6'))
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', part2, 3, ['C200B40A82'])
    test_eq('Test 2.2', part2, 54, ['04005AC33890'])
    test_eq('Test 2.3', part2, 7, ['880086C3E88112'])
    test_eq('Test 2.4', part2, 9, ['CE00C43D881120'])
    test_eq('Test 2.5', part2, 1, ['D8005AC2A8F0'])
    test_eq('Test 2.6', part2, 0, ['F600BC2D8F'])
    test_eq('Test 2.7', part2, 0, ['9C005AC2F8F0'])
    test_eq('Test 2.8', part2, 1, ['9C0141080250320F1802104A08'])
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
