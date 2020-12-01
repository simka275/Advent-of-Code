
def find_mult_of_ok_sum(numbers):
    for i in range(len(numbers)-1):
        for j in range(i+1,len(numbers)):
            if numbers[i] + numbers[j] == 2020:
                return numbers[i] * numbers[j]


def find_mult_of_ok_sum_3(numbers):
    for i in range(len(numbers)-2):
        for j in range(i+1,len(numbers)-1):
            for k in range(j+1,len(numbers)):
                if numbers[i] + numbers[j] + numbers[k] == 2020:
                    return numbers[i] * numbers[j] * numbers[k]


if __name__ == "__main__":
    with open("input", "r") as file:
        numbers = []
        for line in file:
            numbers.append(int(line))

    # part 1
    print(find_mult_of_ok_sum(numbers))
    # part 2
    print(find_mult_of_ok_sum_3(numbers))
