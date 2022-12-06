

def part_one(signal):
    for i in range(3, len(signal)):
        marker = signal[i-3:i+1]
        if any(marker.count(x) != 1 for x in marker):
            continue
        return i+1

def part_two(signal):
    for i in range(13, len(signal)):
        marker = signal[i-13:i+1]
        if any(marker.count(x) != 1 for x in marker):
            continue
        return i+1


if __name__ == "__main__":
    signal = ""
    with open("input", "r") as fd:
        signal = fd.readline().strip()

    print(part_one(signal))

    print(part_two(signal))