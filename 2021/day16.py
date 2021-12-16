
import math


def sum_packet(packet):
    if isinstance(packet[2], list):
        res = 0
        for p in packet[2]:
            res += sum_packet(p)
        return res
    else:
        return packet[2]


def product_packet(packet):
    if isinstance(packet[2], list):
        res = 1
        for p in packet[2]:
            res *= product_packet(p)
        return res
    else:
        return packet[2]


def minimum_packet(packet):
    if isinstance(packet[2], list):
        res = math.inf
        for p in packet[2]:
            res = min(res,minimum_packet(p))
        return res
    else:
        return packet[2]


def maximum_packet(packet):
    if isinstance(packet[2], list):
        res = -math.inf
        for p in packet[2]:
            res = max(res,maximum_packet(p))
        return res
    else:
        return packet[2]


def greater_than_packet(packet):
    v1, v2 = packet[2][0][2], packet[2][1][2]
    return 1 if v1 > v2 else 0


def less_than_packet(packet):
    v1, v2 = packet[2][0][2], packet[2][1][2]
    return 1 if v1 < v2 else 0


def equal_to_packet(packet):
    v1, v2 = packet[2][0][2], packet[2][1][2]
    return 1 if v1 == v2 else 0


def parse_packet(packet, index):
    version = int(packet[index:index+3],2)
    index += 3
    type_id = int(packet[index:index+3],2)
    index += 3
    if type_id == 4: # Literal valu
        payload = ""
        while True:
            value = packet[index:index+5]
            payload += value[1:]
            index += 5
            if value[0] == "0":
                break
        payload = int(payload,2)
        return version, type_id, payload, index
    else:
        version_sum = version
        length_type = packet[index]
        index += 1
        if length_type == "0":
            length = int(packet[index:index+15],2)
            index += 15
            start_index = index
            payload = []
            while index < (start_index + length):
                subversion, subtype_id, subpayload, index = parse_packet(packet, index)
                payload.append([subversion, subtype_id, subpayload, index])
                version_sum += subversion
        elif length_type == "1":
            subpacket_count = int(packet[index:index+11],2)
            index += 11
            payload = []
            for _ in range(subpacket_count):
                subversion, subtype_id, subpayload, index = parse_packet(packet, index)
                payload.append([subversion, subtype_id, subpayload, index])
                version_sum += subversion
        if type_id == 0:
            payload = sum_packet([version_sum, type_id, payload, index])
        elif type_id == 1:
            payload = product_packet([version_sum, type_id, payload, index])
        elif type_id == 2:
            payload = minimum_packet([version_sum, type_id, payload, index])
        elif type_id == 3:
            payload = maximum_packet([version_sum, type_id, payload, index])
        elif type_id == 5:
            payload = greater_than_packet([version_sum, type_id, payload, index])
        elif type_id == 6:
            payload = less_than_packet([version_sum, type_id, payload, index])
        elif type_id == 7:
            payload = equal_to_packet([version_sum, type_id, payload, index])
        return version_sum, type_id, payload, index


def sum_version_nrs(packet):
    res = packet[0]
    if isinstance(packet[2], list):
        for p in packet[2]:
            res += sum_version_nrs(p)
    return res


def add_version_nrs(packet):
    parsed_packets = parse_packet(packet, 0)
    return parsed_packets[0]


assert(add_version_nrs("".join(["{:04b}".format(int(x,16)) for x in "8A004A801A8002F478"])) == 16)
assert(add_version_nrs("".join(["{:04b}".format(int(x,16)) for x in "620080001611562C8802118E34"])) == 12)
assert(add_version_nrs("".join(["{:04b}".format(int(x,16)) for x in "C0015000016115A2E0802F182340"])) == 23)
assert(add_version_nrs("".join(["{:04b}".format(int(x,16)) for x in "A0016C880162017C3686B18A3D4780"])) == 31)


assert(parse_packet("".join(["{:04b}".format(int(x,16)) for x in "C200B40A82"]),0)[2] == 3)
assert(parse_packet("".join(["{:04b}".format(int(x,16)) for x in "04005AC33890"]),0)[2] == 54)
assert(parse_packet("".join(["{:04b}".format(int(x,16)) for x in "880086C3E88112"]),0)[2] == 7)
assert(parse_packet("".join(["{:04b}".format(int(x,16)) for x in "CE00C43D881120"]),0)[2] == 9)
assert(parse_packet("".join(["{:04b}".format(int(x,16)) for x in "D8005AC2A8F0"]),0)[2] == 1)
assert(parse_packet("".join(["{:04b}".format(int(x,16)) for x in "F600BC2D8F"]),0)[2] == 0)
assert(parse_packet("".join(["{:04b}".format(int(x,16)) for x in "9C005AC2F8F0"]),0)[2] == 0)
assert(parse_packet("".join(["{:04b}".format(int(x,16)) for x in "9C0141080250320F1802104A08"]),0)[2] == 1)


if __name__ == "__main__":
    packet = ""
    with open("input", "r") as file:
        for line in file:
            packet = "".join(["{:04b}".format(int(x,16)) for x in line.strip()])

    # p1
    print(add_version_nrs(packet))

    # p2
    print(parse_packet(packet,0)[2])