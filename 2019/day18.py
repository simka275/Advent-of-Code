
import math
import time
import queue

def find_items(grid):
    start_pos, keys, keys_pos, doors = [], set(), dict(), dict()
    # start_x, start_y, keys, doors = None, None, set(), set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "@":
                start_pos.append((x,y))
                # start_x, start_y = x, y
            elif grid[y][x].isalpha() and grid[y][x].islower():
                keys.add(grid[y][x])
                keys_pos[grid[y][x]] = (x,y)
                # keys.add(grid[y][x])
            elif grid[y][x].isalpha() and grid[y][x].isupper():
                doors[grid[y][x]] = (x,y)
                # doors.add(grid[y][x])
    return start_pos, keys, keys_pos, doors



def find_keys(sx,sy, grid):
    keys = dict()
    visited = set()
    q = queue.PriorityQueue()
    q.put((0,sx,sy,set()))
    while not q.empty():
        dist,x,y,req_keys = q.get()

        if grid[y][x] == "#" or (x,y) in visited:
            continue

        visited.add((x,y))

        if grid[y][x].isalpha() and grid[y][x].isupper():
            req_keys.add(grid[y][x].lower())
        
        if grid[y][x].isalpha() and grid[y][x].islower() and grid[y][x] != grid[sy][sx]:
            keys[grid[y][x]] = (dist, frozenset(req_keys))
            continue

        # n
        dist += 1
        if 0 < y: 
            q.put((dist, x, y-1, req_keys.copy()))
        # e
        if x < len(grid[y])-1:
            q.put((dist, x+1, y, req_keys.copy()))
        # s
        if y < len(grid)-1:
            q.put((dist, x, y+1, req_keys.copy()))
        # w
        if 0 < x:
            q.put((dist, x-1, y, req_keys.copy()))
    
    return keys


def find_path(grid):
    cur_pos, all_keys, keys_pos, _ = find_items(grid)
    q = queue.PriorityQueue()
    key_state = set()
    key_cache = dict()
    q.put((0, cur_pos, set()))

    while not q.empty():
        dist, cur_pos, coll_keys = q.get()
        
        # if state already seen then continue
        if (frozenset(cur_pos), frozenset(coll_keys)) in key_state:
            continue

        key_state.add((frozenset(cur_pos), frozenset(coll_keys)))

        # grab keys at new positions
        for pos in cur_pos:
            if grid[pos[1]][pos[0]] != "@":
                coll_keys.add(grid[pos[1]][pos[0]])

        # collection done
        if coll_keys == all_keys:
            return dist

        # cache dist and req keys to every other key from this key
        for pos in cur_pos:
            if pos not in key_cache:
                key_cache[pos] = find_keys(pos[0], pos[1], grid)

        # enqueue every key reachable with collected keys
        for pos in cur_pos:
            new_cur_pos = cur_pos.copy()
            new_cur_pos.remove(pos)

            for k, v in key_cache[pos].items():
                steps, req_keys = v
                if req_keys <= coll_keys:
                    q.put((dist+steps, new_cur_pos + [keys_pos[k]], coll_keys.copy()))
    
    raise Exception("No path")

if __name__ == "__main__":
    with open("input", "r") as file:
        grid = []
        for line in file:
            grid.append(line.strip("\n"))

        # print(grid)
        # print(find_path(grid))
        start = time.perf_counter()
        print(find_path(grid))
        print("{} seconds".format(time.perf_counter()-start))