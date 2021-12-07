import math


def calc_min_fuel(positions):
    res = math.inf
    start = min(positions)
    end = max(positions)
    for i in range(start,end+1):
        cur_sum = 0
        for crab in positions:
            cur_sum += abs(i-crab)
        res = min(res, cur_sum)
    return res


def calc_min_fuel_inc_rate(positions):
    res = math.inf
    start = min(positions)
    end = max(positions)
    for i in range(start,end+1):
        cur_sum = 0
        for crab in positions:
            steps = abs(i-crab)
            cur_sum += ((steps+1)*steps)/2
        res = min(res, cur_sum)
    return res


if __name__ == "__main__":
    positions = []
    with open("input", "r") as file:
        for line in file:
            positions = [int(x) for x in line.strip().split(",")]

    # p1
    print(calc_min_fuel(positions))

    # p2
    print(calc_min_fuel_inc_rate(positions))