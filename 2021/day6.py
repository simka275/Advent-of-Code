

def calc_fishes(fishes, days):
    res = 0
    for fish in fishes:
        res += how_many_from_one(days+7-fish, dict())
    return res

def how_many_from_one(days, memo):
    if days in memo:
        return memo[days]
    elif days > 7:
        res = how_many_from_one(days-7, memo) + how_many_from_one(days-9, memo)
        memo[days] = res
        return res
    else:
        return 1


if __name__ == "__main__":
    fishes = []
    with open("input", "r") as file:
        for line in file:
            fishes = [int(x) for x in line.strip().split(",")]

    # p1
    print(calc_fishes(fishes,80))

    # p2
    print(calc_fishes(fishes,256))