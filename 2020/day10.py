
import bisect


def get_jolt_diffs(adapters):
    cur_jolt = 0
    jolt_diffs = [0,0,0]
    for ad in adapters:
        if ad - cur_jolt > 3:
            break
        jolt_diffs[ad - cur_jolt -1] += 1
        cur_jolt = ad
    jolt_diffs[2] += 1
    return jolt_diffs


"""
Calculate how many new alternatives available with a given numbers of 1 diffs between adapters.
(Starting at 0 jolts in all examples)
Ex.  Adapters of jolt 1,2 have two options, either -> 1 -> 2 -> or -> 2 ->
Ex. 1,2,3 gives 4 paths:  -> 1 -> 2 -> 3 ->, -> 2 -> 3 ->, -> 1 -> 3 ->, or -> 3 ->
When we have more than 3 1 diffs in a row we reach a general case since we can no longer reach this
new diff position from the starting jolt (0 in the examples).
Ex. 1,2,3,4 gives 7 path: paths ... -> 1 -> 4 -> + paths ... -> 2 -> 4 -> + path ... -> 3 -> 4 ->
And this can den be generalized to: Number of paths with n number of 1 diffs in a row is then
#paths to n-1 plus #paths to n-2 plus #paths to n-3
"""
def path_factor(nr_of_ones):
    if nr_of_ones < 2:
        return 1
    elif nr_of_ones == 2:
        return 2
    elif nr_of_ones == 3:
        return 4
    else:
        return path_factor(nr_of_ones-1) + path_factor(nr_of_ones-2) + path_factor(nr_of_ones-3)


def arrangements(adapters):
    res = 1
    diffs = []
    for i in range(len(adapters)):
        if i == 0:
            diffs.append(adapters[i])
        else:
            diffs.append(adapters[i] - adapters[i-1])
    diffs.append(3) # built in adapter diff

    one_counter = 0
    for d in diffs:
        if d == 1:
            one_counter += 1
        elif d == 3:
            res *= path_factor(one_counter)
            one_counter = 0
        else:
            print("!=!==", d)

    return res


if __name__ == "__main__":
    adapters = []
    with open("input", "r") as file:
        for line in file:
            bisect.insort(adapters, int(line.rstrip()))

    # part 1
    print(get_jolt_diffs(adapters)[0] * get_jolt_diffs(adapters)[2])

    # part 2
    print(arrangements(adapters))
