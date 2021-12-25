
import math

class ALU:
    def __init__(self, instructions):
        self.instructions = instructions.copy()

    def run(self, _input):
        input = _input.copy()
        self.registers = {"w":0, "x":0, "y":0, "z":0}
        for instruction in self.instructions:
            op = instruction[:3]
            arg1 = instruction[4]
            arg2 = instruction[6:] if len(instruction) > 5 else None
            if arg2 in self.registers:
                arg2 = self.registers[arg2]
            elif arg2:
                arg2 = int(arg2)
            if op == "inp":
                self.registers[arg1] = input.pop(0)
            elif op == "add":
                self.registers[arg1] += arg2
            elif op == "mul":
                self.registers[arg1] *= arg2
            elif op == "div":
                self.registers[arg1] = int(self.registers[arg1] / arg2)
            elif op == "mod":
                self.registers[arg1] = int(self.registers[arg1] % arg2)
            elif op == "eql":
                self.registers[arg1] = 1 if self.registers[arg1] == arg2 else 0

alu = ALU(["inp x", "mul x -1"])
alu.run([11])
assert(alu.registers["x"] == -11)

alu = ALU(["inp z", "inp x", "mul z 3", "eql z x"])
alu.run([-10, -30])
assert(alu.registers["z"] == 1)
alu.run([-10, 30])
assert(alu.registers["z"] == 0)

alu = ALU(['inp w', 'add z w', 'mod z 2', 'div w 2', 'add y w', 'mod y 2', 'div w 2', 'add x w', 'mod x 2', 'div w 2', 'mod w 2'])
alu.run([9])
assert(alu.registers["w"] == 1 and alu.registers["x"] == 0 and alu.registers["y"] == 0 and alu.registers["z"] == 1)
alu.run([10])
assert(alu.registers["w"] == 1 and alu.registers["x"] == 0 and alu.registers["y"] == 1 and alu.registers["z"] == 0)
alu.run([1])
assert(alu.registers["w"] == 0 and alu.registers["x"] == 0 and alu.registers["y"] == 0 and alu.registers["z"] == 1)



def find_larget_model_nr(instructions):
    # Restrictions on the model number w
    # w0 = w13 + 6 -> w0 = 9, w13 = 3
    # w1 = w12 - 8 -> w1 = 1, w12 = 9
    # w2 = w11 - 7 -> w2 = 2, w11 = 9
    # w3 = w4 + 2  -> w3 = 9, w4 = 7
    # w5 = w10 - 6 -> w5 = 3, w10 = 9
    # w6 = w7 + 4  -> w6 = 9, w7 = 5
    # w8 = w9 + 8  -> w8 = 9, w9 = 1
    # 0 < wi < 10
    # -> n = 91297395919993
    return 91297395919993


def find_smallest_model_nr(instructions):
    # w0 = w13 + 6 -> w0 = 7, w13 = 1
    # w1 = w12 - 8 -> w1 = 1, w12 = 9
    # w2 = w11 - 7 -> w2 = 1, w11 = 8
    # w3 = w4 + 2  -> w3 = 3, w4 = 1
    # w5 = w10 - 6 -> w5 = 1, w10 = 7
    # w6 = w7 + 4  -> w6 = 5, w7 = 1
    # w8 = w9 + 8  -> w8 = 9, w9 = 1
    # 0 < wi < 10
    # -> 71131151917891
    return 71131151917891





if __name__ == "__main__":
    instructions = []
    with open("input", "r") as file:
        for line in file:
            instructions.append(line.strip())

    # p1
    print(find_larget_model_nr(instructions))

    # p2
    print(find_smallest_model_nr(instructions))