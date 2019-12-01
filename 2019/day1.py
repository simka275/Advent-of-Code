
def part_one():
    fuel_req_sum = 0
    with open("input", "r") as file:
        for line in file:
            fuel_req_sum += int(line) // 3 -2 
    
    print(fuel_req_sum)

def calc_fuel(mass):
    fuel = mass // 3 -2
    if fuel <= 0:
        return 0
    else:
        return fuel + calc_fuel(fuel)

def part_two():
    fuel_req_sum = 0
    with open("input", "r") as file:
        for line in file:
            fuel_req_sum += calc_fuel(int(line))
    
    print(fuel_req_sum)

if __name__ == "__main__":
    # part_one()
    part_two()