
def check_passwords_p1():
    res = 0
    with open("input", "r") as file:
        for line in file:
            line = line.split(" ")
            minc, maxc = [ int(x) for x in line[0].split("-") ]
            char = line[1][0]
            string = line[2].rstrip()
            if minc <= string.count(char) <= maxc:
                res = res +1
    return res


def check_passwords_p2():
    res = 0
    with open("input", "r") as file:
        for line in file:
            line = line.split(" ")
            pos1, pos2 = [ int(x)-1 for x in line[0].split("-") ]
            char = line[1][0]
            string = line[2].rstrip()
            if (char == string[pos1]) ^ (char == string[pos2]):
                res = res +1
    return res


if __name__ == "__main__":
    # Part 1
    print(check_passwords_p1())
    # Part 2
    print(check_passwords_p2())