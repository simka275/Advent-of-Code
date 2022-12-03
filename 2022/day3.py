

def part_one(rucksacks):
    res = 0
    for sack in rucksacks:
        left = sack[:len(sack)//2]
        right = sack[len(sack)//2:]
        for char in left:
            if char in right:
                res += ord(char)-96 if char.islower() else ord(char)-38
                break
    return res


def part_two(rucksacks):
    res = 0
    for i in range(0, len(rucksacks), 3):
        first = rucksacks[i]
        second = rucksacks[i+1]
        third = rucksacks[i+2]

        potential_badges = set(first)

        potential_badges = [badge for badge in potential_badges if second.count(badge) > 0]
        potential_badges = [badge for badge in potential_badges if third.count(badge) > 0]

        assert len(potential_badges) == 1
        badge = potential_badges[0]
        res += ord(badge)-96 if badge.islower() else ord(badge)-38
    return res


if __name__ == "__main__":
    rucksacks = []
    with open("input", "r") as fd:
        rucksacks = [x.strip() for x in fd]

    print(part_one(rucksacks))

    print(part_two(rucksacks))