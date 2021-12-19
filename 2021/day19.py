

import math

def rotate_around_x_axis(coords):
    x,y,z = coords
    return (x,-z,y)

def rotate_around_y_axis(coords):
    x,y,z = coords
    return (-z,y,x)

def rotate_around_z_axis(coords):
    x,y,z = coords
    return (-y,x,z)


# def generate_orientations(beacons):
#     res = [beacons]

#     # 2d orientations
#     current_beacons = beacons
#     for _ in range(3):
#         rotated_beacons = []
#         for beacon in current_beacons:
#             rotated_beacons.append(rotate_around_z_axis(beacon))
#         res.append(rotated_beacons)
#         current_beacons = rotated_beacons

#     # For each 2d orientation rotate it around x and y axis
#     # Account for: 2 rotations around axis A == 2 rotations around B followed by 2 rotations around C
#     orientations = res.copy()
#     for i in range(len(orientations)):
#         current_beacons = orientations[i]
#         for j in range(3):
#             if i == 2 and j == 1: continue # 0Z + 2Y == 2Z + 2X
#             if i == 3 and j == 1: continue # 1Z + 2Y == 3Z + 2X
#             rotated_beacons = []
#             for beacon in current_beacons:
#                 rotated_beacons.append(rotate_around_x_axis(beacon))
#             res.append(rotated_beacons)
#             current_beacons = rotated_beacons

#         for j in range(3):
#             if i == 2 and j == 1: continue # 0Z + 2X == 2Z + 2Y
#             if i == 3 and j == 1: continue # 1Z + 2X == 3Z + 2Y
#             rotated_beacons = []
#             for beacon in current_beacons:
#                 rotated_beacons.append(rotate_around_y_axis(beacon))
#             res.append(rotated_beacons)
#             current_beacons = rotated_beacons
#     return res


# This one generates duplicates but gives correct results...
def generate_orientations(beacons):
    res = [beacons]
    current_beacons = beacons
    for _ in range(3):
        rotated_beacons = []
        for beacon in current_beacons:
            rotated_beacons.append(rotate_around_z_axis(beacon))
        res.append(rotated_beacons)
        current_beacons = rotated_beacons

    for current_beacons in res.copy():
        for _ in range(3):
            rotated_beacons = []
            for beacon in current_beacons:
                rotated_beacons.append(rotate_around_x_axis(beacon))
            res.append(rotated_beacons)
            current_beacons = rotated_beacons

    for current_beacons in res.copy():
        for _ in range(3):
            rotated_beacons = []
            for beacon in current_beacons:
                rotated_beacons.append(rotate_around_y_axis(beacon))
            res.append(rotated_beacons)
            current_beacons = rotated_beacons
    return res


def match_beacons(reference, other):
    orientations = generate_orientations(other)
    for orientation in orientations:
        deltas = {}
        for ref_beacon in reference:
            for other_beacon in orientation:
                delta = (other_beacon[0] - ref_beacon[0], other_beacon[1] - ref_beacon[1], other_beacon[2] - ref_beacon[2])
                if delta not in deltas:
                    deltas[delta] = 0
                deltas[delta] += 1
                if deltas[delta] >= 12:
                    for i in range(len(orientation)):
                        orientation[i] = (orientation[i][0] - delta[0], orientation[i][1] - delta[1], orientation[i][2] - delta[2])
                    return True, delta, orientation
    return False, None, None


def lock_scanners(scanners):
    locked_scanners = [scanners[0]]
    scanner_positions = [(0,0,0)]
    scanner_queue = scanners[1:]
    while scanner_queue:
        scanner = scanner_queue.pop(0)
        found_match = False
        for locked_scanner in locked_scanners:
            found_match, scanner_pos, new_locked_scanner = match_beacons(locked_scanner, scanner)
            if found_match:
                scanner_positions.append(scanner_pos)
                locked_scanners.append(new_locked_scanner)
                break
        if not found_match:
            scanner_queue.append(scanner)
    return locked_scanners, scanner_positions


def count_beacons(scanners):
    beacons = set()
    for scanner in scanners:
        for beacon in scanner:
            beacons.add(beacon)
    return len(beacons)


def greatest_scanner_distance(scanner_positions):
    max_distance = -math.inf
    for p1 in scanner_positions:
        for p2 in scanner_positions:
            max_distance = max(max_distance, abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2]))
    return max_distance


if __name__ == "__main__":
    scanners = []
    with open("input", "r") as file:
        beacons = []
        for line in file:
            if line.find("---") != -1: continue
            if line == "\n":
                scanners.append(beacons)
                beacons = []
            else:
                x,y,z = line.strip().split(",")
                beacons.append((int(x),int(y),int(z)))
        if beacons: scanners.append(beacons)

    # p1
    locked_scanners, scanner_positions = lock_scanners(scanners)
    print(count_beacons(locked_scanners))

    # p2
    print(greatest_scanner_distance(scanner_positions))
