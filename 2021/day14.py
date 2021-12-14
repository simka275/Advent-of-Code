
import math

def expand_polymer(polymer, rules, steps):
    count = {}
    for i in range(len(polymer)-1):
        pair = polymer[i:i+2]
        if pair in count:
            count[pair] += 1
        else:
            count[pair] = 1

    for _ in range(steps):
        new_count = {}
        for pair, occurences in count.items():
            new_pair_1 = pair[0] + rules[pair]
            new_pair_2 = rules[pair] + pair[1]
            if new_pair_1 in new_count:
                new_count[new_pair_1] += occurences
            else:
                new_count[new_pair_1] = occurences
            if new_pair_2 in new_count:
                new_count[new_pair_2] += occurences
            else:
                new_count[new_pair_2] = occurences
        count = new_count

    char_count = {}
    for k,v in count.items():
        c1 = k[0]
        c2 = k[1]
        if c1 in char_count:
            char_count[c1] += v
        else:
            char_count[c1] = v
        if c2 in char_count:
            char_count[c2] += v
        else:
            char_count[c2] = v

    # All char (expect 1st and last) part of two pairs so occurs twice
    # Compensate first and last char prior to divide away duplicates
    char_count[polymer[0]] += 1
    char_count[polymer[-1]] += 1
    for k,v in char_count.items():
        char_count[k] = v/2

    most_common_count = 0
    least_common_count = math.inf
    for _,v in char_count.items():
        most_common_count = max(most_common_count,v)
        least_common_count = min(least_common_count,v)

    return most_common_count-least_common_count


if __name__ == "__main__":
    polymer = None
    rules = {}
    with open("input", "r") as file:
        reading_rules = False
        for line in file:
            if line == "\n":
                reading_rules = True
                continue
            if reading_rules:
                k,v = line.strip().split(" -> ")
                rules[k] = v
            else:
                polymer = line.strip()

    # p1
    print(expand_polymer(polymer, rules, 10))

    # p2
    print(expand_polymer(polymer, rules, 40))
