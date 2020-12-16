
def numberwang(numbers, stop_turn):
    current_turn = len(numbers)+1
    last_seen = dict()
    for i in range(len(numbers)):
        last_seen[numbers[i]] = i+1

    while current_turn <= stop_turn:
        n = numbers[current_turn-2]
        n_turn = current_turn-1
        if n in last_seen and last_seen[n] != n_turn:
            numbers.append(n_turn - last_seen[n])
        else:
            numbers.append(0)
        last_seen[n] = n_turn
        current_turn += 1
    return numbers[-1]

assert(numberwang([0,3,6], 10) == 0)
assert(numberwang([1,3,2], 2020) == 1)
assert(numberwang([2,1,3], 2020) == 10)

if __name__ == "__main__":
    with open("input", "r") as file:
        numbers = [int(x) for x in file.readline().rstrip().split(",")]

    # part 1
    print(numberwang(numbers, 2020))

    # part 2
    print(numberwang(numbers, 30000000))