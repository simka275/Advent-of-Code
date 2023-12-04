

def part_one(lines):
    res = 0
    for line in lines:
        card, numbers = line.split(": ")
        winning_numbers, chosen_numbers = numbers.split(" | ")
        winning_numbers = set([int(x) for x in winning_numbers.split()])
        chosen_numbers = set([int(x) for x in chosen_numbers.split()])
        points = 0
        for chosen_number in chosen_numbers:
            if chosen_number in winning_numbers:
                points = points*2 if points > 0 else 1
        res += points
    return res

def part_two(lines):
    card_count = [1] * len(lines)
    for i in range(len(lines)):
        _, numbers = lines[i].split(": ")
        winning_numbers, chosen_numbers = numbers.split(" | ")
        winning_numbers = set([int(x) for x in winning_numbers.split()])
        chosen_numbers = set([int(x) for x in chosen_numbers.split()])

        add_index = i+1
        for chosen_number in chosen_numbers:
            if chosen_number in winning_numbers:
                card_count[add_index] += card_count[i]
                add_index += 1

    return sum(card_count)


if __name__ == "__main__":
    lines = []
    with open("input", "r") as fd:
        lines = [x.strip() for x in fd]

    print(part_one(lines))

    print(part_two(lines))
