
class Machine:
    def __init__(self, memory):
        self.memory = memory
        self.accumulator = 0
        self.pc = 0
        self.history = []
        self.mod_pc = None
        self.mod_history = []
        self.mod_accumulator = 0

    def _execute(self, instruction):
        op, arg = instruction.split()
        num = int(arg[0:])
        if op == "acc":
            if self.mod_pc:
                self.mod_accumulator += num
            else:
                self.accumulator += num
            self.pc += 1
        elif op == "nop":
            self.pc += 1
        elif op == "jmp":
            self.pc += num

    def run_p1(self):
        while True:
            if self.pc in self.history:
                break
            self.history.append(self.pc)
            self._execute(self.memory[self.pc])

    def run_p2(self):
        while self.pc != len(self.memory):
            # If loop or out of bounds then
            # reset to mod pc, reset history, and acc and revert mem change
            # then run from that pc
            if self.pc in self.history or self.pc in self.mod_history or self.pc > len(self.memory):
                self.pc = self.mod_pc
                self.mod_pc = None
                self.mod_history = []
                self.mod_accumulator = 0
                if self.memory[self.pc].find("jmp") == 0:
                    self.memory[self.pc] = self.memory[self.pc].replace("jmp", "nop")
                elif self.memory[self.pc].find("nop") == 0:
                    self.memory[self.pc] = self.memory[self.pc].replace("nop", "jmp")
                self.history.append(self.pc)
                self._execute(self.memory[self.pc])
            # If we are running with modified memory
            # run and store history in mod history
            elif self.mod_pc:
                self.mod_history.append(self.pc)
                self._execute(self.memory[self.pc])
            # if non mod and jmp instr modify and save pc and store in mod history
            elif self.memory[self.pc].find("jmp") == 0:
                self.memory[self.pc] = self.memory[self.pc].replace("jmp", "nop")
                self.mod_pc = self.pc
                self.mod_history.append(self.pc)
                self._execute(self.memory[self.pc])
            # if non mod and nop instr modify and save pc and store in mod history
            elif self.memory[self.pc].find("nop") == 0:
                self.memory[self.pc] = self.memory[self.pc].replace("nop", "jmp")
                self.mod_pc = self.pc
                self.mod_history.append(self.pc)
                self._execute(self.memory[self.pc])
            # else run and store in history
            else:
                self.history.append(self.pc)
                self._execute(self.memory[self.pc])

        # When program exit ok add mod accumulator to real accumlator
        self.accumulator += self.mod_accumulator



if __name__ == "__main__":
    mem = []
    with open("input", "r") as file:
        for line in file:
            mem.append(line.rstrip())

    m = Machine(mem)
    m.run_p1()
    print(m.accumulator)

    m = Machine(mem)
    m.run_p2()
    print(m.accumulator)

