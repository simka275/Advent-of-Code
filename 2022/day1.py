

def part_one(elves):
    max_calories = 0
    for snacks in elves:
        max_calories = max(max_calories, sum(snacks))
    return max_calories


def part_two(elves):
    sorted_calories = []
    for snacks in elves:
        calories = sum(snacks)
        if not sorted_calories:
            sorted_calories.append(calories)
            continue

        for i in range(len(sorted_calories)):
            if calories >= sorted_calories[i]:
                sorted_calories = sorted_calories[:i] + [calories] + sorted_calories[i:]
                break
            if i == len(sorted_calories)-1:
                sorted_calories.append(calories)

    return sum(sorted_calories[:3])


if __name__ == "__main__":
    elves = []
    with open("input", "r") as fd:
        snacks = []
        for line in fd:
            line = line.strip()
            if not line:
                elves.append(snacks)
                snacks = []
            else:
                snacks.append(int(line))
        if snacks:
            elves.append(snacks)

    # p1
    print(part_one(elves))

    # p2
    print(part_two(elves))




