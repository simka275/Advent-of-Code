
from queue import PriorityQueue


def find_lowest_risk_level(cave):
    queue = PriorityQueue()
    goal = (len(cave[0])-1,len(cave)-1)
    # (cost,x,y)
    queue.put((0,0,0))
    visited = {}
    while queue:
        cost,x,y = queue.get()
        if (x,y) == goal:
            return cost
        for xx,yy in [(x,y-1),(x+1,y),(x,y+1),(x-1,y)]:
            if xx < 0 or xx >= len(cave[y]):
                continue
            if yy < 0 or yy >= len(cave):
                continue
            new_cost = cost + cave[yy][xx]
            if (xx,yy) not in visited or new_cost < visited[xx,yy]:
                visited[xx,yy] = new_cost
                queue.put((new_cost,xx,yy))


def find_lowest_risk_level_x5(cave):
    queue = PriorityQueue()
    height, length = len(cave), len(cave[0])
    goal = (len(cave[0])*5-1,len(cave)*5-1)
    # (cost,x,y)
    queue.put((0,0,0))
    visited = {}
    while queue:
        cost,x,y = queue.get()
        if (x,y) == goal:
            return cost
        for xx,yy in [(x,y-1),(x+1,y),(x,y+1),(x-1,y)]:
            if xx < 0 or xx >= length*5:
                continue
            if yy < 0 or yy >=height*5:
                continue

            x_incr = 0
            y_incr = 0
            if xx >= length:
                x_incr = xx // length
            if yy >=height:
                y_incr = yy //height
            step_cost = cave[yy %height][xx % length] + x_incr + y_incr
            if step_cost > 9:
                step_cost = 1 + step_cost % 10
            new_cost = cost + step_cost
            if (xx,yy) not in visited or new_cost < visited[xx,yy]:
                visited[xx,yy] = new_cost
                queue.put((new_cost,xx,yy))


if __name__ == "__main__":
    cave = []
    with open("input", "r") as file:
        for line in file:
            row = [int(x) for x in line.strip()]
            cave.append(row)

    # p1
    print(find_lowest_risk_level(cave))

    # p2
    print(find_lowest_risk_level_x5(cave))