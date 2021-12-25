



def update(ocean_floor, width, height):
    updated_ocean_floor = dict()
    updated = False
    for (x,y), cucumber in ocean_floor.items():
        if cucumber == ">":
            new_x = (x+1) % width
            if (new_x, y) not in ocean_floor:
                updated = True
                updated_ocean_floor[new_x,y] = cucumber
            else:
                updated_ocean_floor[x,y] = cucumber

    for (x,y), cucumber in ocean_floor.items():
        if cucumber == "v":
            new_y = (y+1) % height
            # Can move if new spot not occupied by new ">" and not occupied by old "v"
            if (x, new_y) not in updated_ocean_floor and ((x,new_y) not in ocean_floor or ocean_floor[x,new_y] == ">"):
                updated = True
                updated_ocean_floor[x,new_y] = cucumber
            else:
                updated_ocean_floor[x,y] = cucumber

    return updated_ocean_floor, updated


def move_until_static(ocean_floor, width, height):

    step_nr = 0
    while True:
        step_nr += 1
        ocean_floor, updated = update(ocean_floor, width, height)
        if not updated:
            return step_nr

if __name__ == "__main__":
    ocean_floor = dict()
    width = None
    height = None
    with open("input", "r") as file:
        y = 0
        for line in file:
            width = len(line.strip())
            for x in range(len(line)):
                if line[x] in [">", "v"]:
                    ocean_floor[x,y] = line[x]
            y += 1
        height = y
    # p1
    print(move_until_static(ocean_floor, width, height))
