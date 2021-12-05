
def get_points(line):
    points = []
    current_x, current_y = line[0][0],line[0][1]
    end_x, end_y = line[1][0],line[1][1]
    if current_x != end_x and current_y != end_y: # only horizontal or vertical lines
        return []
    while current_x != end_x or current_y != end_y:
        points.append((current_x,current_y))
        if current_x < end_x:
            current_x += 1
        elif current_x > end_x:
            current_x -= 1
        elif current_y < end_y:
            current_y += 1
        elif current_y > end_y:
            current_y -= 1
    points.append((end_x,end_y))
    return points


def calc_intersects(lines):
    res = 0
    intersects = dict()
    points = []
    for line in lines:
        points += get_points(line)
    for point in points:
        if point in intersects:
            intersects[point] += 1
        else:
            intersects[point] = 0
    for _, value in intersects.items():
        if value > 0:
            res += 1
    return res


def get_points_w_diag(line):
    points = []
    current_x, current_y = line[0][0],line[0][1]
    end_x, end_y = line[1][0],line[1][1]
    if current_x == end_x or current_y == end_y:
        return get_points(line)
    while current_x != end_x and current_y != end_y:
        points.append((current_x,current_y))
        if current_x < end_x and current_y < end_y: # SE
            current_x += 1
            current_y += 1
        elif current_x < end_x and current_y > end_y: # NE
            current_x += 1
            current_y -= 1
        elif current_x > end_x and current_y < end_y: # SW
            current_x -= 1
            current_y += 1
        elif current_x > end_x and current_y > end_y: # NW
            current_x -= 1
            current_y -= 1
    points.append((end_x,end_y))
    return points


def calc_intersects_w_diag(lines):
    res = 0
    intersects = dict()
    points = []
    for line in lines:
        points += get_points_w_diag(line)
    for point in points:
        if point in intersects:
            intersects[point] += 1
        else:
            intersects[point] = 0
    for _, value in intersects.items():
        if value > 0:
            res += 1
    return res


if __name__ == "__main__":
    lines = []
    with open("input", "r") as file:
        for line in file:
            pos1, pos2 = line.split(" -> ")
            pos1 = [int(x) for x in pos1.split(",")]
            pos1 = (pos1[0],pos1[1])
            pos2 = [int(x) for x in pos2.split(",")]
            pos2 = (pos2[0],pos2[1])
            lines.append([pos1,pos2])

    # p1
    print(calc_intersects(lines))

    # p2
    print(calc_intersects_w_diag(lines))