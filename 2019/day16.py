

def fft(inp, offset):
    base_pattern = [0, 1, 0, -1]

    outp = fft_past_offset(inp, offset)
    if offset >= len(inp)//2:
        return outp

    for i in range(len(inp)//2-1, offset-1, -1):
        s = 0
        for j in  range(len(inp)-1, i-1, -1):
            base_pattern_index = (j+1)//(i+1)
            base_pattern_index %= len(base_pattern)
            s += inp[j]*base_pattern[base_pattern_index]
        outp[i] = abs(s) % 10
    return outp


def fft_past_offset(inp, offset):
    outp = inp.copy()
    s = 0
    llim = len(inp)//2 if offset < len(inp)//2 else offset
    for i in range(len(inp)-1, llim-1, -1):
        s += inp[i]
        outp[i] = abs(s) % 10
    return outp


def fft_repeat(inp, offset, runs):
    res = fft(inp, offset)
    for _ in range(1, runs):
        res = fft(res, offset)
    return res


assert fft([int(x) for x in "12345678"], 0) == [int(x) for x in "48226158"]
assert fft_repeat([int(x) for x in "12345678"], 0, 1) == [int(x) for x in "48226158"]
assert fft_repeat([int(x) for x in "12345678"], 0, 2) == [int(x) for x in "34040438"]
assert fft_repeat([int(x) for x in "12345678"], 0, 3) == [int(x) for x in "03415518"]
assert fft_repeat([int(x) for x in "12345678"], 0, 4) == [int(x) for x in "01029498"]
assert fft_repeat([int(x) for x in "80871224585914546619083218645595"], 0, 100)[:8] == [int(x) for x in "24176176"]
assert fft_repeat([int(x) for x in "19617804207202209144916044189917"], 0, 100)[:8] == [int(x) for x in "73745418"]
assert fft_repeat([int(x) for x in "69317163492948606335995924319873"], 0, 100)[:8] == [int(x) for x in "52432133"]

inp = [int(x) for x in "03036732577212944063491565474664"*10000]
offset = int("".join(map(str, inp[:7])))
assert fft_repeat(inp, offset, 100)[offset:offset+8] == [int(x) for x in "84462026"]
inp = [int(x) for x in "02935109699940807407585447034323"*10000]
offset = int("".join(map(str, inp[:7])))
assert fft_repeat(inp, offset, 100)[offset:offset+8] == [int(x) for x in "78725270"]
inp = [int(x) for x in "03081770884921959731165446850517"*10000]
offset = int("".join(map(str, inp[:7])))
assert fft_repeat(inp, offset, 100)[offset:offset+8] == [int(x) for x in "53553731"]


if __name__ == "__main__":
    with open("input", "r") as file:
        line = file.readline().strip()
        inp = [int(x) for x in line]
        print("".join(map(str, fft_repeat(inp, 0, 100)[:8]))) # part one
        inp = [int(x) for x in line*10000]
        offset = int("".join(map(str, inp[:7])))
        print("".join(map(str, fft_repeat(inp, offset, 100)[offset:offset+8]))) # part two

