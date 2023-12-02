

def part_one(lines):
    res = 0
    for line in lines:
        max_values = dict()
        game, rest = line.split(": ")
        game = game.split()[-1]
        sets = rest.split("; ")
        for x in sets:
            balls = x.split(", ")
            for ball in balls:
                number, color = ball.split()
                if color in max_values:
                    max_values[color] = max(max_values[color], int(number))
                else:
                    max_values[color] = int(number)
        if max_values["red"] <= 12 and max_values["green"] <= 13 and max_values["blue"] <= 14:
            res += int(game)
    return res


def part_two(lines):
    res = 0
    for line in lines:
        max_values = dict()
        game, rest = line.split(": ")
        game = game.split()[-1]
        sets = rest.split("; ")
        for x in sets:
            balls = x.split(", ")
            for ball in balls:
                number, color = ball.split()
                if color in max_values:
                    max_values[color] = max(max_values[color], int(number))
                else:
                    max_values[color] = int(number)
        res += max_values["red"] * max_values["green"] * max_values["blue"]
    return res

if __name__ == "__main__":
    lines = []
    with open("input", "r") as fd:
        lines = [x.strip() for x in fd]

    print(part_one(lines))

    print(part_two(lines))
