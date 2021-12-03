
def most_common(report, pos):
    counter = 0
    for line in report:
        if line[pos] == "1":
            counter += 1
        elif line[pos] == "0":
            counter -= 1
    return "1" if counter >= 0 else "0"


def calc_power_consumption(report):
    gamma_rate =""
    epsilon_rate = ""
    for i in range(0, len(report[0])):
        gamma_rate += most_common(report, i)

    # NOT
    for c in gamma_rate:
        epsilon_rate += "0" if c == "1" else "1"

    return gamma_rate, epsilon_rate, int(gamma_rate, 2)*int(epsilon_rate, 2)


def calc_life_support_rating(report):
    gamma_rate, epsilon_rate, _ = calc_power_consumption(report)
    oxygen_rating = ""
    co2_scrubber_rating = ""

    filtered = report.copy()
    pos = 0
    while len(filtered) > 1 and pos < len(report[0]):
        filtered = [x for x in filtered if x[pos] == most_common(filtered, pos)]
        pos += 1
    oxygen_rating = filtered.pop()
    
    filtered = report.copy()
    pos = 0
    while len(filtered) > 1 and pos < len(report[0]):
        filtered = [x for x in filtered if x[pos] != most_common(filtered, pos)]
        pos += 1
    co2_scrubber_rating = filtered.pop()
    
    return int(oxygen_rating, 2)*int(co2_scrubber_rating, 2)


if __name__ == "__main__":
    report = []
    with open("input", "r") as file:
        for line in file:
            report.append(line.strip())

    # p1
    print(calc_power_consumption(report)[2])

    # p2
    print(calc_life_support_rating(report))
