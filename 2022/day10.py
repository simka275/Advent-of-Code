

def part_one(operations):
    cycle = 0
    register_x = 1
    signal_strength = dict()
    for op in operations:
        cycle += 1
        if cycle in (20, 60, 100, 140, 180, 220):
            signal_strength[cycle] = cycle*register_x
        if op[:4] == "addx":
            cycle += 1
            if cycle in (20, 60, 100, 140, 180, 220):
                signal_strength[cycle] = cycle*register_x
            register_x += int(op[5:])

    return sum(signal_strength.values())


def part_two(operations):
    screen = [[] for x in range(6)]
    cycle = 0
    register_x = 1
    for op in operations:
        if (cycle % 40) in (register_x-1, register_x, register_x+1):
            screen[cycle // 40].append("#")
        else:
            screen[cycle // 40].append(".")
        cycle += 1
        if op[:4] == "addx":
            if (cycle % 40) in (register_x-1, register_x, register_x+1):
                screen[cycle // 40].append("#")
            else:
                screen[cycle // 40].append(".")
            cycle += 1
            register_x += int(op[5:])

    return screen



if __name__ == "__main__":
    operations = []
    with open("input", "r") as fd:
        operations = [x.strip() for x in fd]


    print(part_one(operations))

    for row in part_two(operations):
        print("".join(row))