
def is_valid(code, preamble_len, pos):
    for i in range(pos-preamble_len,pos):
        for j in range(i+1,pos):
            if code[i] + code[j] == code[pos]:
                return True
    return False


def find_invalid(code, preamble_len):
    for i in range(preamble_len, len(code)):
        if not is_valid(code, preamble_len, i):
            return code[i]


def find_weakness(code, target):
    for i in range(0, len(code)-1):
        cur_sum = code[i]
        small = code[i]
        big = code[i]
        for j in range(i+1,len(code)):
            cur_sum += code[j]
            small = min(small, code[j])
            big = max(big, code[j])
            if cur_sum == target:
                return small + big

if __name__ == "__main__":
    code = []
    with open("input", "r") as file:
        for line in file:
            code.append(int(line))

    # part 1
    print(find_invalid(code, 25))

    # part 2
    print(find_weakness(code, find_invalid(code, 25)))