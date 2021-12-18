
import math

def explode(_number):
    number = _number.copy()
    reader_pos = 0
    depth = 0
    while reader_pos < len(number):
        if number[reader_pos] == "[":
            depth += 1
            reader_pos += 1
        elif number[reader_pos] == "]":
            depth -= 1
            reader_pos += 1
        elif depth <= 4 or number[reader_pos] == ",":
            reader_pos += 1
        elif (reader_pos + 2) < len(number) and number[reader_pos+2] == "[":
            reader_pos += 1
        else: # explode
            lhs = int(number[reader_pos])
            prev_nr_index = None
            for i in range(0, reader_pos):
                if number[i] not in ["[","]",","]:
                    prev_nr_index = i
            if prev_nr_index:
                number[prev_nr_index] = str(int(number[prev_nr_index]) + lhs)

            rhs = int(number[reader_pos+2])
            next_nr_index = None
            for i in range(reader_pos+3,len(number)):
                if number[i] not in ["[","]",","]:
                    next_nr_index = i
                    break
            if next_nr_index:
                number[next_nr_index] = str(int(number[next_nr_index]) + rhs)

            number = number[:reader_pos-1] + ["0"] + number[reader_pos+4:]
            break
    return number


def split(_number):
    number = _number.copy()
    reader_pos = 0
    while reader_pos < len(number):
        if number[reader_pos] not in ["[","]",","] and int(number[reader_pos]) > 9: # split
            lhs = int(number[reader_pos]) // 2
            rhs = int(number[reader_pos]) - lhs
            number = number[:reader_pos] + ["[", str(lhs), ",", str(rhs), "]"] + number[reader_pos+1:]
            break
        reader_pos += 1
    return number


def reduce(_number):
    res = explode(_number)
    if res != _number:
        return res
    return split(_number)

assert(reduce(list("[[[[[9,8],1],2],3],4]")) == list("[[[[0,9],2],3],4]"))
assert(reduce(list("[7,[6,[5,[4,[3,2]]]]]")) == list("[7,[6,[5,[7,0]]]]"))
assert(reduce(list("[[6,[5,[4,[3,2]]]],1]")) == list("[[6,[5,[7,0]]],3]"))
assert(reduce(list("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")) == list("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"))
assert(reduce(list("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")) == list("[[3,[2,[8,0]]],[9,[5,[7,0]]]]"))
assert(reduce(list("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")) == list("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"))
assert(reduce(list("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")) == list("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"))


def add_numbers(numbers):
    res = numbers[0]
    for i in range(1,len(numbers)):
        res = ["["] + res + [","] + numbers[i] + ["]"]
        while True:
            reduced = reduce(res)
            if reduced == res:
                res = reduced
                break
            res = reduced
    return res

assert(add_numbers([list("[[[[4,3],4],4],[7,[[8,4],9]]]"), list("[1,1]")]) == list("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"))
assert("".join(add_numbers([list("[1,1]"), list("[2,2]"), list("[3,3]"), list("[4,4]")])) == "[[[[1,1],[2,2]],[3,3]],[4,4]]")
assert("".join(add_numbers([list("[1,1]"), list("[2,2]"), list("[3,3]"), list("[4,4]")])) == "[[[[1,1],[2,2]],[3,3]],[4,4]]")
assert("".join(add_numbers([list("[1,1]"), list("[2,2]"), list("[3,3]"), list("[4,4]"), list("[5,5]")])) == "[[[[3,0],[5,3]],[4,4]],[5,5]]")
assert("".join(add_numbers([list("[1,1]"), list("[2,2]"), list("[3,3]"), list("[4,4]"), list("[5,5]"), list("[6,6]")])) == "[[[[5,0],[7,4]],[5,5]],[6,6]]")
assert("".join(add_numbers([list("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]"), list("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")])) == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")


def get_magnitude(number):
    if type(number) == int:
        return number
    return 3*get_magnitude(number[0])+2*get_magnitude(number[1])

assert(get_magnitude(eval("[9,1]")) == 29)
assert(get_magnitude(eval("[1,9]")) == 21)
assert(get_magnitude(eval("[[9,1],[1,9]]")) == 129)


def get_max_magnitude_pair(numbers):
    res = -math.inf
    for n1 in numbers:
        for n2 in numbers:
            sum = add_numbers([n1,n2])
            res = max(res, get_magnitude(eval("".join(sum))))
    return res


if __name__ == "__main__":
    numbers = []
    with open("input", "r") as file:
        for line in file:
            numbers.append(list(line.strip()))

    # p1
    tot_sum = add_numbers(numbers)
    magnitude = get_magnitude(eval("".join(tot_sum)))
    print(magnitude)

    # p2
    print(get_max_magnitude_pair(numbers))