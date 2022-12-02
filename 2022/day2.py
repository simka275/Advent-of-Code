

def part_one(matches):
    score = 0
    mappings = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}

    for opponent_move, player_move in matches:
        score += mappings[player_move]
        if mappings[opponent_move] == mappings[player_move]-1 or mappings[opponent_move] == mappings[player_move]+2: # win
            score += 6
        elif mappings[opponent_move] == mappings[player_move]: # even
            score += 3
    return score


def part_two(matches):
    score = 0
    mappings = {"A": 1, "B": 2, "C": 3, "X": 0, "Y": 3, "Z": 6}
    for opponent_move, result in matches:
        score += mappings[result]
        if result == "X": # lose
            score += mappings[opponent_move]+2 if opponent_move == "A" else mappings[opponent_move]-1
        elif result == "Y": # draw
            score += mappings[opponent_move]
        elif result == "Z": # win
            score += mappings[opponent_move]-2 if opponent_move == "C" else mappings[opponent_move]+1
    return score


if __name__ == "__main__":
    matches = []
    with open("input", "r") as fd:
        for line in fd:
            matches.append(line.strip().split(" "))

    print(part_one(matches))

    print(part_two(matches))
