
def crab_game(start_cup, cups, iterations):
    current_cup = start_cup
    while iterations > 0:
        # Choose 3
        chosen_cups = []
        chosen_cup = cups[current_cup]
        for _ in range(3):
            chosen_cups.append(chosen_cup)
            chosen_cup = cups[chosen_cup]
        # Destination cup
        dest_cup = max(cups) if current_cup == 1 else current_cup-1
        while dest_cup not in cups or dest_cup in chosen_cups:
            dest_cup = max(cups) if dest_cup == 1 else dest_cup-1
        # Move cups
        # Connect current with after last chosen
        cups[current_cup] = cups[chosen_cups[-1]]
        # Connect destination with first chosen
        tmp = cups[dest_cup]
        cups[dest_cup] = chosen_cups[0]
        # Connect last chosen with after destination
        cups[chosen_cups[-1]] = tmp
        # Step
        current_cup = cups[current_cup]
        iterations -= 1
        if iterations % 100000 == 0:
            print("Iterations left: ", iterations)

    string = ""
    current_cup = cups[1]
    while current_cup != 1 and max(cups) < 10:
        string += str(current_cup)
        current_cup = cups[current_cup]
    return string, cups[1] * cups[cups[1]]


if __name__ == "__main__":
    cups = dict()
    with open("input", "r") as file:
        tmp_cups = [int(x) for x in file.readline().rstrip()]
        for i in range(len(tmp_cups)):
            cups[tmp_cups[i]] = tmp_cups[(i+1)%len(tmp_cups)]
            if i == 0:
                start_cup = tmp_cups[i]
            if i == len(tmp_cups)-1:
                last_cup = tmp_cups[i]

    # part 1
    # p1,p2 = crab_game(start_cup, cups.copy(), 100)
    # print(p1)
    # part 2
    cups[last_cup] = max(cups)+1
    for i in range(max(cups)+1,1000000):
        cups[i] = i+1
    cups[1000000] = start_cup
    print(cups[1000000-1])
    p1,p2 = crab_game(start_cup, cups, 10000000)
    print(p2)


