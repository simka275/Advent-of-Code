
import math

# Calculate modular multiplicative inverse
# i.e. x such that a*x is congruent with 1 mod m
# Note: Only works if m and a is coprime
def mod_mult_inv(a,m):
    if math.gcd(a,m) != 1:
        raise Exception("{} and {} are not coprime".format(a,m))
    return pow(a, m-2, m)


def rev(i,size):
    return (size-1-i)%size

assert rev(0,10) == 9
assert rev(1,10) == 8
assert rev(8,10) == 1


def cut(n,i,size):
    return (size-n+i)%size

assert cut(3,4,10) == 1
assert cut(3,8,10) == 5
assert cut(3,1,10) == 8
assert cut(-4,4,10) == 8
assert cut(-4,8,10) == 2
assert cut(-4,1,10) == 5


def incr(n,i,size):
    return (n*i) % size

assert incr(3,1,10) == 3
assert incr(3,2,10) == 6
assert incr(3,6,10) == 8


def inv_rev(i,size):
    return rev(i,size)

assert inv_rev(0,10) == 9
assert inv_rev(1,10) == 8
assert inv_rev(8,10) == 1


def inv_cut(n,i,size):
    return (size+n+i)%size

assert inv_cut(3,4,10) == 7
assert inv_cut(3,8,10) == 1
assert inv_cut(3,1,10) == 4
assert inv_cut(-4,4,10) == 0
assert inv_cut(-4,8,10) == 4
assert inv_cut(-4,1,10) == 7


def inv_incr(n,i,size):
    return (mod_mult_inv(n,size)*i) % size

assert inv_incr(3,1,11) == 4
assert inv_incr(3,3,11) == 1
assert inv_incr(3,10,11) == 7


# Returns index of card at index after completed shuffle
def shuffle(instructions, index, size):
    for line in instructions:
        if line.find("deal into new stack") != -1:
            index = rev(index, size)
        elif line.find("cut") != -1:
            _, n = line.strip("\n").split(" ")
            n = int(n)
            index = cut(n,index,size)
        elif line.find("deal with increment") != -1:
            _, _, _, n = line.strip("\n").split(" ")
            n = int(n)
            index = incr(n,index,size)
        else:
            raise Exception("Not implemented cmd: {}".format(line))
    return index


# Returns the starting pos of card at index after a shuffle
def inverse_shuffle(instructions, index, size):
    instructions.reverse()
    for line in instructions:
        if line.find("deal into new stack") != -1:
            index = inv_rev(index, size)
        elif line.find("cut") != -1:
            _, n = line.strip("\n").split(" ")
            n = int(n)
            index = inv_cut(n,index,size)
        elif line.find("deal with increment") != -1:
            _, _, _, n = line.strip("\n").split(" ")
            n = int(n)
            index = inv_incr(n,index,size)
        else:
            raise Exception("Not implemented cmd: {}".format(line))
    return index
    

# Applying all linear function (inverses function above) is
# the same as applying on linear function new_index f(current_index) = a*current_index + b % size
# Determine coefficient by:
# Let y = f(index) <=> y = (a*index+b) % size
# z = f(y) <=> z = (a*y+b) % size
# z-y = ((a*y+b) -(a*index+b)) % size
# z-y = (a*(y-index)) % size
# a = (z-y)* modular_mult_inverse(y-index, size) % size
# Note: Uses Fermats little theorem to calc mod mult inverse so if y-index isn't coprime this fails
# Source: https://old.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnifwk/
def det_coeff_inv_shuffle(instructions, index, size):
    y = inverse_shuffle(instructions.copy(), index, size)
    z = inverse_shuffle(instructions.copy(), y, size)
    a = ((z-y)*mod_mult_inv(y-index,size)) % size
    b = (y-a*index) % size
    return a, b


def part_one():
    with open("input", "r") as file:
        instructions = []
        for line in file:
            instructions.append(line)

        print(shuffle(instructions, 2019, 10007))
        print(inverse_shuffle(instructions, 3074, 10007))


def part_two():
    with open("input", "r") as file:
        instructions = []
        for line in file:
            instructions.append(line)

        size = 119315717514047
        repetitions = 101741582076661

        # One repetition of the (inverse) shuffle can be describe as a linear function
        # f(i) = a*i+b (see reasoning in function comments) 
        # Repeating the shuffle another time can then be describe as f(f(i)) = a*f(i)+b = a*(a*i+b)+b
        # a^2*i +ab +b. Another repeat: f(f(f(i))) = a*(a^2*i +ab +b) +b = a^3*i +a^2*b +ab +b
        # Applying the shuffle n times: f^n(i) = a^n*i +a^(n-1)*b +a^(n-2)*b + ... + a^2*b +ab +b
        # The additions excluding a^n*i describes a geometric series a^(n-k)*n where k from 0 to n-1
        # The geometric series can be simplified to (a^n-1)*b*(a-1)^(-1), and since it is modular arithmetic
        # (a-1) is the mod multiplicate inverse such that (a-1)*(a-1)^(-1) is congruent to 1 mod n
        # To calcualte this inverse we can again use Fermats little theorem (since n is a prime number and 
        # therefore a-1 and n are coprime)
        # Source: https://old.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnifwk/
        a, b = det_coeff_inv_shuffle(instructions, 2020, size)
        print((pow(a,repetitions,size)*2020+(pow(a,repetitions,size)-1)*mod_mult_inv(a-1,size)*b)%size)


if __name__ == "__main__":
    # part_one()
    part_two()