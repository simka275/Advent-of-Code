
import re
import copy

def part_one(stacks, operations):
    res = ""
    stacks = copy.deepcopy(stacks)
    for move_count, src, dst in operations:
        for _ in range(move_count):
            stacks[dst-1].append(stacks[src-1].pop())

    for stack in stacks:
        if stack:
            res += stack[-1]

    return res


def part_two(stacks, operations):
    res = ""
    stacks = copy.deepcopy(stacks)
    for move_count, src, dst in operations:
        stacks[dst-1] = stacks[dst-1] + stacks[src-1][-move_count:]
        stacks[src-1] = stacks[src-1][:-move_count]

    for stack in stacks:
        if stack:
            res += stack[-1]

    return res


if __name__ == "__main__":
    stacks = [[] for i in range(9)]
    operations = []
    with open("input", "r") as fd:
        parsing_stacks = True
        for line in fd:
            line = line.strip("\n")
            if not line:
                parsing_stacks = False
                continue
            if parsing_stacks:
                for i in range(len(line)):
                    if line[i].isalpha():
                        stacks[i//4].insert(0, line[i])
            else:
                match = re.match(r'move (\d+) from (\d+) to (\d+)', line)
                operations.append([int(x) for x in match.groups()])

    print(part_one(stacks, operations))

    print(part_two(stacks, operations))


