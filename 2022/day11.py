
import re
import copy

def part_one(monkeys):
    monkeys = copy.deepcopy(monkeys)
    for _ in range(20):
        for monkey in monkeys:
            items = monkeys[monkey]["items"]
            operation = monkeys[monkey]["operation"]
            test = monkeys[monkey]["test"]
            success_monkey = monkeys[monkey]["test_success"]
            fail_monkey = monkeys[monkey]["test_fail"]
            for item in items:
                monkeys[monkey]["inspection_count"] += 1
                worry = eval(operation.replace("old", str(item)))
                worry = worry // 3
                if worry % test == 0:
                    monkeys[success_monkey]["items"].append(worry)
                else:
                    monkeys[fail_monkey]["items"].append(worry)
            monkeys[monkey]["items"] = []

    inspections = []
    for monkey in monkeys:
        inspections.append(monkeys[monkey]["inspection_count"])
    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


def part_two(monkeys):
    monkeys = copy.deepcopy(monkeys)
    divisor = 1
    for monkey in monkeys:
        divisor *= monkeys[monkey]["test"]
    for _ in range(10000):
        for monkey in monkeys:
            items = monkeys[monkey]["items"]
            operation = monkeys[monkey]["operation"]
            test = monkeys[monkey]["test"]
            success_monkey = monkeys[monkey]["test_success"]
            fail_monkey = monkeys[monkey]["test_fail"]
            for item in items:
                monkeys[monkey]["inspection_count"] += 1
                worry = eval(operation.replace("old", str(item)))
                worry = worry % divisor
                if worry % test == 0:
                    monkeys[success_monkey]["items"].append(worry)
                else:
                    monkeys[fail_monkey]["items"].append(worry)
            monkeys[monkey]["items"] = []

    inspections = []
    for monkey in monkeys:
        inspections.append(monkeys[monkey]["inspection_count"])
    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


if __name__ == "__main__":
    monkeys = dict()
    with open("input", "r") as fd:
        current_monkey = None
        for line in fd:
            match = re.match(r'Monkey (\d+):', line)
            if match:
                current_monkey = int(match.groups()[0])
                monkeys[current_monkey] = {"items": [], "operation": "", "test": None, "test_success": None, "test_fail": None, "inspection_count": 0}

            match = re.match(r'  Starting items: ', line)
            if match:
                monkeys[current_monkey]["items"] = [int(x) for x in line.strip().split("Starting items: ")[1].split(", ")]

            match = re.match(r'  Operation: new = ', line)
            if match:
                monkeys[current_monkey]["operation"] = line.strip().split("Operation: new = ")[1]

            match = re.match(r'  Test: divisible by (\d+)', line)
            if match:
                monkeys[current_monkey]["test"] = int(match.groups()[0])

            match = re.match(r'    If true: throw to monkey (\d+)', line)
            if match:
                monkeys[current_monkey]["test_success"] = int(match.groups()[0])

            match = re.match(r'    If false: throw to monkey (\d+)', line)
            if match:
                monkeys[current_monkey]["test_fail"] = int(match.groups()[0])

    print(part_one(monkeys))

    print(part_two(monkeys))