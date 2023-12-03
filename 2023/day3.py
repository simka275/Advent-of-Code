

def check_adjacent(x_start, x_end, y, lines):
    for yy in [y-1, y, y+1]:
        if yy < 0 or yy >= len(lines):
            continue
        for xx in range(x_start-1, x_end+1):
            if xx < 0 or xx >= len(lines[yy]):
                continue
            if not lines[yy][xx].isdigit() and not lines[yy][xx] == '.':
                return int(lines[y][x_start:x_end])
    return 0

def part_one(lines):
    res = 0
    for y in range(len(lines)):
        x = 0
        while x < len(lines[y]):
            if lines[y][x].isdigit():
                num_end = x+1
                while num_end < len(lines[y]) and lines[y][num_end].isdigit():
                    num_end+=1

                res += check_adjacent(x, num_end, y, lines)
                x = num_end-1
            x+=1
    return res


def check_adjacent_to_stars(x_start, x_end, y, lines):
    adjacent_stars = []
    for yy in [y-1, y, y+1]:
        if yy < 0 or yy >= len(lines):
            continue
        for xx in range(x_start-1, x_end+1):
            if xx < 0 or xx >= len(lines[yy]):
                continue
            if lines[yy][xx] == '*':
                adjacent_stars.append((xx,yy))
    return adjacent_stars

def part_two(lines):
    res = 0
    star_num_mapping = dict()
    for y in range(len(lines)):
        x = 0
        while x < len(lines[y]):
            if lines[y][x].isdigit():
                num_end = x+1
                while num_end < len(lines[y]) and lines[y][num_end].isdigit():
                    num_end+=1

                adjacent_stars = check_adjacent_to_stars(x, num_end, y, lines)
                for star in adjacent_stars:
                    if star in star_num_mapping:
                        star_num_mapping[star].append(int(lines[y][x:num_end]))
                    else:
                        star_num_mapping[star] = [int(lines[y][x:num_end])]

                x = num_end-1
            x+=1

    for star, num_list in star_num_mapping.items():
        if len(num_list) == 2:
            res += num_list[0] * num_list[1]

    return res


if __name__ == "__main__":
    lines = []
    with open("input", "r") as fd:
        lines = [x.strip() for x in fd]

    print(part_one(lines))

    print(part_two(lines))
