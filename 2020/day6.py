
def unique_answers(group):
    answers = set()
    for person in group:
        for a in person:
            answers.add(a)
    return len(answers)


def answer_count_p1(answers):
    res = 0
    for group in answers:
        res += unique_answers(group)
    return res


def common_answers(group):
    answers = {}
    for person in group:
        for a in person:
            if a in answers:
                answers[a] += 1
            else:
                answers[a] = 1
    res = 0
    for _, c in answers.items():
        if c == len(group):
            res += 1
    return res


def answer_count_p2(answers):
    res = 0
    for group in answers:
        res += common_answers(group)
    return res


if __name__ == "__main__":
    answers = []
    with open("input", "r") as file:
        group = []
        for line in file:
            if line.rstrip():
                group.append(line.rstrip())
            else:
                answers.append(group)
                group = []
        if len(group) != 0:
            answers.append(group)

    # part 1
    print(answer_count_p1(answers))
    # part 2
    print(answer_count_p2(answers))

