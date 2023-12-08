

import math


def part_one(lines):
    instructions = lines[0]
    mapping = dict()
    for i in range(2, len(lines)):
        node, neighbors = lines[i].split(" = ")
        left_neighbor, right_neighbor = neighbors.split(", ")
        left_neighbor = left_neighbor[1:]
        right_neighbor = right_neighbor[:-1]
        mapping[node] = {"L": left_neighbor, "R": right_neighbor}

    goal = "ZZZ"
    queue = [("AAA", 0, 0)]
    while queue:
        current_node, instruction_index, steps = queue.pop(0)
        if current_node == goal:
            return steps
        next_node = mapping[current_node][instructions[instruction_index]]
        instruction_index = (instruction_index + 1) % len(instructions)
        steps += 1
        queue.append((next_node, instruction_index, steps))


def lcm(a, b):
    return abs(a*b) // math.gcd(a,b)

def lcm_of_list(numbers):
    result = 1
    for number in numbers:
        result = lcm(result, number)
    return result

def find_cycle_length(start_node, instructions, mapping):
    queue = [(start_node, 0, 0)]
    goal_nodes_reached = []
    while queue:
        current_node, instruction_index, steps = queue.pop(0)
        if current_node[-1] == "Z":
            for goal_node, goal_index, goal_steps, in goal_nodes_reached:
                if current_node == goal_node and instruction_index == goal_index:
                    cycle_length = steps - goal_steps
                    return cycle_length
            goal_nodes_reached.append((current_node, instruction_index, steps))

        next_node = mapping[current_node][instructions[instruction_index]]
        instruction_index = (instruction_index + 1) % len(instructions)
        steps += 1
        queue.append((next_node, instruction_index, steps))

def part_two(lines):
    instructions = lines[0]
    mapping = dict()
    start_nodes = []
    for i in range(2, len(lines)):
        node, neighbors = lines[i].split(" = ")
        left_neighbor, right_neighbor = neighbors.split(", ")
        left_neighbor = left_neighbor[1:]
        right_neighbor = right_neighbor[:-1]
        mapping[node] = {"L": left_neighbor, "R": right_neighbor}
        if node[-1] == "A":
            start_nodes.append(node)

    start_nodes = [x for x in start_nodes]
    cycle_lengths = []
    for start_node in start_nodes:
        cycle_lengths.append(find_cycle_length(start_node, instructions, mapping))

    return lcm_of_list(cycle_lengths)


if __name__ == "__main__":
    lines = []
    with open("input", "r") as fd:
        lines = [x.strip() for x in fd]

    print(part_one(lines))

    print(part_two(lines))
