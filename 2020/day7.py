
def parse_rules(rule):
    bag, rest = line.split(" bags contain ")
    bag_rules = {}
    content_rules = rest.split(",")
    for rule in content_rules:
        count = rule.split()[0]
        if count == "no":
            continue
        adjective = rule.split()[1]
        color = rule.split()[2]
        bag_rules["{} {}".format(adjective, color)] =  int(count)
    return bag, bag_rules


def rev_graph(rules):
    res = {}
    for bag in rules.keys():
        res[bag] = []
        for parent, rule in rules.items():
            if bag in rule:
                res[bag].append(parent)
    return res


def trav_up(node, graph):
    if not graph[node]:
        return set({node})
    res = set()
    for parent in graph[node]:
        res = res.union({parent}).union(trav_up(parent, graph))
    return res


def trav_down(node, graph):
    if not graph[node]:
        return 1
    res = 0
    for child, count in graph[node].items():
        res += count * trav_down(child, graph)
    return res+1


if __name__ == "__main__":
    bag_rules = {}
    with open("input", "r") as file:
        for line in file:
            bag, rules = parse_rules(line)
            bag_rules[bag] = rules

    # part 1
    print(len(trav_up("shiny gold", rev_graph(bag_rules))))
    # part 2
    print(trav_down("shiny gold", bag_rules)-1) # -1 because you get nr of bags including gold

