
import os
import time

def render_grid(grid):
    for row in grid:
        print(row)


def tick(grid):
    new_grid = []
    for y in range(len(grid)):
        new_grid.append("")
        for x in range(len(grid[y])):
            neighbors = 0
            if y > 0:
                neighbors += 1 if grid[y-1][x] == "#" else 0
            if x+1 < len(grid[y]):
                neighbors += 1 if grid[y][x+1] == "#" else 0
            if y+1 < len(grid[y]):
                neighbors += 1 if grid[y+1][x] == "#" else 0
            if x > 0:
                neighbors += 1 if grid[y][x-1] == "#" else 0
            
            if grid[y][x] == "#" and neighbors != 1:
                new_grid[y] += "."
            elif grid[y][x] == "." and neighbors in [1,2]:
                new_grid[y] += "#"
            else:
                new_grid[y] += grid[y][x]

    return new_grid


def grid_to_str(grid):
    res = ""
    for row in grid:
        res += row
    return res


def calc_biodiversity(grid):
    res = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                res += 1 << y*len(grid[y])+x
    return res


def part_one():
    with open("input", "r") as file:
        grid = []
        seen = set()

        for row in file:
            grid.append(row.strip("\n"))
        
        while True:
            grid_str = grid_to_str(grid)
            if grid_str in seen:
                print("Repeat: ")
                render_grid(grid)
                print(calc_biodiversity(grid))
                break
            seen.add(grid_str)
            # render_grid(grid)
            grid = tick(grid)


def count_neighbors(x, y, grid, include_north=True, include_east=True, include_south=True, include_west=True):
    neighbors = 0
    if not grid:
        return neighbors

    if y > 0 and include_north:
        neighbors += 1 if grid[y-1][x] == "#" else 0
    if x+1 < len(grid[y]) and include_east:
        neighbors += 1 if grid[y][x+1] == "#" else 0
    if y+1 < len(grid[y]) and include_south:
        neighbors += 1 if grid[y+1][x] == "#" else 0
    if x > 0 and include_west:
        neighbors += 1 if grid[y][x-1] == "#" else 0
    return neighbors


def count_neighbors_inner(x,y, inner_grid, direction=""):
    neighbors = 0
    w, h = len(inner_grid[0]), len(inner_grid)
    if direction == "n":
        for j in range(w):
            if inner_grid[h-1][j] == "#":
                neighbors += 1
    elif direction == "e":
        for j in range(h):
            if inner_grid[j][0] == "#":
                neighbors += 1
    elif direction == "s":
        for j in range(w):
            if inner_grid[0][j] == "#":
                neighbors += 1
    elif direction == "w":
        for j in range(h):
            if inner_grid[j][w-1] == "#":
                neighbors += 1
    return neighbors


def tick_recursive(grids, iteration, w, h):
    new_grids = dict()
    for level in range(-iteration,iteration+1):
        new_grid = []
        old_grid = None if level not in grids else grids[level]
        outer_grid = None if level-1 not in grids else grids[level-1]
        inner_grid = None if level+1 not in grids else grids[level+1]
        # 
        for y in range(h):
            new_grid.append("")
            for x in range(w):
                neighbors = 0
                # north inner 
                if inner_grid and y == (h//2-1) and x == w//2:
                    neighbors += count_neighbors(x,y,old_grid, include_south=False)
                    neighbors += count_neighbors_inner(x,y,inner_grid,"s")
                # east inner 
                elif inner_grid and x == (w//2+1) and y == h//2:
                    neighbors += count_neighbors(x,y,old_grid, include_west=False)
                    neighbors += count_neighbors_inner(x,y,inner_grid, "w")
                # south inner 
                elif inner_grid and y == (h//2+1) and x == w//2:
                    neighbors += count_neighbors(x,y,old_grid, include_north=False)
                    neighbors += count_neighbors_inner(x,y,inner_grid,"n")
                # west inner 
                elif inner_grid and x == (w//2-1) and y == h//2:
                    neighbors += count_neighbors(x,y,old_grid, include_east=False)
                    neighbors += count_neighbors_inner(x,y,inner_grid,"e")
                # upper left corner
                elif outer_grid and x == 0 and y == 0:
                    neighbors += count_neighbors(x,y,old_grid,include_north=False,include_west=False)
                    neighbors += 1 if outer_grid and outer_grid[h//2-1][w//2] == "#" else 0
                    neighbors += 1 if outer_grid and outer_grid[h//2][w//2-1] == "#" else 0
                # upper right corner
                elif outer_grid and x == w-1 and y == 0:
                    neighbors += count_neighbors(x,y,old_grid,include_north=False,include_east=False)
                    neighbors += 1 if outer_grid and outer_grid[h//2-1][w//2] == "#" else 0
                    neighbors += 1 if outer_grid and outer_grid[h//2][w//2+1] == "#" else 0
                # bottom right corner
                elif outer_grid and x == w-1 and y == h-1:
                    neighbors += count_neighbors(x,y,old_grid,include_east=False,include_south=False)
                    neighbors += 1 if outer_grid and outer_grid[h//2][w//2+1] == "#" else 0
                    neighbors += 1 if outer_grid and outer_grid[h//2+1][w//2] == "#" else 0
                # bottom left
                elif outer_grid and x == 0 and y == h-1:
                    neighbors += count_neighbors(x,y,old_grid,include_south=False,include_west=False)
                    neighbors += 1 if outer_grid and outer_grid[h//2+1][w//2] == "#" else 0
                    neighbors += 1 if outer_grid and outer_grid[h//2][w//2-1] == "#" else 0
                # north outer line
                elif outer_grid and y == 0:
                    neighbors += count_neighbors(x,y,old_grid,include_north=False)
                    neighbors += 1 if outer_grid and outer_grid[h//2-1][w//2] == "#" else 0
                # east outer line
                elif outer_grid and x == w-1:
                    neighbors += count_neighbors(x,y,old_grid,include_east=False)
                    neighbors += 1 if outer_grid and outer_grid[h//2][w//2+1] == "#" else 0
                # south outer line
                elif outer_grid and y == h-1:
                    neighbors += count_neighbors(x,y,old_grid,include_south=False)
                    neighbors += 1 if outer_grid and outer_grid[h//2+1][w//2] == "#" else 0
                # west outer line
                elif outer_grid and x == 0:
                    neighbors += count_neighbors(x,y,old_grid,include_west=False)
                    neighbors += 1 if outer_grid and outer_grid[h//2][w//2-1] == "#" else 0
                # ignore middle
                elif x == w//2 and y == h//2:
                    new_grid[y] += "?"
                    continue
                # base case
                else:
                    neighbors += count_neighbors(x,y,old_grid)
                
                if old_grid and old_grid[y][x] == "#" and neighbors != 1:
                    new_grid[y] += "."
                elif old_grid and old_grid[y][x] == "." and neighbors in [1,2]:
                    new_grid[y] += "#"
                elif not old_grid and neighbors in [1,2]:
                    new_grid[y] += "#"
                else:
                    new_grid[y] += "." if not old_grid else old_grid[y][x]

        new_grids[level] = new_grid
    return new_grids


def render_grids(grids):
    for k in grids:
        print("Depth: {}".format(k))
        render_grid(grids[k])


def count_bugs(grids):
    bugs = 0
    for k in grids:
        for row in grids[k]:
            bugs += row.count("#")
    return bugs


def part_two():
    with open("input", "r") as file:
        grids = dict()
        grid = []

        for row in file:
            grid.append(row.strip("\n"))

        grid[2] = grid[2][:2] + "?" + grid[2][3:]
        grids[0] = grid

        # render_grids(grids)
        for i in range(200):
            grids = tick_recursive(grids, i+1, 5, 5)
            # render_grids(grids)

        print("#bugs: {}".format(count_bugs(grids)))

if __name__ == "__main__":
    part_one()
    part_two()
