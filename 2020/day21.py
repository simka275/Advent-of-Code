
def count_ok_ingredients(dishes, allergens):
    tot_ingr = set()
    bad_ingr = set()
    for dish in dishes:
        tot_ingr = tot_ingr.union(dish)

    for alle in allergens:
        bad_ingr = bad_ingr.union(allergens[alle])

    good_ingr = tot_ingr - bad_ingr
    res = 0
    for ingr in good_ingr:
        for dish in dishes:
            if ingr in dish:
                res += 1
    return res


def danger_list(allergens):
    print(allergens)
    solved = []
    while True:
        changes = False
        for name in allergens:
            if len(allergens[name]) == 1 and name not in solved:
                solved.append(name)
                ingr = next(iter(allergens[name]))
                changes = True
                break

        if not changes:
            break

        for other in allergens:
            if name == other:
                continue
            if ingr in allergens[other]:
                allergens[other].remove(ingr)

    print(allergens)
    res = ""
    for name in sorted(allergens):
        res += "{},".format(next(iter(allergens[name])))
    return res[:-1]


if __name__ == "__main__":
    ingredients = set()
    dishes = []
    allergens = dict()
    with open("input", "r") as file:
        for line in file:
            ingr, alls = line.rstrip().split(" (contains ")
            ingr = ingr.split()
            alls = alls[:-1].split(", ")
            dishes.append(ingr)
            ingredients = ingredients.union(ingr)
            for al in alls:
                if al in allergens:
                    allergens[al] = allergens[al].intersection(ingr)
                else:
                    allergens[al] = set(ingr)

    # part 1
    print(count_ok_ingredients(dishes, allergens))
    # part 2
    print(danger_list(allergens))
