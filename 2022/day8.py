

def is_visible(x, y, forest):
    height = len(forest)
    width = len(forest[y])
    tree_len = forest[y][x]

    if all(l < tree_len for l in forest[y][:x]):
        return True

    if all(l < tree_len for l in forest[y][x+1:]):
        return True

    above_tree = []
    for yy in range(y):
        above_tree.append(forest[yy][x])
    if all(l < tree_len for l in above_tree):
        return True

    below_tree = []
    for yy in range(y+1, height):
        below_tree.append(forest[yy][x])
    if all(l < tree_len for l in below_tree):
        return True

    return False


def part_one(forest):
    visible_tree = 2*len(forest) + 2*len(forest[0]) -4
    for y in range(1, len(forest)-1):
        for x in range(1, len(forest[y])-1):
            if is_visible(x, y, forest):
                visible_tree += 1
    return visible_tree


def scenic_score(x, y, forest):
    res = 1
    tree_len = forest[y][x]
    visible_trees = 0
    for xx in range(x-1, -1, -1):
        if forest[y][xx] >= tree_len:
            visible_trees += 1
            break
        visible_trees += 1
    res *= visible_trees

    visible_trees = 0
    for xx in range(x+1, len(forest[y])):
        if forest[y][xx] >= tree_len:
            visible_trees += 1
            break
        visible_trees += 1
    res *= visible_trees

    visible_trees = 0
    for yy in range(y-1, -1, -1):
        if forest[yy][x] >= tree_len:
            visible_trees += 1
            break
        visible_trees += 1
    res *= visible_trees

    visible_trees = 0
    for yy in range(y+1, len(forest)):
        if forest[yy][x] >= tree_len:
            visible_trees += 1
            break
        visible_trees += 1
    res *= visible_trees

    return res


def part_two(forest):
    res = 0
    for y in range(len(forest)):
        for x in range(len(forest[y])):
            res = max(res, scenic_score(x, y, forest))
    return res


if __name__ == "__main__":
    forest = []
    width = None
    height = None
    with open("input", "r") as fd:
        for line in fd:
            forest.append([int(x) for x in line.strip()])


    print(part_one(forest))

    print(part_two(forest))