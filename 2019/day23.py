
import queue

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




if __name__ == "__main__":
    with open("input", "r") as file:
        program = file.readline().strip().split(",")

        process_queue = queue.Queue()
        processes = frozenset(range(50))
        idle_processes = set()
        msgs = dict()
        nat_buffer = []
        ps_count = 50
        for addr in range(ps_count):
            process_queue.put((IntcodeProcess(program),addr,addr,0))
            msgs[addr] = queue.Queue()
        
        # while not nat_buffer: # part one
        while True:
            #
            if idle_processes == processes:
                if len(nat_buffer) > 1 and nat_buffer[-1] == nat_buffer[-2]:
                    print(nat_buffer[-1])
                    break
                elif msgs[0].empty():
                    msgs[0].put(nat_buffer[-1])

            #
            p, addr, arg, idle_counter = process_queue.get()
            ret = p.Run(arg)

            # pkt out
            if p.exit_code == 1:
                dst = ret
                x = p.Run()
                y = p.Run()
                # print("#{} -> #{}: ({}, {})".format(addr,dst,x,y))
                # write to NAT
                if dst == 255:
                    if len(nat_buffer) > 1:
                        nat_buffer.pop(0)
                    nat_buffer.append((x,y))
                # network message
                elif dst not in msgs:
                    msgs[dst] = queue.Queue()    
                    msgs[dst].put((x,y))
                else:
                    msgs[dst].put((x,y))
                process_queue.put((p,addr,None,0))
                # No longer idle
                if addr in idle_processes:
                    idle_processes.remove(addr)
            # pkt in 
            elif p.exit_code == 2:
                if msgs[addr].empty():
                    process_queue.put((p, addr, -1, idle_counter+1))
                    # Process is idle
                    if idle_counter > 10:
                        idle_processes.add(addr)
                else:
                    x,y = msgs[addr].get()
                    # print("#{} <- ?: ({}, {})".format(addr,x,y))
                    p.Run(x)
                    process_queue.put((p,addr,y, 0))
                    # No longer idle
                    if addr in idle_processes:
                        idle_processes.remove(addr)

        print(nat_buffer)