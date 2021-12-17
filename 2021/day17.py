
import math

def find_max_y_initial_velocity(target_area):
    target_x_min, target_x_max = target_area[0], target_area[1]
    target_y_min, target_y_max = target_area[2], target_area[3]

    valid_vxs = {}
    init_vx = 1
    while init_vx <= target_x_max:
        x = 0
        vx = init_vx
        steps = 0
        while x <= target_x_max and vx > 0:
            x += vx
            vx -= 1
            steps += 1
            if target_x_min <= x <= target_x_max:
                if steps in valid_vxs:
                    valid_vxs[steps].append(init_vx)
                else:
                    valid_vxs[steps] = [init_vx]
        init_vx += 1

    valid_init_vs = set()
    for steps, init_vxs in valid_vxs.items():
        # symmetric trajectory so if init vy is v then when back at y=0 vy equals -v
        # if at y=0 and vy < target_y_min then the probe will jump past it
        # therefore largest init vy is |target_y_min|
        for init_vy in range(abs(target_y_min), target_y_min-1, -1):
            for init_vx in init_vxs:
                x,y = 0,0
                vx = init_vx
                vy = init_vy
                step = 0
                while  x <= target_x_max and y >= target_y_min:
                    x += vx
                    y += vy
                    if vx > 0:
                        vx -= 1
                    vy -= 1
                    step += 1
                    if (target_x_min <= x <= target_x_max) and (target_y_min <= y <= target_y_max):
                        valid_init_vs.add((init_vx, init_vy))

    max_vys = -math.inf
    for init_v in valid_init_vs:
        max_vys = max(max_vys, init_v[1])
    max_height = (max_vys+1)*max_vys/2

    return max_height, len(valid_init_vs)


if __name__ == "__main__":
    target_area = []
    with open("input", "r") as file:
        for line in file:
            _, _, xrange, yrange = line.strip().split()
            xrange = [int(x) for x in xrange[2:-1].split("..")]
            yrange = [int(y) for y in yrange[2:].split("..")]
            target_area = xrange + yrange

    max_height, valid_init_vs = find_max_y_initial_velocity(target_area)
    # p1
    print(max_height)

    # p2
    print(valid_init_vs)
