
def part_one(sections):
    res = 0
    for assignments in sections:
        first, second = assignments
        if second[0] <= first[0] and first[1] <= second[1]: # first in second
            res += 1
        elif first[0] <= second[0] and second[1] <= first[1]: # second in first
            res += 1
    return res

def part_two(sections):
    res = 0
    for assignments in sections:
        first, second = assignments
        if first[0] <= second[0] <= first[1]: # second starts inside first
            res += 1
        elif second[0] <= first[0] <= second[1]: # first starts inside second
            res += 1
    return res

if __name__ == "__main__":
    sections = []
    with open("input", "r") as fd:
        for line in fd:
            first, second = line.strip().split(",")
            sections.append([[int(x) for x in first.split("-")], [int(x) for x in second.split("-")]])

    print(part_one(sections))

    print(part_two(sections))