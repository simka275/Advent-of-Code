

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(x={0}, y={1})".format(self.x, self.y)


class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    # Manhattan length
    def length(self):
        return abs(self.end.x - self.start.x) + abs(self.end.y - self.start.y)


def delta_dist(step):
    dx, dy = 0, 0
    if step[0] == "U":
        dy = int(step[1:])
    elif step[0] == "R":
        dx = int(step[1:])
    elif step[0] == "D":
        dy = -int(step[1:])
    elif step[0] == "L":
        dx = -int(step[1:])
    return dx, dy


def create_lines(path):
    lines = []
    x, y = 0, 0
    for step in path:
        dx, dy = delta_dist(step)
        lines.append(Line(Point(x, y), Point(x+dx, y+dy)))
        x += dx
        y += dy

    return lines


def find_intersection_horiz_vert(l1, l2):
    # l2 x within l1 bounds
    if min(l1.start.x, l1.end.x) <= l2.start.x and max(l1.start.x, l1.end.x) >= l2.start.x:
        # l1 y within l2 bound
        if min(l2.start.y, l2.end.y) <= l1.start.y and max(l2.start.y, l2.end.y) >= l1.start.y:
            return Point(l2.start.x, l1.start.y)


# currently ignores case where both horizontal or both vertical
def find_intersection(l1, l2):
    # 1 horiz 2 vert
    if l1.start.y == l1.end.y and l2.start.x == l2.end.x:
        return find_intersection_horiz_vert(l1, l2)
    # 1 vert 2 horiz
    if l2.start.y == l2.end.y and l1.start.x == l1.end.x:
        return find_intersection_horiz_vert(l2, l1)

    return None


def find_intersections(lines1, lines2):
    intersections = []
    for i in range(1,len(lines1)):
        for j in range(1,len(lines2)):
            p = find_intersection(lines1[i], lines2[j])
            if p:
                intersections.append(p)
    return intersections


def calc_manhattan_dist(p1, p2):
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)


def find_shortest_manhattan(points):
    res = None
    for p in points:
        d = calc_manhattan_dist(Point(0,0), p)
        if not res or res > d:
            res = d
    return res


def part_one():
    with open("input", "r") as file:
        lines1 = create_lines(file.readline().strip().split(","))
        lines2 = create_lines(file.readline().strip().split(","))
        intersections = find_intersections(lines1, lines2)
        print(find_shortest_manhattan(intersections))


def find_min_cost_intersect(lines1, lines2):
    # cheapest_intersection = None
    min_cost = None
    l1_cost = 0
    for i in range(len(lines1)):
        l1_cost += lines1[i].length()
        tot_cost = l1_cost
        for j in range(len(lines2)):
            tot_cost += lines2[j].length()
            p = find_intersection(lines1[i], lines2[j])
            if p and p.x != 0 and p.y != 0 and (not min_cost or min_cost > tot_cost):
                # Cost is total cost of lines then subtracting distance from intersection to end of line
                min_cost = tot_cost -calc_manhattan_dist(p, lines1[i].end) -calc_manhattan_dist(p, lines2[j].end)
                break

    return min_cost
    

def part_two():
    with open("input", "r") as file:
        lines1 = create_lines(file.readline().strip().split(","))
        lines2 = create_lines(file.readline().strip().split(","))
        print(find_min_cost_intersect(lines1, lines2))


if __name__ == "__main__":
    # part_one()
    part_two()