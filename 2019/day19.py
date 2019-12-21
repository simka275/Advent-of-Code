
import time

# exit codes:
# 0 - program halted 
# 1 - running
# 2 - expect input
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
                return 

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
                if signal is None:
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


def check_pos(x,y,program):
    process = IntcodeProcess(program)
    process.Run(x)
    return process.Run(y)
    

def calc_affected(rows, cols, program):
    affected = 0
    # x, y, w, isbeam = 0, 0, 0, False
    # while True:
    start_x = 0
    for y in range(rows):
        in_beam = False
        for x in range(start_x, cols):
            # check pos if in beam
            ret = check_pos(x,y,program)
            affected += ret
            # Stepped out of beam
            if in_beam and ret == 0:
                continue
            # set in beam
            in_beam = ret == 1
        # step start x
        start_x += 1
    return affected


# travel down bottom and left side of beam and draw a 100x100 square up 
# and to the right of current pos, then check if the corners of the 
# square is inside beam
def find_square_pos(size, program):
    x,y = 0, max(size-1,5) # avoid empty rows at start
    while True:
        # find beam
        if check_pos(x,y,program) == 1:
            # if pos diagonally opposite current is inside beam 
            # then the square fits
            if y >= size-1 and check_pos(x+(size-1),y-(size-1), program) == 1:
                return x,y-(size-1)
            # else next row
            else:
                y += 1
        # else check next col
        else:
            x += 1


if __name__ == "__main__":
    with open("input", "r") as file:
        program = file.readline().strip().split(",")
        
        start = time.perf_counter()
        print(calc_affected(50, 50, program))
        print("{} seconds".format(time.perf_counter()-start))
        start = time.perf_counter()
        pos = find_square_pos(100, program)
        print("{} seconds".format(time.perf_counter()-start))
        print("{}*10000+{}={}".format(pos[0], pos[1], pos[0]*10000+pos[1]))