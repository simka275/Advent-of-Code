
from itertools import permutations

class Amplifier:
    def __init__(self, mem, phase):
        self.memory = mem.copy()
        self.phase = phase
        self.phase_set = False
        self.ip = 0
        self.exit_code = 1

    def run(self, signal):
        a, b, store_addr = 0, 0, 0
        
        while self.memory[self.ip][-2:] != "99":
            instr = self.memory[self.ip]
            opcode = int(instr[-2:])
            get_addr_mode = lambda x, i: 0 if i > len(instr) else int(x[-i])

            # One param
            if opcode in [1, 2, 4, 5, 6, 7, 8]:
                addr_mode_a = get_addr_mode(instr, 3)
                param = int(self.memory[self.ip+1])
                if addr_mode_a == 0:
                    a = int(self.memory[param])
                elif addr_mode_a == 1:
                    a = param

            # Two params and 
            if opcode in [1, 2, 5, 6, 7, 8]:
                # reg b
                addr_mode_b = get_addr_mode(instr, 4)
                param = int(self.memory[self.ip+2])
                if addr_mode_b == 0:
                    b = int(self.memory[param])
                elif addr_mode_b == 1:
                    b = param
                # 
                store_addr = int(self.memory[self.ip+3])
            
            if opcode in [3]:
                store_addr = int(self.memory[self.ip+1])

            # Addition
            if opcode == 1:
                self.memory[store_addr] = str(a + b)
                self.ip += 4
            # Multiplication
            elif opcode == 2:
                self.memory[store_addr] = str(a * b)
                self.ip += 4
            # Input
            elif opcode == 3:
                # Read from phase and amplifier input
                if not self.phase_set:
                    self.memory[store_addr] = str(self.phase)
                    self.phase_set = True
                else:
                    self.memory[store_addr] = str(signal)
                self.ip += 2
            # Output
            elif opcode == 4:
                self.ip += 2
                return int(a)
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
                    self.memory[store_addr] = 1
                else:
                    self.memory[store_addr] = 0
                self.ip += 4
            # equals
            elif opcode == 8:
                if a == b:
                    self.memory[store_addr] = 1
                else:
                    self.memory[store_addr] = 0
                self.ip += 4
            else:
                raise Exception("Not implemtend opcode {0}".format(opcode))
            
        self.exit_code = 0
        return None


def create_amplifiers(memory, phase_settings):
    amplifiers = []
    for phase in phase_settings:
        amplifiers.append(Amplifier(memory, phase))
    return amplifiers


def run_amplifiers(amplifiers):
    in_signal = 0
    i = 0
    while amplifiers[i].exit_code == 1:
        output_signal = amplifiers[i].run(in_signal)
        if amplifiers[i].exit_code == 0:
            return in_signal
        else:
            in_signal = output_signal
        i = (i+1) % len(amplifiers)


assert run_amplifiers(create_amplifiers("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(","), [4,3,2,1,0])) == 43210
assert run_amplifiers(create_amplifiers("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0".split(","), [0,1,2,3,4])) == 54321
assert run_amplifiers(create_amplifiers("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0".split(","), [1,0,4,3,2])) == 65210


assert run_amplifiers(create_amplifiers("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(","), [9,8,7,6,5])) == 139629729
assert run_amplifiers(create_amplifiers("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10".split(","), [9,7,8,5,6])) == 18216


if __name__ == "__main__":
    max_thrust = 0
    with open("input", "r") as file:
        mem = file.readline().strip().split(",")
        # perms = list(permutations([0,1,2,3,4])) # part one
        perms = list(permutations([5,6,7,8,9])) # part two
        for perm in perms:
            thrust = run_amplifiers(create_amplifiers(mem, perm))
            max_thrust = max(thrust, max_thrust)
    print(max_thrust)
