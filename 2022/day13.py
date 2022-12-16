
import functools

LT = -1
EQ = 0
GT = 1

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return LT
        elif left == right:
            return 0
        elif left > right:
            return 1
    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    elif isinstance(left, list) and isinstance(right, list):
        for i in range(len(left)):
            if i >= len(right):
                return 1
            res = compare(left[i], right[i])
            if res == LT:
                return LT
            elif res == 1:
                return 1
        if len(left) == len(right):
            return 0
        return LT

def part_one(packet_pairs):
    res = 0
    for i in range(0, len(packet_pairs), 2):
        if compare(packet_pairs[i], packet_pairs[i+1]) == LT:
            res += (i//2)+1
    return res

def part_two(packet_pairs):
    packet_pairs.append([[2]])
    packet_pairs.append([[6]])
    packet_pairs.sort(key=functools.cmp_to_key(compare))
    first_divider = None
    second_divider = None
    for i in range(len(packet_pairs)):
        if not first_divider and compare([[2]], packet_pairs[i]) == EQ:
            first_divider = i+1
        if not second_divider and compare([[6]], packet_pairs[i]) == EQ:
            second_divider = i+1
            break
    return first_divider*second_divider

if __name__ == "__main__":
    packet_pairs = []
    with open("input", "r") as fd:
        packet_pairs = [ eval(x) for x in fd.read().splitlines() if x ]

    print(part_one(packet_pairs))

    print(part_two(packet_pairs))