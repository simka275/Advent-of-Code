
import math
import queue

class IntcodeProcess:
    def __init__(self, program):
        self.program_memory = program.copy()
        self.data_memory = dict()
        self.relative_base = 0
        self.ip = 0
        self.exit_code = 1

    def CalcAddress(self, instr, param_i):
        addr_mode = 0 if (param_i+2) > len(instr) else int(instr[-(param_i+2)])
        # Value
        if addr_mode == 0:
            return self.Load(self.ip+param_i)
        # Indirect
        elif addr_mode == 1:
            return self.ip+param_i
        # Relative
        elif addr_mode == 2:
            return self.relative_base + self.Load(self.ip+param_i)
        else:
            raise Exception("Unsupported addr mode")

    def Clone(self):
        new_p = IntcodeProcess(self.program_memory)
        new_p.data_memory = self.data_memory.copy()
        new_p.relative_base = self.relative_base
        new_p.ip = self.ip
        new_p.exit_code = self.exit_code
        return new_p


    def Load(self, addr):
        if addr < len(self.program_memory):
            return int(self.program_memory[addr])
        else:
            if addr in self.data_memory:
                return int(self.data_memory[addr])
            else:
                return 0
    
    def Store(self, addr, value):
        if addr < len(self.program_memory):
            self.program_memory[addr] = value
        else:
            self.data_memory[addr] = value

    def Run(self, signal=None):
        a, b, store_addr = 0, 0, 0
        while True:
            instr = self.program_memory[self.ip]
            opcode = int(instr[-2:])

            if opcode == 99:
                self.exit_code = 0
                return None

            # One param
            if opcode in [1, 2, 4, 5, 6, 7, 8, 9]:
                a = self.Load(self.CalcAddress(instr, 1))

            # Two params and 
            if opcode in [1, 2, 5, 6, 7, 8]:
                b = self.Load(self.CalcAddress(instr, 2))
                store_addr = self.CalcAddress(instr, 3)
            
            if opcode in [3]:
                store_addr = self.CalcAddress(instr, 1)

            # Addition
            if opcode == 1:
                self.Store(store_addr, str(a + b))
                self.ip += 4
            # Multiplication
            elif opcode == 2:
                self.Store(store_addr, str(a * b))
                self.ip += 4
            # Input
            elif opcode == 3:
                # Read input
                self.Store(store_addr, str(signal))
                self.ip += 2
            # Output
            elif opcode == 4:
                self.ip += 2
                return a
            # jump if true
            elif opcode == 5:
                if a != 0:
                    self.ip = b
                else:
                    self.ip += 3
            # jump if false
            elif opcode == 6:
                if a == 0:
                    self.ip = b
                else:
                    self.ip += 3
            # less than
            elif opcode == 7:
                if a < b:
                    self.Store(store_addr, "1")
                else:
                    self.Store(store_addr, "0")
                self.ip += 4
            # equals
            elif opcode == 8:
                if a == b:
                    self.Store(store_addr, "1")
                else:
                    self.Store(store_addr, "0")
                self.ip += 4
            # relative base adjust
            elif opcode == 9:
                self.relative_base += a
                self.ip += 2
            else:
                raise Exception("Not implemtend opcode {0}".format(opcode))


def explore(process):
    min_dist, goal_x, goal_y = math.inf, None, None
    visited = dict()
    process_queue = queue.Queue()
    process_queue.put( (0, 0, 0, process.Clone()) )
    while not process_queue.empty():
        x, y, dist, p = process_queue.get()
        # north 1
        if (x,y-1) not in visited:
            new_pos = (x, y-1)
            new_p = p.Clone()
            r = new_p.Run(1)
            visited[new_pos] = r
            if r != 0:
                process_queue.put((new_pos[0], new_pos[1], dist+1, new_p))
            if r == 2:
                min_dist, goal_x, goal_y = min(min_dist, dist+1), new_pos[0], new_pos[1]
        # east 4
        if (x+1,y) not in visited:
            new_pos = (x+1,y)
            new_p = p.Clone()
            r = new_p.Run(4)
            visited[new_pos] = r
            if r != 0:
                process_queue.put((new_pos[0], new_pos[1], dist+1, new_p))
            if r == 2:
                min_dist, goal_x, goal_y = min(min_dist, dist+1), new_pos[0], new_pos[1]
        # south 2
        if (x,y+1) not in visited:
            new_pos = (x,y+1)
            new_p = p.Clone()
            r = new_p.Run(2)
            visited[new_pos] = r
            if r != 0:
                process_queue.put((new_pos[0], new_pos[1], dist+1, new_p))
            if r == 2:
                min_dist, goal_x, goal_y = min(min_dist, dist+1), new_pos[0], new_pos[1]
        # west 3
        if (x-1,y) not in visited:
            new_pos = (x-1,y)
            new_p = p.Clone()
            r = new_p.Run(3)
            visited[new_pos] = r
            if r != 0:
                process_queue.put((new_pos[0], new_pos[1], dist+1, new_p))
            if r == 2:
                min_dist, goal_x, goal_y = min(min_dist, dist+1), new_pos[0], new_pos[1]
                
    return visited, min_dist, goal_x, goal_y


def create_grid(points):
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for k in points.keys():
        min_x = min(k[0], min_x)
        max_x = max(k[0], max_x)
        min_y = min(k[1], min_y)
        max_y = max(k[1], max_y)

    width, height = max_x-min_x+1, max_y-min_y+1

    grid = []
    for y in range(height):
        grid.append([])
        for _ in range(width):
            grid[y].append(" ")

    for k,v in points.items():
        x, y = k[0], k[1]

        # # start pos
        # if x == 0 and y == 0:
        #     grid[y-min_y][x-min_x] = "D"
        #     continue

        if v == 0:
            grid[y-min_y][x-min_x] = "#"
        elif v == 1:
            grid[y-min_y][x-min_x] = "-"
        elif v == 2:
            grid[y-min_y][x-min_x] = "*"
    
    return grid, min_x, min_y
    

def render_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(grid[y][x], end="")
        print("")


def find_max_distance(grid, start_x, start_y):
    max_dist = 0
    visited = set()
    q = queue.Queue()
    q.put((start_x, start_y, 0))
    while not q.empty():
        x, y, dist = q.get()
        visited.add( (x,y) )
        max_dist = max(max_dist, dist)
        # north
        if (x, y-1) not in visited and y > 0 and grid[y-1][x] != "#":
            q.put( (x, y-1, dist+1) ) 
        # east
        if (x+1, y) not in visited and x+1 < len(grid[y]) and grid[y][x+1] != "#":
            q.put( (x+1, y, dist+1) )
        # south
        if (x, y+1) not in visited and y+1 < len(grid) and grid[y+1][x] != "#":
            q.put( (x, y+1, dist+1) )
        # west
        if (x-1, y) not in visited and x > 0 and grid[y][x-1] != "#":
            q.put( (x-1, y, dist+1) )

    return max_dist

    


if __name__ == "__main__":
    with open("input", "r") as file:
        mem = file.readline().strip().split(",")
        p = IntcodeProcess(mem)
        points, min_dist, x, y = explore(p)
        grid, offset_x, offset_y = create_grid(points)
        render_grid(grid)
        print("Distance to goal: {0}, position: x={1} y={2}".format(min_dist, x-offset_x, y-offset_y))
        print("Max distance from goal: {}".format(find_max_distance(grid, x-offset_x, y-offset_y)))