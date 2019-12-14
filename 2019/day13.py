import time
import os

paddle_x, ball_x = None, None


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
                # self.Store(store_addr, str(signal))
                # self.Store(store_addr, str(input("-1 0 1:")))

                # Hack the game
                inp = "0"
                if ball_x < paddle_x:
                    inp = "-1"
                elif ball_x > paddle_x:
                    inp = "1"
                self.Store(store_addr, inp)

                # self.exit_code = 2 # exit code -> game setup done
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
            

def create_grid(p):
    grid = dict()
    while True:
        x = p.Run()
        y = p.Run()
        tile_type = p.Run()
        if p.exit_code == 0:
            break
        grid[(x,y)] = tile_type
    return grid


def render_grid(grid):
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for k in grid.keys():
        min_x = min(k[0], min_x)
        max_x = max(k[0], max_x)
        min_y = min(k[1], min_y)
        max_y = max(k[1], max_y)

    width, height = max_x-min_x+1, max_y-min_y+1

    img = []
    for y in range(height):
        img.append([])
        for _ in range(width):
            img[y].append(" ")

    for k,v in grid.items():
        x, y = k[0], k[1]
        if v == 1:
            img[y-min_y][x-min_x] = "X"
        elif v == 2:
            img[y-min_y][x-min_x] = "*"
        elif v == 3:
            img[y-min_y][x-min_x] = "-"
        elif v == 4:
            img[y-min_y][x-min_x] = "O"

    for y in range(height):
        for x in range(width):
            print(img[y][x], end="")
        print("")


def part_one():
    with open("input", "r") as file:
        mem = file.readline().strip().split(",")
        p = IntcodeProcess(mem)
        grid = create_grid(p)
        block_tiles = 0
        for _, tile_type in grid.items():
            if tile_type == 2:
                block_tiles += 1
        print(block_tiles)


def run_game(p, coins):
    global ball_x
    global paddle_x
    p.program_memory[0] = str(coins)
    grid = dict()
    while True:
        x = p.Run()
        y = p.Run()
        param = p.Run()

        if p.exit_code == 0:
            break

        if x == -1 and y == 0:
            print("Score: {}".format(param))
        else:
            grid[(x,y)] = param
        
        if param == 3:
            paddle_x = x
        elif param == 4:
            ball_x = x

        # Setup done
        # if p.exit_code == 2:
        #     time.sleep(1)
        #     os.system("cls")
        #     render_grid(grid)


def part_two():
    with open("input", "r") as file:
        mem = file.readline().strip().split(",")
        p = IntcodeProcess(mem)
        run_game(p, 2)


if __name__ == "__main__":
    # part_one()
    part_two()
