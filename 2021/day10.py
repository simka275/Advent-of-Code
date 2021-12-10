

def get_first_error_score(line):
    closers = {")":3, "]":57, "}":1197, ">":25137}
    mappings = {"(":")", "[":"]", "{":"}", "<":">"}
    stack = []
    for char in line:
        if char in closers:
            if not stack or char != mappings[stack[-1]]:
                return closers[char]
            else:
                stack.pop()
        else:
            stack.append(char)
    return 0


def calc_syntax_error_score(lines):
    res = 0
    for line in lines:
        res += get_first_error_score(line)
    return res


def calc_completion_score(line):
    res = 0
    closers = {")":1, "]":2, "}":3, ">":4}
    mappings = {"(":")", "[":"]", "{":"}", "<":">"}
    stack = []
    for char in line:
        if char in closers:
            if not stack or char != mappings[stack[-1]]:
                return closers[char]
            else:
                stack.pop()
        else:
            stack.append(char)
    while stack:
        closer = mappings[stack.pop()]
        res *= 5
        res += closers[closer]
    return res


def calc_middle_completion_score(lines):
    scores = []
    correct_lines = []
    for line in lines:
        if get_first_error_score(line) == 0:
            correct_lines.append(line)
    for line in correct_lines:
        scores.append(calc_completion_score(line))
    scores = sorted(scores)
    return scores[int(len(scores)/2)]


if __name__ == "__main__":
    lines = []
    with open("input", "r") as file:
        for line in file:
            lines.append(line.strip())

    # p1
    print(calc_syntax_error_score(lines))

    # p2
    print(calc_middle_completion_score(lines))