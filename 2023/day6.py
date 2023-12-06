
import math

def part_one(lines):
    res = 1
    times = [int(x) for x in lines[0].split("Time:")[-1].split()]
    distances = [int(x) for x in lines[1].split("Distance:")[-1].split()]

    # Quadratic polynomial
    # Need to find t = t_record/2 +- sqrt(t_record^2 - 4*distance)/2
    for i in range(len(distances)):
        t_record = times[i]
        distance = distances[i]
        t1 = t_record/2 - math.sqrt(t_record**2 - 4*distance)/2
        t2 = t_record/2 + math.sqrt(t_record**2 - 4*distance)/2
        if t1 == int(t1): # If solution is integer
            t1 = t1 + 1
        t1 = math.ceil(t1) # Next whole number for lower limit
        if t2 == int(t2): # If solution is integer
            t2 = t2 - 1
        t2 = math.floor(t2) # Prev whole number for upper limit
        alternatives = t2 - t1 + 1
        res *= alternatives

    return res

def part_two(lines):
    t_record = int("".join([x for x in lines[0].split("Time:")[-1].split()]))
    distance = int("".join([x for x in lines[1].split("Distance:")[-1].split()]))

    t1 = t_record/2 - math.sqrt(t_record**2 - 4*distance)/2
    t2 = t_record/2 + math.sqrt(t_record**2 - 4*distance)/2
    if t1 == int(t1): # If solution is integer
        t1 = t1 + 1
    t1 = math.ceil(t1) # Next whole number for lower limit
    if t2 == int(t2): # If solution is integer
        t2 = t2 - 1
    t2 = math.floor(t2) # Prev whole number for upper limit
    alternatives = t2 - t1 + 1
    return alternatives


if __name__ == "__main__":
    lines = []
    with open("input", "r") as fd:
        lines = [x.strip() for x in fd]

    print(part_one(lines))

    print(part_two(lines))
