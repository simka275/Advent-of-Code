

def fold_paper(points, operations):
    for op in operations:
        _, _, line = op.split()
        axis,value = line.split("=")
        value = int(value)
        new_points = set()
        for x,y in points:
            if axis == "x":
                xx = x if x <= value else 2*value - x
                new_points.add((xx,y))
            elif axis == "y":
                yy = y if y <= value else 2*value - y
                new_points.add((x,yy))
        points = new_points

        # p1
        # return len(points)
    print_points(points)
    return len(points)


def print_points(points):
    x_max, y_max = 0,0
    for x,y in points:
        x_max = max(x,x_max)
        y_max = max(y,y_max)

    for y in range(y_max+1):
        for x in range(x_max+1):
            if (x,y) in points:
                print("#", end="")
            else:
                print(".", end="")
        print()


if __name__ == "__main__":
    points = set()
    operations = []
    with open("input", "r") as file:
        reading_points = True
        for line in file:
            if line == "\n":
                reading_points = False
                continue
            if reading_points:
                x,y = line.strip().split(",")
                points.add((int(x),int(y)))
            else:
                operations.append(line.strip())

    print(fold_paper(points, operations))
