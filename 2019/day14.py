import queue

def create_formula(line):
    ingredients, res = line.strip("\n").split(" => ")
    quantity, name = res.split(" ")
    ingredients = ingredients.split(", ")
    ingredients = [ tuple(x.split(" ")) for x in ingredients ]
    return name, quantity, ingredients

"""
def break_down(resource, quantity, reactions, storage):
    # Init storage of resource
    if resource not in storage:
        storage[resource] = 0

    # Handle base case
    if resource == "ORE":
        storage[resource] += quantity
        return

    # Break down
    req_quantity = int(reactions[resource]["quantity"])
    available_quantity = quantity + storage[resource]
    multiple, remainder = available_quantity // req_quantity, available_quantity % req_quantity
    storage[resource] = remainder
    # If cannot be broken down further store what we have
    if multiple == 0:
        return

    for ingredient in reactions[resource]["ingredients"]:
        name, qnty = ingredient[1], multiple*int(ingredient[0])
        break_down(name, qnty, reactions, storage)
"""
def break_down(resource, quantity, reactions, storage):
    storage[resource] = quantity
    break_down_queue = queue.Queue()
    break_down_queue.put(resource)
    debt = dict()

    while not break_down_queue.empty():
        r = break_down_queue.get()
        
        if r not in debt:
            debt[r] = 0

        # Pay off debt
        if debt[r] > 0:
            if debt[r] <= storage[r]:
                storage[r] -= debt[r]
                debt[r] = 0
            elif debt[r] > storage[r]:
                debt[r] -= storage[r]
                storage[r] = 0

        # Down break down ORE
        if r == "ORE":
            continue

        # Borrow if to completly break down resource r
        req_quantity = int(reactions[r]["quantity"])
        multiple, remainder = storage[r] // req_quantity, storage[r] % req_quantity
        storage[r] = 0
        if remainder != 0:
            multiple += 1
            debt[r] += req_quantity - remainder

        # Queue break down of components and store amount in storage
        for ingredient in reactions[r]["ingredients"]:
            name, qnty = ingredient[1], multiple*int(ingredient[0])
            break_down_queue.put(name)
            if name not in storage:
                storage[name] = qnty
            else:
                storage[name] += qnty

    return storage["ORE"]

def part_one():
    with open("input", "r") as file:
        reactions = dict()
        for line in file:
            res, quantity, ingredients = create_formula(line)
            reactions[res] = {"quantity": quantity, "ingredients": ingredients}
        
        print(reactions)
        storage = dict()
        break_down("FUEL", 1, reactions, storage)
        print(storage)
        print("ORE: {}".format(storage["ORE"]))


def part_two():
    with open("input", "r") as file:
        reactions = dict()
        for line in file:
            res, quantity, ingredients = create_formula(line)
            reactions[res] = {"quantity": quantity, "ingredients": ingredients}
        
        # prev, curr = 0, 0
        # for i in range(1,10):
        #     storage = dict()
        #     break_down("FUEL", i, reactions, storage)
            # curr = storage["ORE"]
            # print("FUEL {0} costs ORE: {1} diff: {2}".format(i, storage["ORE"], curr-prev))
            # print("{},{}".format(i, curr))
            # prev = curr


        # Safe to say resulting amount of fuel should be between 1 and 1 trillion
        # since 1 fuel definitely costs more than 1 ore
        min_fuel, max_fuel = 1, 1000000000000
        while max_fuel-min_fuel > 1:
            fuel = (max_fuel+min_fuel) // 2
            storage = dict()
            ore = break_down("FUEL", fuel, reactions, storage)
            print("MIN {0} MAX {1} CURR FUEL {2} costs ORE: {3}".format(min_fuel, max_fuel, fuel, ore))
            if ore > 1000000000000:
                max_fuel = fuel
            else:
                min_fuel = fuel

        


if __name__ == "__main__":
    # part_one()
    part_two()
