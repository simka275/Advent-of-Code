

def roll_deterministic_dice(p1_start, p2_start):
    p1_pos = p1_start
    p2_pos = p2_start
    p1_score = 0
    p2_score = 0
    dice_roll = 0
    dice = range(1,101)
    while True:
        steps = dice[dice_roll % 100] + dice[(dice_roll+1) % 100] + dice[(dice_roll+2) % 100]
        p1_pos = (p1_pos + steps) % 10
        p1_score += p1_pos if p1_pos != 0 else 10
        dice_roll += 3

        if p1_score >= 1000:
            return (dice_roll)*p2_score

        steps = dice[dice_roll % 100] + dice[(dice_roll+1) % 100] + dice[(dice_roll+2) % 100]
        p2_pos = (p2_pos + steps) % 10
        p2_score += p2_pos if p2_pos != 0 else 10
        dice_roll += 3

        if p2_score >= 1000:
            return (dice_roll)*p1_score


def roll_dirac_dice(p1_start, p2_start):
    pos_and_score = {(p1_start,p2_start,0,0): 1}
    p1_wins = 0
    p2_wins = 0
    steps = [(s1,s2,s3) for s1 in (1,2,3) for s2 in (1,2,3) for s3 in (1,2,3)]
    while pos_and_score:
        new_pos_and_score = {}
        for (p1_pos,p2_pos,p1_score,p2_score), count in pos_and_score.items():
            for p1_steps in steps:
                p1_step = sum(p1_steps)
                new_p1_pos = (p1_pos + p1_step) % 10
                new_p1_score = p1_score + (new_p1_pos if new_p1_pos != 0 else 10)
                if new_p1_score >= 21:
                    p1_wins += count
                    continue

                if (new_p1_pos,p2_pos,new_p1_score,p2_score) in new_pos_and_score:
                    new_pos_and_score[(new_p1_pos,p2_pos,new_p1_score,p2_score)] += count
                else:
                    new_pos_and_score[(new_p1_pos,p2_pos,new_p1_score,p2_score)] = count

        pos_and_score = {}
        for (p1_pos,p2_pos,p1_score,p2_score), count in new_pos_and_score.items():
            for p2_steps in steps:
                p2_step = sum(p2_steps)
                new_p2_pos = (p2_pos + p2_step) % 10
                new_p2_score = p2_score + (new_p2_pos if new_p2_pos != 0 else 10)
                if new_p2_score >= 21:
                    p2_wins += count
                    continue

                if (p1_pos,new_p2_pos,p1_score,new_p2_score) in pos_and_score:
                    pos_and_score[(p1_pos,new_p2_pos,p1_score,new_p2_score)] += count
                else:
                    pos_and_score[(p1_pos,new_p2_pos,p1_score,new_p2_score)] = count

    return max(p1_wins, p2_wins)



if __name__ == "__main__":
    p1_start = None
    p2_start = None
    with open("input", "r") as file:
        p1_start = int(file.readline().strip().split(": ")[1])
        p2_start = int(file.readline().strip().split(": ")[1])

    print(roll_deterministic_dice(p1_start, p2_start))

    print(roll_dirac_dice(p1_start, p2_start))