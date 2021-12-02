
def move(movements):
    horizontal, depth = 0,0
    for movement in movements:
        direction, steps = movement.split(" ")
        if direction == "up":
            depth -= int(steps)
        elif direction == "forward":
            horizontal += int(steps)
        elif direction == "down":
            depth += int(steps)
    return horizontal*depth

def move_w_aim(movements):
    horizontal, depth, aim = 0,0,0
    for movement in movements:
        direction, steps = movement.split(" ")
        if direction == "up":
            aim -= int(steps)
        elif direction == "forward":
            horizontal += int(steps)
            depth += aim*int(steps)
        elif direction == "down":
            aim += int(steps)
    return horizontal*depth


if __name__ == "__main__":
    movements = []
    with open("input", "r") as file:
        for line in file:
            movements.append(line.strip())

    # part 1
    print(move(movements))

    # part 2
    print(move_w_aim(movements))