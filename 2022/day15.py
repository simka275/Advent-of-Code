
import re
import time

def part_one(zones, beacons, target_row):
    emtpy_positions = set()
    for x,y,r in zones:
        dy = abs(y-target_row)
        if dy <= r:
            for dx in range(-abs(r-dy), abs(r-dy)+1):
                if (x-dx, target_row) not in beacons:
                    emtpy_positions.add((x-dx, target_row))
    return len(emtpy_positions)


def within_range(x,y,zones):
    for sx,sy,r in zones:
        d = abs(x-sx) + abs(y-sy)
        if d <= r:
            return True
    return False


def part_two(zones, beacons):
    for sx, sy, r in zones:
        for dx in range(r+2): # Check positions 1 step outside sensor range
            dy = (r+1) - dx
            for rotation_x, rotation_y in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                x = sx + dx * rotation_x
                y = sy + dy * rotation_y
                if x < 0 or x > 4000000 or y < 0 or y > 4000000:
                    continue
                # if x < 0 or x > 20 or y < 0 or y > 20:
                #     continue
                if not within_range(x,y,zones) and (x,y) not in beacons:
                    return 4000000 * x + y



if __name__ == "__main__":
    zones = []
    beacons = set()
    with open("input", "r") as fd:
        for line in fd:
            match = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
            if match:
                sx, sy, bx, by = [int(x) for x in match.groups()]
                zones.append((sx, sy, abs(sx-bx) + abs(sy-by)))
                beacons.add((bx,by))

    start_time = time.time()
    print(part_one(zones, beacons, 2000000))
    end_time = time.time()
    print("Took {} seconds".format(end_time-start_time))

    start_time = time.time()
    print(part_two(zones, beacons))
    end_time = time.time()
    print("Took {} seconds".format(end_time-start_time))