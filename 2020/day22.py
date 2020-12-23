
def play_combat(player1, player2):
    while player1 and player2:
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        if card1 > card2:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)

    res = 0
    if player1:
        for i in range(len(player1),0,-1):
            res += i*player1[-i]
    else:
        for i in range(len(player2),0,-1):
            res += i*player2[-i]
    return res


def play_recursive_combat(player1, player2):
    states = set()
    while player1 and player2:
        # Check if already seen
        state = ",".join([str(x) for x in player1]) + "|" + ",".join([str(x) for x in player2])
        if state in states: # Rule 1
            return play_recursive_combat(player1, [])
        states.add(state)
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        if len(player1) >= card1 and len(player2) >= card2: # Rule 2
            player1_won, score = play_recursive_combat(player1[:card1], player2[:card2])
            if player1_won:
                player1.append(card1)
                player1.append(card2)
            else:
                player2.append(card2)
                player2.append(card1)
        elif card1 > card2:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)

    score = 0
    if player1:
        for i in range(len(player1),0,-1):
            score += i*player1[-i]
        return True, score
    else:
        for i in range(len(player2),0,-1):
            score += i*player2[-i]
        return False, score


if __name__ == "__main__":
    player1 = []
    player2 = []
    with open("input", "r") as file:
        file.readline() # Player 2
        for line in file:
            if line == "\n":
                break
            player1.append(int(line.rstrip()))
        file.readline() # Player 2:
        for line in file:
            if not line:
                break
            player2.append(int(line.rstrip()))

    # part 1
    print(play_combat(player1.copy(), player2.copy()))
    # part 2
    print(play_recursive_combat(player1.copy(), player2.copy()))
