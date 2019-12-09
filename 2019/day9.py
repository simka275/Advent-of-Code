

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

    def Run(self, signal):
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
                # print(a, end=" ")
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
            

def execute_process(p, sig):
    res = []
    while p.exit_code != 0:
        out = p.Run(sig)
        if out != None:
            res.append(out)
    return res


assert execute_process(IntcodeProcess("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")), 0) == [int(x) for x in "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")]
assert len(str(execute_process(IntcodeProcess("1102,34915192,34915192,7,4,7,99,0".split(",")), 0)[0])) == 16
assert execute_process(IntcodeProcess("104,1125899906842624,99".split(",")), 0) == [1125899906842624]


if __name__ == "__main__":
    with open("input", "r") as file:
        mem = file.readline().strip().split(",")
        p = IntcodeProcess(mem)
        # print(execute_process(IntcodeProcess(mem), 1))
        print(execute_process(IntcodeProcess(mem), 2))