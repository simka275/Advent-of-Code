
def count_incrs(values):
    res = 0
    prev = None
    for v in values:
        if prev and v > prev:
            res += 1
        prev = v
    return res

def count_incrs_window(values):
    res = 0
    prev = None
    for i in range(len(values)-2):
        curr = values[i] + values[i+1] + values[i+2]
        if prev and curr > prev:
            res += 1
        prev = curr
    return res

if __name__ == "__main__":
    depths = []
    with open("input", "r") as file:
        for line in file:
            depths.append(int(line.strip()))

    # part 1
    print(count_incrs(depths))
    # part 2
    print(count_incrs_window(depths))