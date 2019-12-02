

def run_intcode(instructions, noun, verb):
    instruction_p = 0
    instructions[1] = noun
    instructions[2] = verb

    while instructions[instruction_p] != 99:
        # Addition
        if instructions[instruction_p] == 1:
            instructions[instructions[instruction_p+3]] = instructions[instructions[instruction_p+1]] + instructions[instructions[instruction_p+2]]
        # Multiplication
        elif instructions[instruction_p] == 2:
            instructions[instructions[instruction_p+3]] = instructions[instructions[instruction_p+1]] * instructions[instructions[instruction_p+2]]
        
        instruction_p += 4
    
    return instructions[0]


# def reverse_intcode(instructions):
# def extended_gcd(a,b):
#     x,y, u,v = 0,1, 1,0
#     while a != 0:
#         q, r = b//a, b%a
#         m, n = x-u*q, y-v*q
#         b,a, x,y, u,v = a,r, u,v, m,n
#     g = b
#     return g, x, y


# def solve_dio(a, b, c):
#     g, x, y = extended_gcd(a,b)
#     return x*c/g, y*c/g


def brute_force_sigh(instructions, goal):
    for noun in range(0,100):
        for verb in range(0,50):
            if run_intcode(instructions.copy(), noun, verb) == goal:
                return noun, verb
    raise Exception("No noun verb combo found for goal=", goal)


def part_one():
    with open("input", "r") as file:
        instructions = [ int(x) for x in file.readline().split(",") ]
        run_intcode(instructions, 12, 2)
        print(instructions[0])


def part_two():
    with open("input", "r") as file:
        instructions = [ int(x) for x in file.readline().split(",") ]
        
        # c = a*x + b*y
        # a = run_intcode(instructions.copy(), 1, 0) - run_intcode(instructions.copy(), 0, 0)
        # b = run_intcode(instructions.copy(), 0, 1) - run_intcode(instructions.copy(), 0, 0)
        # noun, verb = solve_dio(a, b, c=19690720)

        noun, verb = brute_force_sigh(instructions, 19690720)
        print(noun*100+verb)
        print(run_intcode(instructions, noun, verb))


if __name__ == "__main__":
    # part_one()
    part_two()