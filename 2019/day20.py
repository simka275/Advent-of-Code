
import time
import queue

def eval_grid(grid):
    start, end, = None, None
    labels = dict()
    portals = dict()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if not grid[y][x].isalpha():
                continue
            
            label = None
            pos = None
            # e
            if x+1 < len(grid[y]) and grid[y][x+1].isalpha():
                label = grid[y][x] + grid[y][x+1]
                if x+2 < len(grid[y]) and grid[y][x+2] == ".":
                    pos = [x+2,y]
                else:
                    pos = [x-1,y]
                # level
                if pos[0]-3 < 0 or pos[0]+3 >= len(grid[pos[1]]):
                    pos.append(-1)
                else:
                    pos.append(1)
            # s
            elif y+1 < len(grid) and grid[y+1][x].isalpha():
                label = grid[y][x] + grid[y+1][x]
                if y+2 < len(grid) and grid[y+2][x] == ".":
                    pos = [x,y+2]
                else:
                    pos = [x,y-1]
                # level
                if pos[1]-3 < 0 or pos[1]+3 >= len(grid):
                    pos.append(-1)
                else:
                    pos.append(1)
            else:
                continue

            if label in labels:
                labels[label].append(pos)
            else:
                labels[label] = [pos]
    
    for label in labels:
        if label == "AA":
            start = tuple(labels[label][0])
        elif label == "ZZ":
            end = tuple(labels[label][0])
        else:
            portals[tuple(labels[label][0])] = tuple(labels[label][1])
            portals[tuple(labels[label][1])] = tuple(labels[label][0])

    # print(labels)
    # for l,v in labels.items():
    #     print(l,v)
    return start, end, portals


def bfs(start, end, portals, grid):
    q = queue.Queue()
    visited = set()
    q.put((0, start[0], start[1]))
    while not q.empty():
        cost, x, y = q.get()
        visited.add((x,y))

        if  x == end[0] and y == end[1]:
            return cost
        # n
        if y > 0 and grid[y-1][x] == "." and (x,y-1) not in visited:
            q.put((cost+1,x,y-1))
        # e
        if x+1 < len(grid) and grid[y][x+1] == "." and (x+1,y) not in visited:
            q.put((cost+1,x+1,y))
        # s
        if y+1 < len(grid) and grid[y+1][x] == "." and (x,y+1) not in visited:
            q.put((cost+1,x,y+1))
        # w
        if x > 0 and grid[y][x-1] == "." and (x-1,y) not in visited:
            q.put((cost+1,x-1,y))
        # teleport
        if (x,y,1) in portals:
            q.put((cost+1,portals[(x,y,1)][0],portals[(x,y,1)][1]))
        if (x,y,-1) in portals:
            q.put((cost+1,portals[(x,y,-1)][0],portals[(x,y,-1)][1]))


def bfs_levels(start, end, portals, grid, max_level):
    q = queue.Queue()
    visited = set()
    q.put((0, start[0], start[1], 0))
    while not q.empty():
        cost, x, y,level = q.get()

        # if (x,y,level) in visited:
        #     continue

        # visited[(x,y,level)] = cost
        visited.add((x,y,level))

        if level > max_level:
            continue

        if x == end[0] and y == end[1] and level == 0:
            return cost
        # n
        if y > 0 and grid[y-1][x] == "." and (x,y-1,level) not in visited:
            q.put((cost+1,x,y-1,level))
        # e
        if x+1 < len(grid[y]) and grid[y][x+1] == "." and (x+1,y,level) not in visited:
            q.put((cost+1,x+1,y,level))
        # s
        if y+1 < len(grid) and grid[y+1][x] == "." and (x,y+1,level) not in visited:
            q.put((cost+1,x,y+1,level))
        # w
        if x > 0 and grid[y][x-1] == "." and (x-1,y,level) not in visited:
            q.put((cost+1,x-1,y,level))
        # teleport
        if (x,y,1) in portals and (portals[(x,y,1)][0],portals[(x,y,1)][1],level+1) not in visited:
            # print("{} -> {}".format((x,y,level), (portals[(x,y,1)][0],portals[(x,y,1)][1],level+1)))
            q.put((cost+1,portals[(x,y,1)][0],portals[(x,y,1)][1],level+1))
        if level > 0 and (x,y,-1) in portals and (portals[(x,y,-1)][0],portals[(x,y,-1)][1],level-1) not in visited:
            # print("{} -> {}".format((x,y,level), (portals[(x,y,-1)][0],portals[(x,y,-1)][1],level-1)))
            q.put((cost+1,portals[(x,y,-1)][0],portals[(x,y,-1)][1],level-1))
    raise Exception("No path")


if __name__ == "__main__":
    with open("input", "r") as file:
        grid = []
        for line in file:
            grid.append(line.strip("\n"))

        # for row in grid:
        #     print(row)

        start, end, portals = eval_grid(grid)
        # print(start, end, portals)
        # print(bfs(start,end,portals,grid)) #part one

        start_t = time.perf_counter()
        print(bfs_levels(start,end,portals,grid,1000)) #part two
        print("{} seconds".format(time.perf_counter()-start_t))
        
        # for max_level in range(20):
        #     start_t = time.perf_counter()
        #     print(bfs_levels(start,end,portals,grid,max_level)) #part two
        #     print("{},{}".format(max_level,time.perf_counter()-start_t))