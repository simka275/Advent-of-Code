

def combine_cubes(cubes_to_add):
    cubes = cubes_to_add[:1]
    for (add_x1,add_x2,add_y1,add_y2,add_z1,add_z2,add_is_on) in cubes_to_add[1:]:
        new_cubes = []
        for (prev_x1,prev_x2,prev_y1,prev_y2,prev_z1,prev_z2,prev_is_on) in cubes:
            intersection_x1 = max(add_x1,prev_x1)
            intersection_x2 = min(add_x2,prev_x2)
            intersection_y1 = max(add_y1,prev_y1)
            intersection_y2 = min(add_y2,prev_y2)
            intersection_z1 = max(add_z1,prev_z1)
            intersection_z2 = min(add_z2,prev_z2)

            new_cubes.append((prev_x1,prev_x2,prev_y1,prev_y2,prev_z1,prev_z2,prev_is_on))
            if intersection_x2-intersection_x1 < 0: continue
            if intersection_y2-intersection_y1 < 0: continue
            if intersection_z2-intersection_z1 < 0: continue
            new_cubes.append((intersection_x1,intersection_x2,intersection_y1,intersection_y2,intersection_z1,intersection_z2, not prev_is_on))

        if add_is_on:
            new_cubes.append((add_x1,add_x2,add_y1,add_y2,add_z1,add_z2,add_is_on))
        cubes = new_cubes

    return cubes

def calc_on_cubes_init_proc(cubes):
    min_pos = -50
    max_pos = 50
    res = 0
    for (x1,x2,y1,y2,z1,z2,is_on) in cubes:
        if x1 > max_pos: continue
        if x2 < min_pos: continue
        if y1 > max_pos: continue
        if y2 < min_pos: continue
        if z1 > max_pos: continue
        if z2 < min_pos: continue
        volume = (x2-x1+1)*(y2-y1+1)*(z2-z1+1)
        if is_on:
            res += volume
        else:
            res -= volume
    return res


def calc_on_cubes(cubes):
    res = 0
    for (x1,x2,y1,y2,z1,z2,is_on) in cubes:
        volume = (x2-x1+1)*(y2-y1+1)*(z2-z1+1)
        if is_on:
            res += volume
        else:
            res -= volume
    return res


if __name__ == "__main__":
    cubes = []
    with open("input", "r") as file:
        for line in file:
            if "on" in line:
                x,y,z = line[3:].strip().split(",")
                x1,x2 = [int(e) for e in x[2:].split("..")]
                y1,y2 = [int(e) for e in y[2:].split("..")]
                z1,z2 = [int(e) for e in z[2:].split("..")]
                cubes.append((x1,x2,y1,y2,z1,z2,True))
            elif "off" in line:
                x,y,z = line[4:].strip().split(",")
                x1,x2 = [int(e) for e in x[2:].split("..")]
                y1,y2 = [int(e) for e in y[2:].split("..")]
                z1,z2 = [int(e) for e in z[2:].split("..")]
                cubes.append((x1,x2,y1,y2,z1,z2,False))


    cubes = combine_cubes(cubes)
    # p1
    print(calc_on_cubes_init_proc(cubes))

    # p2
    print(calc_on_cubes(cubes))