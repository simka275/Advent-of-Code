
def part_one(lines):
    sand = set()
    rocks = set()
    lowest_point = -1
    for line in lines:
        x1,y1 = line[0]
        x2,y2 = line[1]
        lowest_point = max(lowest_point,max(y1,y2))
        if x1 == x1:
            [rocks.add((x1,y)) for y in range(min(y1,y2), max(y1,y2)+1)]
        if y1 == y2:
            [rocks.add((x,y1)) for x in range(min(x1,x2), max(x1,x2)+1)]

    while True:
        x,y = (500,0)
        pre_len = len(sand)
        while y < lowest_point:
            new_x, new_y = x, y+1
            # below is occupied
            if (new_x,new_y) in rocks or (new_x,new_y) in sand:
                new_x = x-1
            else:
                x,y = new_x, new_y
                continue
            # downleft is occupied
            if (new_x,new_y) in rocks or (new_x, new_y) in sand:
                new_x = x+1
            else:
                x,y = new_x, new_y
                continue
            # downright is occupied
            if (new_x,new_y) in rocks or (new_x, new_y) in sand:
                sand.add((x,y))
                break
            else:
                x,y = new_x, new_y
                continue
        if pre_len == len(sand):
            return len(sand)


def part_two(lines):
    sand = set()
    rocks = set()
    lowest_point = -1
    for line in lines:
        x1,y1 = line[0]
        x2,y2 = line[1]
        lowest_point = max(lowest_point,max(y1,y2))
        if x1 == x1:
            [rocks.add((x1,y)) for y in range(min(y1,y2), max(y1,y2)+1)]
        if y1 == y2:
            [rocks.add((x,y1)) for x in range(min(x1,x2), max(x1,x2)+1)]
    floor_y = lowest_point + 2

    while True:
        x,y = (500,0)
        pre_len = len(sand)
        while y < floor_y:
            # print(x,y)
            new_x, new_y = x, y+1
            if new_y == floor_y:
                sand.add((x,y))
                break
            # below is occupied
            if (new_x,new_y) in rocks or (new_x,new_y) in sand:
                new_x = x-1
            else:
                x,y = new_x, new_y
                continue
            # downleft is occupied
            if (new_x,new_y) in rocks or (new_x, new_y) in sand:
                new_x = x+1
            else:
                x,y = new_x, new_y
                continue
            # downright is occupied
            if (new_x,new_y) in rocks or (new_x, new_y) in sand:
                sand.add((x,y))
                break
            else:
                x,y = new_x, new_y
                continue
        if pre_len == len(sand):
            return len(sand)

if __name__ == "__main__":
    lines = []
    with open("input", "r") as fd:
        for line in fd:
            points = [(int(x), int(y)) for x,y in [p.split(",") for p in line.strip().split(" -> ")]]
            for i in range(1, len(points)):
                lines.append((points[i-1], points[i]))

    print(part_one(lines))

    print(part_two(lines))