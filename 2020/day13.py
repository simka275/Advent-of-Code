
import math


def earliest_departure(start, ids):
    dep_time = math.inf
    bus_id = None
    for d in ids:
        if d == "x":
            continue
        d = int(d)
        r = start % d
        if r == 0:
            dep_time = start
            bus_id = d
        n = start // d
        if d * (n+1) < dep_time:
            dep_time = d * (n+1)
            bus_id = d
    return (dep_time - start) * bus_id


# Extended Euclid
# a*x + b*y = gcd(a,b)
def ext_euclid(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = ext_euclid(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

assert(ext_euclid(35,15)[0]==5)

def modular_multiplicative_inverse(a, m):
    _, x, _ = ext_euclid(a, m)
    return (x % m + m) % m

assert(modular_multiplicative_inverse(3,11) == 4)
assert(modular_multiplicative_inverse(56,5) == 1)
assert(modular_multiplicative_inverse(40,7) == 3)
assert(modular_multiplicative_inverse(35,8) == 3)


# Chinese remainder theorem
def chinese_remainder(b, n):
    N = 1
    x = []
    bNx = []
    # Create big N that is the product of all modulos
    for n_i in n:
        if n_i == "x":
            continue
        N *= n_i
    # x_i is the modular multiplicative inverse of Ni modulo n_i
    for n_i in n:
        if n_i == "x":
            x.append(None)
            continue
        Ni = N // n_i
        x.append(modular_multiplicative_inverse(Ni, n_i))

    # Calculate product of b_i * N_i * x_i
    for i in range(len(n)):
        if n[i] == "x":
            continue
        bNx.append(b[i] * (N // n[i]) * x[i])

    return sum(bNx) % N

assert(chinese_remainder([3,1,6],[5,7,8]) == 78)
assert(chinese_remainder([0,-1,-2,-3], [17,"x",13,19]) == 3417)


if __name__ == "__main__":
    with open("input", "r") as file:
        start = int(file.readline().rstrip())
        ids = [x for x in file.readline().rstrip().split(",")]

    # part 1
    print(earliest_departure(start, ids))

    # part 2
    # For 3 buses with id a,b,c it holds for our solution that
    # a*n_1 = b*n_2 -1 = c*n_3 -2, where our departure time x=a*n_1
    # this can also be written as x is congruent with -1 mod b (or b-1 mod b)
    # this allows us to us chinese remainder theorem
    remainders = []
    for i in range(len(ids)):
        remainders.append(-i)
        if ids[i] != "x":
            ids[i] = int(ids[i])
    print(chinese_remainder(remainders, ids))
