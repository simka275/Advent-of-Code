
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


def springscript_ascii(s):
    res = []
    for w in s:
        for c in w:
            res.append(ord(c))
        res.append(ord("\n"))
    return res


def exec_process(process, input_list):
    insig = None
    out = ""
    while True:
        ret = process.Run(insig)
        insig = None
        if process.exit_code == 0:
            print(out, end="")
            break
        elif process.exit_code == 1:
            if ret < 255:
                out += chr(ret)
            else:
                out += str(ret)
        elif process.exit_code == 2:
            if out:
                print(out, end="")
                out = ""
            if input_list:
                insig = input_list.pop(0)
            else:
                insig = input("in: ")


part_one_script = [
    "NOT C J",
    "AND D J",
    "NOT A T",
    "OR T J",
    "WALK",
]

part_two_script = [
    "NOT A T",
    "NOT B J",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "AND E T",
    "OR E T",
    "AND I T",
    "OR H T",
    "OR F T",
    "AND T J",
    "RUN",
]

part_two_script = [
    "NOT A T",
    "NOT B J",
    "OR T J",
    "NOT C T",
    "OR T J",
    "OR E T",
    "AND E T",
    "OR H T",
    "AND T J",
    "AND D J",
    "RUN",
]

if __name__ == "__main__":
    with open("input", "r") as file:
        program = file.readline().strip().split(",")
        process = IntcodeProcess(program)
        # input_list = springscript_ascii(part_one_script)
        input_list = springscript_ascii(part_two_script)
        exec_process(process, input_list)

