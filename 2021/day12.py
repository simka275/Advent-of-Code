
def calc_paths(edges):
    paths = [["start"]]
    complete_paths = []
    while paths:
        path = paths.pop()
        pos = path[-1]
        for next in edges[pos]:
            if next == "end":
                complete_paths.append(path + [next])
            elif next == "start":
                continue
            elif next.isupper():
                paths.append(path + [next])
            elif next.islower() and next not in path:
                paths.append(path + [next])
    return len(complete_paths)


def calc_paths_double_visit(edges):
    double_visit_tag = "doublevisitdone"
    paths = [["start"]]
    complete_paths = []
    while paths:
        path = paths.pop()
        pos = path[-1]
        for next in edges[pos]:
            if next == "end":
                complete_paths.append(path + [next])
            elif next == "start":
                continue
            elif next.isupper():
                paths.append(path + [next])
            elif next.islower() and next not in path:
                paths.append(path + [next])
            elif next.islower() and double_visit_tag not in path:
                paths.append(path + [double_visit_tag, next])
    return len(complete_paths)


if __name__ == "__main__":
    edges = dict()
    with open("input", "r") as file:
        for line in file:
            p1, p2 = line.strip().split("-")
            if p1 in edges:
                edges[p1].append(p2)
            else:
                edges[p1] = [p2]
            if p2 in edges:
                edges[p2].append(p1)
            else:
                edges[p2] = [p1]

    # p1
    print(calc_paths(edges))

    #p2
    print(calc_paths_double_visit(edges))