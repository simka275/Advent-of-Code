
def valid_pos_3d(space, coord):
    x,y,z = coord
    # z
    if z < 0 or z >= len(space):
        return False
    # y
    if y < 0 or y >= len(space[z]):
        return False
    # x
    if x < 0 or x >= len(space[z][y]):
        return False
    return True


def count_active_neighbors_3d(space, coord):
    res = 0
    x,y,z = coord
    for dz in[-1,0,1]:
        for dy in[-1,0,1]:
            for dx in[-1,0,1]:
                xx,yy,zz = x+dx,y+dy,z+dz
                if (xx,yy,zz) == (x,y,z) or not valid_pos_3d(space, (xx,yy,zz)):
                    continue
                elif space[zz][yy][xx] == "#":
                    res += 1
    return res


def tick_3d(space):
    new_space = []
    new_z_range = len(space)+2
    new_y_range = len(space[0])+2
    new_x_range = len(space[0][0])+2
    for z in range(new_z_range):
        depth = []
        for y in range(new_y_range):
            row = []
            for x in range(new_x_range):
                xx,yy,zz = x-1,y-1,z-1
                active_neighbors = count_active_neighbors_3d(space, (xx,yy,zz))
                if valid_pos_3d(space, (xx,yy,zz)) and space[zz][yy][xx] == "#" and active_neighbors == 2:
                    row.append("#")
                elif active_neighbors == 3:
                    row.append("#")
                else:
                    row.append(".")
            depth.append(row)
        new_space.append(depth)
    return new_space


def elapse_3d(space, ticks):
    res = 0
    # print("Befory any cycles:\n")
    # print_space(space)
    for i in range(ticks):
        space = tick_3d(space)
        # print("After {} cycle:\n".format(i+1))
        # print_space(space)

    for z in range(len(space)):
        for y in range(len(space[z])):
            for x in range(len(space[z][y])):
                if space[z][y][x] == "#":
                    res += 1
    return res



def valid_pos_4d(space, coord):
    x,y,z,w = coord
    # w
    if w < 0 or w >= len(space):
        return False
    # z
    if z < 0 or z >= len(space[w]):
        return False
    # y
    if y < 0 or y >= len(space[w][z]):
        return False
    # x
    if x < 0 or x >= len(space[w][z][y]):
        return False
    return True


def count_active_neighbors_4d(space, coord):
    res = 0
    x,y,z,w = coord
    for dw in [-1,0,1]:
        for dz in [-1,0,1]:
            for dy in [-1,0,1]:
                for dx in [-1,0,1]:
                    xx,yy,zz,ww = x+dx,y+dy,z+dz,w+dw
                    if (xx,yy,zz,ww) == (x,y,z,w) or not valid_pos_4d(space, (xx,yy,zz,ww)):
                        continue
                    elif space[ww][zz][yy][xx] == "#":
                        res += 1
    return res


def tick_4d(space):
    new_space = []
    new_w_range = len(space)+2
    new_z_range = len(space[0])+2
    new_y_range = len(space[0][0])+2
    new_x_range = len(space[0][0][0])+2
    for w in range(new_w_range):
        glorf = [] # well known name of the 4th dimension
        for z in range(new_z_range):
            depth = []
            for y in range(new_y_range):
                row = []
                for x in range(new_x_range):
                    xx,yy,zz,ww = x-1,y-1,z-1,w-1
                    active_neighbors = count_active_neighbors_4d(space, (xx,yy,zz,ww))
                    if valid_pos_4d(space, (xx,yy,zz,ww)) and space[ww][zz][yy][xx] == "#" and active_neighbors == 2:
                        row.append("#")
                    elif active_neighbors == 3:
                        row.append("#")
                    else:
                        row.append(".")
                depth.append(row)
            glorf.append(depth)
        new_space.append(glorf)
    return new_space


def elapse_4d(space, ticks):
    res = 0
    for _ in range(ticks):
        space = tick_4d(space)

    for w in range(len(space)):
        for z in range(len(space[w])):
            for y in range(len(space[w][z])):
                for x in range(len(space[w][z][y])):
                    if space[w][z][y][x] == "#":
                        res += 1
    return res


# def print_space(space):
#     for z in range(len(space)):
#         print("z={}".format(z))
#         for y in range(len(space[z])):
#             for x in range(len(space[z][y])):
#                 print(space[z][y][x], end="")
#             print()
#         print()
#     print()


if __name__ == "__main__":
    space = []
    with open("input", "r") as file:
        depth = []
        for line in file:
            line = line.rstrip()
            row = []
            for c in line:
                row.append(c)
            depth.append(row)
        space.append(depth)

    # part 1
    print(elapse_3d(space.copy(),6))
    # part 2
    print(elapse_4d(space.copy(), 6))
