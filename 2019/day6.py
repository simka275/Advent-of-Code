from queue import PriorityQueue

def add_orbit(orbits, orbitee, orbiter):
    # add orbiter
    if orbitee in orbits.keys():
        orbits[orbitee]["orbiters"].append(orbiter)
    else:
        orbits[orbitee] = {"orbitee": None, "orbiters": [orbiter]}
    # add orbitee to orbiter
    if orbiter in orbits.keys():
        orbits[orbiter]["orbitee"] = orbitee
    else:
        orbits[orbiter] = {"orbitee": orbitee, "orbiters": []}


def calc_orbits(orbits, orbiter):
    orbitee = orbits[orbiter]["orbitee"]
    if orbitee is None:
        return 0
    else:
        return 1 + calc_orbits(orbits, orbitee)


def calc_tot_orbits(orbits):
    res = 0
    for orbiter in orbits:
        res += calc_orbits(orbits, orbiter)
    return res


def part_one():
    with open("input", "r") as file:
        orbits = dict()
        for line in file:
            orbitee, orbiter = line.strip().split(")")
            add_orbit(orbits, orbitee, orbiter)
        print(calc_tot_orbits(orbits))


def min_steps_to_orbiter(orbits, start, end):
    visited = []
    queue = PriorityQueue()
    queue.put((0, start))
    while not queue.empty():
        cost, current = queue.get()
        if current == end:
            return cost
        visited.append(current)
        orbiters = orbits[current]["orbiters"]
        orbitee = orbits[current]["orbitee"]
        # For all orbiters add to queue if not visited
        for orbiter in orbiters:
            if not orbiter in visited:
                queue.put((cost+1, orbiter))
        # if orbitee exist and not in visited add to queue
        if orbitee and orbitee not in visited:
            queue.put((cost+1, orbitee))
    return None


def part_two():
    with open("input", "r") as file:
        orbits = dict()
        for line in file:
            orbitee, orbiter = line.strip().split(")")
            add_orbit(orbits, orbitee, orbiter)
        steps_to_target = min_steps_to_orbiter(orbits, "YOU", "SAN")
        # Minus two since what we are looking for is orbit changes and not 
        # the shortest path. I.e. subtracting one from path since we already are
        # our orbitees orbit and subtracting one from path since we want to be in
        # same orbit as goal, not orbiting around goal
        print(steps_to_target-2)


test_orbits = dict()
for e in "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L".split("\n"):
    orbitee, orbiter = e.split(")")
    add_orbit(test_orbits, orbitee, orbiter)

assert calc_orbits(test_orbits, "D") == 3
assert calc_orbits(test_orbits, "L") == 7
assert calc_orbits(test_orbits, "COM") == 0
assert calc_tot_orbits(test_orbits) == 42

test_orbits = dict()
for e in "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN".split("\n"):
    orbitee, orbiter = e.split(")")
    add_orbit(test_orbits, orbitee, orbiter)

assert min_steps_to_orbiter(test_orbits, "YOU", "SAN") == 6

if __name__ == "__main__":
    # part_one()
    part_two()