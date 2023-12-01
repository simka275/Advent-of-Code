

def part_one(lines):
    res = 0
    for line in lines:
        nums = [int(x) for x in line if x.isdigit()]
        res += 10*nums[0] + nums[-1]
    return res


def part_two(lines):
    res = 0
    num_map = {
                'one': 1,
               'two': 2,
               'three': 3,
               'four': 4,
               'five': 5,
               'six': 6,
               'seven': 7,
               'eight': 8,
               'nine': 9,
               '1': 1,
               '2': 2,
               '3': 3,
               '4': 4,
               '5': 5,
               '6': 6,
               '7': 7,
               '8': 8,
               '9': 9,
               }

    for line in lines:
        first, last = (len(line), None), (-1, None)
        for k,v in num_map.items():
            first_pos = line.find(k)
            if first_pos == -1:
                continue
            if first_pos < first[0]:
                first = (first_pos, v)

            last_pos = line.rfind(k)
            if last_pos > last[0]:
                last = (last_pos, v)
        res += 10*first[1] + last[1]
    return res


if __name__ == "__main__":
    lines = []
    with open("input", "r") as fd:
        lines = [x.strip() for x in fd]

    print(part_one(lines))

    print(part_two(lines))
