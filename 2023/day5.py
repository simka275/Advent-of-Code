
import copy

def part_one(lines):
    _, seeds = lines.pop(0).split(": ")
    seeds = [int(x) for x in seeds.split()]
    lines.pop(0)
    mappings = []
    current_mapping = None
    for line in lines:
        if line == "":
            continue
        elif "map" in line:
            if current_mapping:
                mappings.append(current_mapping)
            current_mapping = []
        else:
            current_mapping.append([int(x) for x in line.split()])
    if current_mapping:
        mappings.append(current_mapping)

    candidate = float("inf")
    for seed in seeds:
        current = seed
        for mapping in mappings:
            for interval in mapping:
                next_location_start = interval[0]
                start = interval[1]
                steps = interval[2]
                if start <= current < start + steps:
                    delta = current - start
                    current = next_location_start + delta
                    break
        if current < candidate:
            candidate = current

    return candidate

def part_two(lines):
    _, seeds = lines.pop(0).split(": ")
    seeds = [int(x) for x in seeds.split()]
    lines.pop(0)
    mappings = []
    current_mapping = None
    for line in lines:
        if line == "":
            continue
        elif "map" in line:
            if current_mapping:
                mappings.append(current_mapping)
            current_mapping = []
        else:
            current_mapping.append([int(x) for x in line.split()])
    if current_mapping:
        mappings.append(current_mapping)


    current_start_and_ranges = []
    for i in range(0, len(seeds), 2):
        current_start_and_ranges.append([seeds[i], seeds[i+1]])

    while mappings:
        mapping = mappings.pop(0)

        next_start_and_ranges = []
        while current_start_and_ranges:
            updated = False
            current_start, current_range = current_start_and_ranges.pop(0)
            current_end = current_start + current_range

            for interval in mapping:
                next_start = interval[0]
                mapping_start = interval[1]
                mapping_range = interval[2]
                mapping_end = mapping_start + mapping_range

                if current_start < mapping_start: # Current interval starts outside mapping interval
                    if current_end <= mapping_start: #2 Current interval end before mapping interval
                        continue
                    elif current_end <= mapping_end: #1 Current interval end inside mapping interval
                        next_start_and_ranges.append([next_start, current_end - mapping_start])
                        current_start_and_ranges.append([current_start, mapping_start - current_start])
                        updated = True
                    elif current_end > mapping_end: #3 Current interval end after mapping interval
                        next_start_and_ranges.append([next_start, mapping_range])
                        current_start_and_ranges.append([current_start, mapping_start - current_start])
                        current_start_and_ranges.append([mapping_end, current_end - mapping_end])
                        updated = True
                elif current_start == mapping_end: # Current interval starts where mapping interval ends
                    continue
                elif current_start < mapping_end: # Current interval starts inside mapping interval
                    if current_end <= mapping_end: #4 Current interval end inside mapping interval
                        next_start_and_ranges.append([next_start + (current_start - mapping_start) , current_range])
                        updated = True
                    elif current_end > mapping_end: #5 Current interval ends after mapping interval
                        next_start_and_ranges.append([next_start + (current_start - mapping_start), mapping_end - current_start])
                        current_start_and_ranges.append([mapping_end, current_end - mapping_end])
                        updated = True
                    elif current_start > current_end:
                        continue

            if not updated:
                next_start_and_ranges.append([current_start, current_range])

        current_start_and_ranges = next_start_and_ranges

    res = float("inf")
    for start,_ in current_start_and_ranges:
        res = min(res, start)
    return res


if __name__ == "__main__":
    lines = []
    with open("input", "r") as fd:
        lines = [x.strip() for x in fd]

    print(part_one(copy.deepcopy(lines)))

    print(part_two(lines))
