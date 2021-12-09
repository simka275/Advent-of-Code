

import math

def calc_risk(height_map):
    res = 0
    low_points = []
    for y in range(len(height_map)):
        for x in range(len(height_map[y])):
            height = height_map[y][x]
            north = height_map[y-1][x] if y-1 >= 0 else math.inf
            east = height_map[y][x+1] if x+1 < len(height_map[y]) else math.inf
            south = height_map[y+1][x] if y+1 < len(height_map) else math.inf
            west = height_map[y][x-1] if x-1 >= 0 else math.inf
            if height < north and height < east and height < south and height < west:
                res += 1 + height
                low_points.append((x,y))
    return res, low_points


def calc_basin_rating(height_map):
    basin_sizes = []
    _, low_points = calc_risk(height_map)
    for lp in low_points:
        queue = [(lp[0],lp[1])]
        visited = {(lp[0],lp[1])}
        basin_size = 1
        while queue:
            p = queue.pop()
            x,y = p[0],p[1]
            north = height_map[y-1][x] if y-1 >= 0 else math.inf
            if north < 9 and (x,y-1) not in visited:
                queue.append((x,y-1))
                visited.add((x,y-1))
                basin_size += 1
            east = height_map[y][x+1] if x+1 < len(height_map[y]) else math.inf
            if east < 9 and (x+1,y) not in visited:
                queue.append((x+1,y))
                visited.add((x+1,y))
                basin_size += 1
            south = height_map[y+1][x] if y+1 < len(height_map) else math.inf
            if south < 9 and (x,y+1) not in visited:
                queue.append((x,y+1))
                visited.add((x,y+1))
                basin_size += 1
            west = height_map[y][x-1] if x-1 >= 0 else math.inf
            if west < 9 and (x-1,y) not in visited:
                queue.append((x-1,y))
                visited.add((x-1,y))
                basin_size += 1
        basin_sizes.append(basin_size)
    basin_sizes = sorted(basin_sizes)
    return basin_sizes[-1]*basin_sizes[-2]*basin_sizes[-3]


if __name__ == "__main__":
    height_map = []
    with open("input", "r") as file:
        for line in file:
            line = line.strip()
            row = []
            for n in line:
                row.append(int(n))
            height_map.append(row)

    # p1
    print(calc_risk(height_map)[0])

    # p2
    print(calc_basin_rating(height_map))
