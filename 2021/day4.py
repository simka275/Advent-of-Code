import copy

def mark_board(number, board):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == number:
                board[y][x] = ""

def is_winner(board):
    # row
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] != "":
                break
            if x == len(board)-1:
                return True
    # cols
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] != "":
                break
            if y == len(board)-1:
                return True
    # diags
    # for i in range(len(board)):
    #     if board[i][i] != "":
    #         break
    #     if i == len(board)-1:
    #         return True
    # for i in range(len(board)):
    #     if board[i][len(board)-1-i] != "":
    #         break
    #     if i == len(board)-1:
    #         return True


assert is_winner([["","",""],["1","1","1"],["1","1","1"]])
assert is_winner([["1","","1"],["1","","1"],["1","","1"]])
# assert is_winner([["","1","1"],["1","","1"],["1","1",""]])
# assert is_winner([["1","1",""],["1","","1"],["","1","1"]])
assert not is_winner([["1","1","1"],["1","","1"],["","1","1"]]) 


def sum_board(board):
    sum = 0
    for y in range(len(board)):
        for x in range(len(board)):
            sum += 0 if board[y][x] == "" else int(board[y][x])
    return sum
            

def calc_winning_board_score(numbers, boards):
    for number in numbers:
        for board in boards:
            mark_board(number, board)
            if is_winner(board):
                return int(number)*sum_board(board)


def calc_winning_board_score(numbers, boards):
    for number in numbers:
        for board in boards:
            mark_board(number, board)
            if is_winner(board):
                return int(number)*sum_board(board)


def calc_last_winning_board_score(numbers, boards):
    winners = []
    losers = boards
    for number in numbers:
        new_losers = []
        for board in losers:
            mark_board(number, board)
            if is_winner(board):
                winners.append([number, board])
            else:
                new_losers.append(board)
        losers = new_losers
    last = winners[-1]
    return int(last[0])*sum_board(last[1])
        

if __name__ == "__main__":
    numbers = []
    boards = []
    with open("input", "r") as file:
        board = []
        for line in file:
            if "," in line:
                numbers = line.strip().split(",")
            elif not line.strip():
                if board:
                    boards.append(board)
                board = []
            else:
                board.append([x for x in line.strip().split()])
        if board:
            boards.append(board)
    
    # p1
    print(calc_winning_board_score(numbers, copy.deepcopy(boards)))

    # p2
    print(calc_last_winning_board_score(numbers, copy.deepcopy(boards)))
