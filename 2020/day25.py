
def transform(goal):
    i = 1
    value = 1
    while True:
        value = (value * 7) % 20201227
        if value == goal:
            break
        i += 1
    return i


def generate_key(subject, iterations):
    value = 1
    for _ in range(iterations):
        value = (value * subject) % 20201227
    return value


if __name__ == "__main__":
    with open("input", "r") as file:
        pub_key1 = int(file.readline().rstrip())
        pub_key2 = int(file.readline().rstrip())

    print(generate_key(pub_key2, transform(pub_key1)))

