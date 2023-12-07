

from enum import IntEnum

class Hands(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

def classify(cards):
    count = dict()
    for card in cards:
        if card in count:
           count[card] += 1
        else:
            count[card] = 1
    if len(count) == 1:
        return Hands.FIVE_OF_A_KIND
    elif len(count) == 2: # Four of a kind, Full house
        for n_of_cards in count.values():
            if n_of_cards == 4:
                return Hands.FOUR_OF_A_KIND
            if n_of_cards == 3:
                return Hands.FULL_HOUSE
    elif len(count) == 3: # Three of a kind, Two pair
        for n_of_cards in count.values():
            if n_of_cards == 3:
                return Hands.THREE_OF_A_KIND
            if n_of_cards == 2:
                return Hands.TWO_PAIR
    elif len(count) == 4:
        return Hands.ONE_PAIR
    elif len(count) == 5:
        return Hands.HIGH_CARD


assert(classify("AAAAA") == Hands.FIVE_OF_A_KIND)
assert(classify("AA8AA") == Hands.FOUR_OF_A_KIND)
assert(classify("23332") == Hands.FULL_HOUSE)
assert(classify("TTT98") == Hands.THREE_OF_A_KIND)
assert(classify("23432") == Hands.TWO_PAIR)
assert(classify("A23A4") == Hands.ONE_PAIR)
assert(classify("23456") == Hands.HIGH_CARD)


class CompRes(IntEnum):
    LESS_THAN = -1
    EQUAL = 0
    GREATER_THAN = 1

def compare_cards(card1, card2):
    order = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    p1 = order.index(card1)
    p2 = order.index(card2)
    if p1 == p2:
        return CompRes.EQUAL
    if p1 < p2:
        return CompRes.LESS_THAN
    if p1 > p2:
        return CompRes.GREATER_THAN


def compare_hands(hand1, hand2):
    class1 = classify(hand1)
    class2 = classify(hand2)
    if class1 < class2:
        return CompRes.LESS_THAN
    if class1 > class2:
        return CompRes.GREATER_THAN
    for i in range(len(hand1)):
        res = compare_cards(hand1[i], hand2[i])
        if res != CompRes.EQUAL:
            return res
    return CompRes.EQUAL


assert(compare_hands("33332", "2AAAA") == CompRes.GREATER_THAN)
assert(compare_hands("77888", "77788") == CompRes.GREATER_THAN)
assert(compare_hands("KK677", "KTJJT") == CompRes.GREATER_THAN)
assert(compare_hands("T55J5", "QQQJA") == CompRes.LESS_THAN)

def part_one(lines):
    res = 0
    hand_bet_mapping = dict()
    for line in lines:
        hand, bet = line.split()
        hand_bet_mapping[hand] = int(bet)

    sorted_hands = []
    for hand in hand_bet_mapping.keys():
        if len(sorted_hands) == 0:
            sorted_hands.append(hand)
        else:
            for i in range(len(sorted_hands)):
                if compare_hands(hand, sorted_hands[i]) == CompRes.LESS_THAN:
                    sorted_hands.insert(i, hand)
                    break
                if i == len(sorted_hands)-1:
                    sorted_hands.append(hand)

    for i in range(len(sorted_hands)):
        hand = sorted_hands[i]
        res += hand_bet_mapping[hand]*(i+1)

    return res



def classify_with_joker(cards):
    count = dict()
    for card in cards:
        if card in count:
           count[card] += 1
        else:
            count[card] = 1

    if "J" not in count:
        return classify(cards)

    if count["J"] == 5 or count["J"] == 4:
        return Hands.FIVE_OF_A_KIND
    elif count["J"] == 3:
        if len(count) == 2: # Two non-J cards are the same
            return Hands.FIVE_OF_A_KIND
        elif len(count) == 3: # Two non-J cards are different
            return Hands.FOUR_OF_A_KIND
    elif count["J"] == 2:
        if len(count) == 2: # Three non-J cards are the same
            return Hands.FIVE_OF_A_KIND
        if len(count) == 3: # Two out of three non-J cards are the same
            return Hands.FOUR_OF_A_KIND
        if len(count) == 4: # All three non-J cards are different
            return Hands.THREE_OF_A_KIND
    elif count["J"] == 1:
        if len(count) == 2: # All four non-J cards are the same
            return Hands.FIVE_OF_A_KIND
        if len(count) == 3: # Either three out of four non-J cards are the same or there are two pair of non-J cards
            if 3 in count.values():
                return Hands.FOUR_OF_A_KIND
            else:
                return Hands.FULL_HOUSE
        if len(count) == 4: # Two of the four non-J cards are the same
            return Hands.THREE_OF_A_KIND
        if len(count) == 5: # All four non-J cards are different
            return Hands.ONE_PAIR


assert(classify_with_joker("QJJQ2") == Hands.FOUR_OF_A_KIND)
assert(classify_with_joker("32T3K") == Hands.ONE_PAIR)
assert(classify_with_joker("KK677") == Hands.TWO_PAIR)
assert(classify_with_joker("T55J5") == Hands.FOUR_OF_A_KIND)
assert(classify_with_joker("KTJJT") == Hands.FOUR_OF_A_KIND)
assert(classify_with_joker("QQQJA") == Hands.FOUR_OF_A_KIND)


def compare_cards_with_joker(card1, card2):
    order = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    p1 = order.index(card1)
    p2 = order.index(card2)
    if p1 == p2:
        return CompRes.EQUAL
    if p1 < p2:
        return CompRes.LESS_THAN
    if p1 > p2:
        return CompRes.GREATER_THAN


def compare_hands_with_joker(hand1, hand2):
    class1 = classify_with_joker(hand1)
    class2 = classify_with_joker(hand2)
    if class1 < class2:
        return CompRes.LESS_THAN
    if class1 > class2:
        return CompRes.GREATER_THAN
    for i in range(len(hand1)):
        res = compare_cards_with_joker(hand1[i], hand2[i])
        if res != CompRes.EQUAL:
            return res
    return CompRes.EQUAL


assert(compare_hands_with_joker("JKKK2", "QQQQ2") == CompRes.LESS_THAN)
assert(compare_hands_with_joker("33332", "2AAAA") == CompRes.GREATER_THAN)
assert(compare_hands_with_joker("77888", "77788") == CompRes.GREATER_THAN)
assert(compare_hands_with_joker("KK677", "KTJJT") == CompRes.LESS_THAN)
assert(compare_hands_with_joker("T55J5", "QQQJA") == CompRes.LESS_THAN)


def part_two(lines):
    res = 0
    hand_bet_mapping = dict()
    for line in lines:
        hand, bet = line.split()
        hand_bet_mapping[hand] = int(bet)

    sorted_hands = []
    for hand in hand_bet_mapping.keys():
        if len(sorted_hands) == 0:
            sorted_hands.append(hand)
        else:
            for i in range(len(sorted_hands)):
                if compare_hands_with_joker(hand, sorted_hands[i]) == CompRes.LESS_THAN:
                    sorted_hands.insert(i, hand)
                    break
                if i == len(sorted_hands)-1:
                    sorted_hands.append(hand)

    for i in range(len(sorted_hands)):
        hand = sorted_hands[i]
        res += hand_bet_mapping[hand]*(i+1)

    return res


if __name__ == "__main__":
    lines = []
    with open("input", "r") as fd:
        lines = [x.strip() for x in fd]

    print(part_one(lines))

    print(part_two(lines))
