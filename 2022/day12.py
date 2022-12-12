
import heapq

def part_one(heightmap):
    start = None
    for y in range(len(heightmap)):
        for x in range(len(heightmap[y])):
            if heightmap[y][x] == "S":
                start = (x,y)
                break

    visited = set()
    queue = [(0, start[0], start[1], [])]
    heapq.heapify(queue)

    while queue:
        cost, x, y, path = heapq.heappop(queue)
        if (x,y) in visited:
            continue
        visited.add((x,y))
        current_height = heightmap[y][x]
        if current_height == "E":
            return cost

        for dx,dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            if not (0 <= x+dx < len(heightmap[y])) or not (0 <= y+dy < len(heightmap)):
                continue
            next_height = heightmap[y+dy][x+dx]
            if current_height not in ("y","z") and next_height == "E":
                continue
            if current_height == "S" and next_height == "a":
                heapq.heappush(queue, (cost+1, x+dx, y+dy, path + [(x+dx,y+dy)]))
            elif ord(next_height) <= ord(current_height)+1:
                heapq.heappush(queue, (cost+1, x+dx, y+dy, path + [(x+dx,y+dy)]))


def part_two(heightmap):
    starts = []
    for y in range(len(heightmap)):
        for x in range(len(heightmap[y])):
            if heightmap[y][x] in ("S","a"):
                starts.append((x,y))

    visited = set()
    queue = [(0, x, y, [(x,y)]) for x,y in starts]
    heapq.heapify(queue)

    while queue:
        cost, x, y, path = heapq.heappop(queue)
        if (x,y) in visited:
            continue
        visited.add((x,y))
        current_height = heightmap[y][x]
        if current_height == "E":
            return cost

        for dx,dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            if not (0 <= x+dx < len(heightmap[y])) or not (0 <= y+dy < len(heightmap)):
                continue
            next_height = heightmap[y+dy][x+dx]
            if current_height not in ("y","z") and next_height == "E":
                continue
            if current_height == "S" and next_height == "a":
                heapq.heappush(queue, (cost+1, x+dx, y+dy, path + [(x+dx,y+dy)]))
            elif ord(next_height) <= ord(current_height)+1:
                heapq.heappush(queue, (cost+1, x+dx, y+dy, path + [(x+dx,y+dy)]))


if __name__ == "__main__":
    heightmap = []
    with open("input", "r") as fd:
        for line in fd:
            heightmap.append([x for x in line.strip()])

    print(part_one(heightmap))

    print(part_two(heightmap))