

def part_one(moves):
    visited = set()
    head = (0,0)
    tail = (0,0)
    visited.add(tail)
    for direction, steps in moves:
        for step in range(int(steps)):
            if direction == "R":
                head = (head[0]+1, head[1])
                if abs(head[0] - tail[0]) > 1:
                    tail = (head[0]-1, head[1])
            if direction == "D":
                head = (head[0], head[1]-1)
                if abs(head[1] - tail[1]) > 1:
                    tail = (head[0], head[1]+1)
            if direction == "L":
                head = (head[0]-1, head[1])
                if abs(head[0] - tail[0]) > 1:
                    tail = (head[0]+1, head[1])
            if direction == "U":
                head = (head[0], head[1]+1)
                if abs(head[1] - tail[1]) > 1:
                    tail = (head[0], head[1]-1)
            visited.add(tail)
    return len(visited)


def part_two(moves):
    visited = set()
    visited.add((0,0))
    knots = [(0,0)] * 10
    for direction, steps in moves:
        for step in range(int(steps)):
            head = knots[0]
            if direction == "R":
                knots[0] = (head[0]+1, head[1])
            elif direction == "D":
                knots[0] = (head[0], head[1]-1)
            elif direction == "L":
                knots[0] = (head[0]-1, head[1])
            elif direction == "U":
                knots[0] = (head[0], head[1]+1)

            for i in range(1, len(knots)):
                x, y = knots[i]
                dx, dy = (knots[i-1][0] - x, knots[i-1][1] - y)
                if (abs(dx), abs(dy)) == (2,2):
                    knots[i] = (x + dx//2, y + dy//2)
                elif abs(dx) == 2:
                    knots[i] = (x + dx//2, y + dy)
                elif abs(dy) == 2:
                    knots[i] = (x + dx, y + dy//2)

            visited.add(knots[-1])
    return len(visited)


if __name__ == "__main__":
    moves = []
    with open("input", "r") as fd:
        moves = [x.strip().split() for x in fd]

    print(part_one(moves))

    print(part_two(moves))