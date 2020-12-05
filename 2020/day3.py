
def count_trees(terrain, dx, dy):
    x, y, trees = 0, 0, 0
    while(y < len(terrain)):
        if terrain[y][x] == "#":
            trees += 1
        y += dy
        x = (x + dx) % len(terrain[y % len(terrain)])
    return trees



if __name__ == "__main__":
    terrain = []
    with open("input", "r") as file:
        for line in file:
            terrain.append([x for x in line.rstrip()])

    # Part 1
    print(count_trees(terrain, 3, 1))

    # Part 2
    print(count_trees(terrain, 1, 1) * count_trees(terrain, 3, 1) * count_trees(terrain, 5, 1) * count_trees(terrain, 7, 1) * count_trees(terrain, 1, 2))

