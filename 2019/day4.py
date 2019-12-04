

def is_valid_one(pw):
    have_adjacent = False
    # six digit
    if len(pw) != 6:
        return False
    prev = ""
    counts = dict()
    for l in pw:
        counts[l] = pw.count(l)
        # increasing
        if prev > l:
            return False
        prev = l
    # two adjecent same
    for _,v in counts.items():
        if v > 1:
            have_adjacent = True
    return have_adjacent

assert is_valid_one("111111")
assert not is_valid_one("223450")
assert not is_valid_one("123789")


def part_one(range_string):
    low, high = [int(x) for x in range_string.split("-")]
    valid_pws = 0
    for pw in range(low,high+1):
        if is_valid_one(str(pw)):
            valid_pws+=1
    print(valid_pws)
        

def is_valid_two(pw):
    # six digit
    if len(pw) != 6:
        return False
    prev = ""
    counts = dict()
    for l in pw:
        counts[l] = pw.count(l)
        # increasing
        if prev > l:
            return False
        prev = l
    # A pair not belonging to long sequence
    if not any(v==2 for v in counts.values()):
        return False
    return True

assert is_valid_two("112233")
assert not is_valid_two("123444")
assert is_valid_two("111122")


def part_two(range_string):
    low, high = [int(x) for x in range_string.split("-")]
    valid_pws = 0
    for pw in range(low,high+1):
        if is_valid_two(str(pw)):
            valid_pws+=1
    print(valid_pws)


if __name__ == "__main__":
    # part_one("178416-676461")
    part_two("178416-676461")