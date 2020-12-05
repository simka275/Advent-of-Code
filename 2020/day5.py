

def get_row(row):
    assert(len(row) == 7)
    res = 0
    for i in range(len(row)):
        assert(row[i] in "FB")
        if row[i] == "B":
            res = res | (1 << 6-i)
    return res


def get_column(column):
    assert(len(column) == 3)
    res = 0
    for i in range(len(column)):
        assert(column[i] in "RL")
        if column[i] == "R":
            res = res | (1 << 2-i)
    return res


def get_id(seat):
    return get_row(seat[:7]) * 8 + get_column(seat[7:])


def max_id(bps):
    res = 0
    for bp in bps:
        res = max(res, get_id(bp))
    return res


assert(get_row("FBFBBFF") == 44)
assert(get_column("RLR") == 5)
assert(get_id("BFFFBBFRRR") == 567)


def find_empty_seat(bps):
    seats = [0] * (2**10)
    for bp in bps:
        seats[get_id(bp)] = 1

    exist = False # No viable seats at start ids
    for i in range(len(seats)):
        if seats[i] == 0 and exist:
            return i
        if seats[i] == 1:
            exist = True


if __name__ == "__main__":
    bps = []
    with open("input", "r") as file:
        for line in file:
            bps.append(line.rstrip())

    # part 1
    print(max_id(bps))
    # print 2
    print(find_empty_seat(bps))



