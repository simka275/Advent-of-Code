
def count_easy_digits(digits):
    res = 0
    for displayed in [x[1] for x in digits]:
        for digit in displayed:
            if len(digit) in [2,4,3,7]: # 1,4,7,8
                res += 1
    return res


def count_intersection(str1, str2):
    res = 0
    for c in str1:
        if c in str2:
            res += 1
    return res


def determine_numbers(wires):
    res = dict()
    # Find easy digits
    filtered_wires = []
    for wire in wires:
        if len(wire) == 2:
            res["1"] = wire
        elif len(wire) == 4:
            res["4"] = wire
        elif len(wire) == 3:
            res["7"] = wire
        elif len(wire) == 7:
            res["8"] = wire
        else:
            filtered_wires.append(wire)

    # find rest
    for wire in filtered_wires:
        if len(wire) == 5 and count_intersection(wire, res["4"]) == 2:
            res["2"] = wire
        elif len(wire) == 5 and count_intersection(wire, res["1"]) == 2:
            res["3"] = wire
        elif len(wire) == 5 and count_intersection(wire, res["4"]) == 3:
            res["5"] = wire
        elif len(wire) == 6 and count_intersection(wire, res["1"]) == 1:
            res["6"] = wire
        elif len(wire) == 6 and count_intersection(wire, res["4"]) == 4:
            res["9"] = wire
        else:
            res["0"] = wire
    return res


def count_digits(digits):
    res = 0
    for ds in digits:
        numbers_mapping = determine_numbers(ds[0])
        display = ""
        for displayed_nr in ds[1]:
            for nr,wire in numbers_mapping.items():
                if sorted(wire) == sorted(displayed_nr):
                    display += nr
                    break
        res += int(display)
    return res


if __name__ == "__main__":
    digits = []
    with open("input", "r") as file:
        for line in file:
            wires, displayed = line.strip().split(" | ")
            digits.append(([x for x in wires.split()], [x for x in displayed.split()]))

    # p1
    print(count_easy_digits(digits))

    # p2
    print(count_digits(digits))