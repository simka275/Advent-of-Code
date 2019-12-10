
import math
from queue import PriorityQueue


def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b, a%b)


def calc_angle(x,y):
    alpha = None
    if x > 0 and y > 0:
        alpha = math.atan(y/x)
    elif x < 0 and y > 0:
        alpha = math.pi - math.atan(abs(y/x))
    elif x < 0 and y < 0:
        alpha = math.pi + math.atan(y/x)
    elif x > 0 and y < 0:
        alpha = -1*math.atan(abs(y/x))
    elif x == 0:
        alpha = math.pi/2 if y > 0 else -1*math.pi/2
    elif y == 0:
        alpha = 0 if x > 0 else math.pi

    return alpha


def get_asteroid_vectors(space, x, y):
    res = []
    for yy in range(len(space)):
        for xx in range(len(space[yy])):
            if yy == y and xx == x:
                continue
            elif space[yy][xx] == "#":
                dy = yy-y
                dx = xx-x
                g = gcd(abs(dx),abs(dy))

                v = (int(dx//g), int(dy/g))
                if v not in res:
                    res.append(v)
    return res


def find_opt_los(space):
    # res = copy.deepcopy(space)
    max_count, max_x, max_y = -1, None, None
    for y in range(len(space)):
        for x in range(len(space[y])):
            if space[y][x] == "#":
                # res[y][x] = count_los_asteroids(space, x, y)
                curr = len(get_asteroid_vectors(space, x ,y))
                if max_count < curr:
                    max_count = curr
                    max_x, max_y = x, y
    # return res
    return max_count, max_x, max_y


def destroy_asteroids(space, x, y):
    destroyed = 0
    # One sweep per loop
    while destroyed < 200:
        av = get_asteroid_vectors(space, x, y)
        if not av:
            raise Exception("To few asteroids")
        queue = PriorityQueue()
        for v in av:
            alpha = calc_angle(v[0], v[1])

            queue.put((alpha, v[0], v[1]))
        while not queue.empty():
            alpha, dx, dy = queue.get()
            xx, yy = x+dx, y+dy
            while 0 <= yy < len(space) and 0 <= xx < len(space[yy]):
                if space[yy][xx] == "#":
                    # print(str(destroyed+1) + ":",xx, yy)
                    space[yy][xx] = str(destroyed+1)
                    break
                else:
                    xx += dx
                    yy += dy
            destroyed += 1
            if destroyed == 200:
                return xx, yy
        



if __name__ == "__main__":
    space = []
    with open("input", "r") as file:
        for line in file:
            space.append([ x for x in line.strip() ])
    # print_space(space)
    asteroids, x, y = find_opt_los(space)
    print(asteroids, x, y)
    # print(get_asteroid_vectors(space, x, y))
    print(destroy_asteroids(space, x, y))


        