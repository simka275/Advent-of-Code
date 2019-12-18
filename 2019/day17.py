
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
        if signal:
            self.exit_code = 1
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
                if not signal:
                    self.exit_code = 2
                    return
                self.Store(store_addr, str(signal))
                signal = None
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
            

def create_grid(memory):
    p = IntcodeProcess(memory)
    grid = [[]]
    row = 0
    while True:
        ret = p.Run()
        if not ret:
            break

        if ret == 10:
            grid.append([])
            row += 1
        else:
            grid[row].append(ret)

    grid = grid[:-2]
    return grid
    

def render_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(chr(grid[y][x]), end="")
        print("")


def calc_alignement(grid):
    sum = 0
    for y in range(1,len(grid)-1):
        for x in range(1,len(grid[y])-1):
            if grid[y][x] == 35 and grid[y-1][x] == 35 and grid[y][x+1] == 35 and grid[y+1][x] == 35 and grid[y][x-1] == 35:
                sum += y*x
                grid[y][x] = 79
    return sum


def part_one():
    with open("input", "r") as file:
        mem = file.readline().strip().split(",")
        grid = create_grid(mem)
        render_grid(grid)
        res = calc_alignement(grid)
        render_grid(grid)
        print(res)


def find_robot(grid):
    robot_ascii = [ord('^'), ord('>'), ord('v'), ord('<')]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in robot_ascii:
                return x,y,robot_ascii.index(grid[y][x])
    return None, None, None


def find_path(grid):
    robot_x, robot_y, direction = find_robot(grid)
    path = []
    steps = 0

    while True:
        # Move straight
        if direction == 0 and robot_y > 0 and grid[robot_y-1][robot_x] == ord('#'):
            robot_y -= 1
            steps += 1
            continue
        elif direction == 1 and robot_x < len(grid[robot_y])-1 and grid[robot_y][robot_x+1] == ord('#'):
            robot_x += 1
            steps += 1
            continue
        elif direction == 2 and robot_y < len(grid)-1 and grid[robot_y+1][robot_x] == ord('#'):
            robot_y += 1
            steps += 1
            continue
        elif direction == 3 and robot_x > 0 and grid[robot_y][robot_x-1] == ord('#'):
            robot_x -= 1
            steps += 1
            continue

        # Turn pos
        next_pos_right, next_pos_left = None, None
        if direction == 0:
            next_pos_right = (robot_x+1, robot_y)
            next_pos_left = (robot_x-1, robot_y)
        elif direction == 1:
            next_pos_right = (robot_x, robot_y+1)
            next_pos_left = (robot_x, robot_y-1)
        elif direction == 2:
            next_pos_right = (robot_x-1, robot_y)
            next_pos_left = (robot_x+1, robot_y)
        elif direction == 3:
            next_pos_right = (robot_x, robot_y-1)
            next_pos_left = (robot_x, robot_y+1)

        # turn
        path.append(steps)
        steps = 0
        if 0 <= next_pos_right[0] < len(grid[robot_y]) and 0 <= next_pos_right[1] < len(grid) and grid[next_pos_right[1]][next_pos_right[0]] == ord('#'):
            direction = (direction+1) % 4
            path.append('R')
            continue
        elif 0 <= next_pos_left[0] < len(grid[robot_y]) and 0 <= next_pos_left[1] < len(grid) and grid[next_pos_left[1]][next_pos_left[0]] == ord('#'):
            direction = (direction-1) % 4
            path.append('L')
            continue
        
        break

    return path[1:]


def translate_ascii(mf):
    letters = ['A', 'B', 'C', 'R', 'L']
    res = []
    for i in range(len(mf)):
        if mf[i] in letters:
            if res and res[-1] != ord(','):
                res.append(ord(','))
            res.append(ord(mf[i]))
            if i < len(mf)-1:
                res.append(ord(','))
        else:
            res.append(ord(mf[i]))
    return res


assert translate_ascii("ABC") == [ord('A'), ord(','), ord('B'), ord(','),ord('C')]


def compress(s):
    candidates = []
    for start in range(len(s)):
        for offset in range(len(s)+1-start, 0, -1):
            candidate = s[start:start+offset]
            if len(translate_ascii(candidate)) <= 20 and not candidate in candidates:
                candidates.append(candidate)
    
    candidates.sort(reverse=True)

    for i in range(len(candidates)):
        for j in range(i+1, len(candidates)):
            if candidates[i] == candidates[j]:
                continue
            for k in range(j+1, len(candidates)):
                if candidates[i] == candidates[k] or candidates[j] == candidates[k]:
                    continue
                cs = s.replace(candidates[i], "A").replace(candidates[j], "B").replace(candidates[k], "C")
                if cs.replace("A","").replace("B","").replace("C","") == "":
                    return candidates[i],candidates[j],candidates[k], cs

    raise Exception("Fail!")


def part_two():
    with open("input", "r") as file:
        mem = file.readline().strip().split(",")
        grid = create_grid(mem)
        # render_grid(grid)
        path = find_path(grid)
        movement = "".join(map(str, path))
        a,b,c, movement = compress(movement)
        input_list = translate_ascii(movement)
        input_list.append(10)
        input_list += translate_ascii(a)
        input_list.append(10)
        input_list += translate_ascii(b)
        input_list.append(10)
        input_list += translate_ascii(c)
        input_list.append(10)

        mem[0]="2"
        p = IntcodeProcess(mem)
        grid = ""
        in_signal = None
        while True:
            ret = p.Run(in_signal)
            in_signal = None
            if p.exit_code == 0:
                print(grid)
                break
            elif p.exit_code == 2:
                # input
                if grid:
                    print(grid)
                grid = ""
                if input_list:
                    in_signal = input_list.pop(0)
                    print(chr(in_signal), end="")
                else:
                    in_signal = input()
            else:
                if ret > 255:
                    print(ret)
                else:
                    grid += chr(ret)


if __name__ == "__main__":
    # part_one()
    part_two()
        
