
import copy

def step_state(octopuses):
    for y in range(len(octopuses)):
        for x in range(len(octopuses[y])):
            octopuses[y][x] += 1


def update_flash(octopuses):
    flashes = 0
    flash_ready = []
    flash_done = []
    for y in range(len(octopuses)):
        for x in range(len(octopuses[y])):
            if octopuses[y][x] > 9:
                flash_ready.append((x,y))

    while flash_ready:
        x,y = flash_ready.pop()
        flashes += 1
        flash_done.append((x,y))
        octopuses[y][x] = 0
        for yy in range(y-1,y+2):
            for xx in range(x-1,x+2):
                if (xx,yy) in flash_done:
                    continue
                if yy == y and xx == x:
                    continue
                if yy < 0 or yy >= len(octopuses):
                    continue
                if xx < 0 or xx >= len(octopuses[yy]):
                    continue
                octopuses[yy][xx] += 1
                if octopuses[yy][xx] > 9 and (xx,yy) not in flash_ready:
                    flash_ready.append((xx,yy))
    return flashes

def calc_flashes(octopuses, steps):
    res = 0
    for i in range(steps):
        step_state(octopuses)
        res += update_flash(octopuses)
    return res


def calc_first_sync(octopuses):
    flash_goal = len(octopuses)*len(octopuses[0])
    step = 1
    while True:
        step_state(octopuses)
        flashes = update_flash(octopuses)
        if flashes == flash_goal:
            return step
        step += 1


if __name__ == "__main__":
    octopuses = []
    with open("input", "r") as file:
        for line in file:
            row = [int(x) for x in line.strip()]
            octopuses.append(row)

    # p1
    print(calc_flashes(copy.deepcopy(octopuses), 100))

    # p2
    print(calc_first_sync(octopuses))