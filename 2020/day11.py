
def print_layout(layout):
    for row in layout:
        for col in row:
            print(col, end="")
        print()
    print()



def count_adjacent_occupied(layout, x, y):
    res = 0
    for yy in range(y-1,y+2):
        if yy < 0 or yy >= len(layout):
            continue
        for xx in range(x-1,x+2):
            if xx < 0 or xx >= len(layout[yy]):
                continue
            if xx == x and yy == y:
                continue
            if layout[yy][xx] == "#":
                res += 1
    return res


def count_visible_occupied(layout, x, y):
    res = 0
    for dy in [-1,0,1]:
        for dx in [-1,0,1]:
            if dy == 0 and dx == 0:
                continue
            xx = x
            yy = y
            while True:
                xx += dx
                yy += dy
                if yy < 0 or yy >= len(layout) or xx < 0 or xx >= len(layout[yy]) or layout[yy][xx] == "L":
                    break
                if layout[yy][xx] == "#":
                    res += 1
                    break
    return res




def step_p1(layout):
    new_layout = []
    for y in range(len(layout)):
        new_row = []
        for x in range(len(layout[y])):
            occu = count_adjacent_occupied(layout, x, y)
            if layout[y][x] == "L" and occu == 0:
                new_row.append("#")
            elif layout[y][x] == "#" and occu >= 4:
                new_row.append("L")
            else:
                new_row.append(layout[y][x])
        new_layout.append(new_row)
    return new_layout

def step_p2(layout):
    new_layout = []
    for y in range(len(layout)):
        new_row = []
        for x in range(len(layout[y])):
            occu = count_visible_occupied(layout, x, y)
            if layout[y][x] == "L" and occu == 0:
                new_row.append("#")
            elif layout[y][x] == "#" and occu >= 5:
                new_row.append("L")
            else:
                new_row.append(layout[y][x])
        new_layout.append(new_row)
    return new_layout


def run_until_stabile_p1(layout):
    tot_occu = 0
    while True:
        old_layout = layout
        layout = step_p1(layout)
        if old_layout == layout:
            break
    for row in layout:
        for col in row:
            if col == "#":
                tot_occu += 1
    return tot_occu


def run_until_stabile_p2(layout):
    tot_occu = 0
    while True:
        old_layout = layout
        layout = step_p2(layout)
        if old_layout == layout:
            break
    for row in layout:
        for col in row:
            if col == "#":
                tot_occu += 1
    return tot_occu


if __name__ == "__main__":
    layout = []
    with open("input", "r") as file:
        for line in file:
            layout.append([x for x in line.rstrip()])

    # part 1
    print(run_until_stabile_p1(layout))
    # part 2
    print(run_until_stabile_p2(layout))