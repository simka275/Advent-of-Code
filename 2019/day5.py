


def run_intcode(mem):
    # instruction pointer, registers
    ip, a, b, store_addr = 0, 0, 0, 0

    while mem[ip][-2:] != "99":
        instr = mem[ip]
        opcode = int(instr[-2:])
        get_addr_mode = lambda x, i: 0 if i > len(instr) else int(x[-i])

        # One param
        if opcode in [1, 2, 4, 5, 6, 7, 8]:
            addr_mode_a = get_addr_mode(instr, 3)
            param = int(mem[ip+1])
            if addr_mode_a == 0:
                a = int(mem[param])
            elif addr_mode_a == 1:
                a = param

        # Two params and 
        if opcode in [1, 2, 5, 6, 7, 8]:
            # reg b
            addr_mode_b = get_addr_mode(instr, 4)
            param = int(mem[ip+2])
            if addr_mode_b == 0:
                b = int(mem[param])
            elif addr_mode_b == 1:
                b = param
            # 
            store_addr = int(mem[ip+3])
        
        if opcode in [3]:
            store_addr = int(mem[ip+1])

        # Addition
        if opcode == 1:
            mem[store_addr] = str(a + b)
            ip += 4
        # Multiplication
        elif opcode == 2:
            mem[store_addr] = str(a * b)
            ip += 4
        # Input
        elif opcode == 3:
            mem[store_addr] = str(input("input:"))
            ip += 2
        # Output
        elif opcode == 4:
            print(a)
            ip += 2
        # jump if true
        elif opcode == 5:
            if a != 0:
                ip = b
            else:
                ip += 3
        # jump if false
        elif opcode == 6:
            if a == 0:
                ip = b
            else:
                ip += 3
        # less than
        elif opcode == 7:
            if a < b:
                mem[store_addr] = 1
            else:
                mem[store_addr] = 0
            ip += 4
        # equals
        elif opcode == 8:
            if a == b:
                mem[store_addr] = 1
            else:
                mem[store_addr] = 0
            ip += 4
        else:
            raise Exception("Not implemtend opcode {0}".format(opcode))
        
    
    return mem

# part one
assert run_intcode("1002,4,3,4,33".split(",")) == "1002,4,3,4,99".split(",")
assert run_intcode("1101,100,-1,4,0".split(",")) == "1101,100,-1,4,99".split(",")
# assert run_intcode("03,0,04,0,99".split(","))

# part two
# assert run_intcode("3,9,8,9,10,9,4,9,99,-1,8".split(","))
# assert run_intcode("3,9,7,9,10,9,4,9,99,-1,8".split(","))
# assert run_intcode("3,3,1108,-1,8,3,4,3,99".split(","))
# assert run_intcode("3,3,1107,-1,8,3,4,3,99".split(","))
# assert run_intcode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(","))
# assert run_intcode("3,3,1105,-1,9,1101,0,0,12,4,12,99,1".split(","))
# assert run_intcode("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(","))


if __name__ == "__main__":
    with open("input", "r") as file:
        mem = file.readline().split(",")
        run_intcode(mem)