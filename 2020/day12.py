
import math

def manhattan_p1(instructions):
    x, y = 0, 0
    direction = 0 # degress
    for inst in instructions:
        op, arg = inst[0], int(inst[1:])
        if op == "E":
            x += arg
        elif op == "N":
            y += arg
        elif op == "W":
            x -= arg
        elif op == "S":
            y -= arg
        elif op == "F":
            x += arg * math.floor(math.cos(math.radians(direction)) + 0.5)
            y += arg * math.floor(math.sin(math.radians(direction)) + 0.5)
        elif op == "R":
            direction -= arg
            direction = direction % 360
        elif op == "L":
            direction += arg
    return abs(x) + abs(y)


def manhattan_p2(instructions):
    x, y = 0, 0
    wx, wy = 10, 1
    for inst in instructions:
        op, arg = inst[0], int(inst[1:])
        if op == "E":
            wx += arg
        elif op == "N":
            wy += arg
        elif op == "W":
            wx -= arg
        elif op == "S":
            wy -= arg
        elif op == "F":
            x += arg * wx
            y += arg * wy
        elif op == "R":
            arg = -arg
            post_x = wx
            post_y = wy
            wx = post_x * math.cos(math.radians(arg)) - post_y * math.sin(math.radians(arg))
            wy = post_x * math.sin(math.radians(arg)) + post_y * math.cos(math.radians(arg))
        elif op == "L":
            post_x = wx
            post_y = wy
            wx = post_x * math.cos(math.radians(arg)) - post_y * math.sin(math.radians(arg))
            wy = post_x * math.sin(math.radians(arg)) + post_y * math.cos(math.radians(arg))

    return math.floor(abs(x) + abs(y) + 0.5)


if __name__ == "__main__":
    instructions = []
    with open("input", "r") as file:
        instructions = [line.rstrip() for line in file]

    # part 1
    print(manhattan_p1(instructions))

    # part 2
    print(manhattan_p2(instructions))
