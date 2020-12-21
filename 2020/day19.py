
def string_to_list_helper(string):
    res = []
    for e in string.split():
        res.append(e)
        res.append(" ")
    return res[:-1]


def earley_parse(rules, word):
    states = []
    for _ in range(len(word)+1):
        states.append([])

    # state = (production/rule being matched, pos in rule being matched, origin pos)
    states[0].append([("0",string_to_list_helper(rules["0"])),0,0])
    for k in range(len(word)):
        i = 0
        while i < len(states[k]):
            state = states[k][i]
            lh = state[0][0]
            rh = state[0][1]
            x = state[2]
            # If finished -> complete state
            if state[1] == len(rh):
                # Completer
                for cs in states[x]:
                    comp_state = cs.copy()
                    comp_pos = comp_state[1]
                    comp_rule = comp_state[0][1]
                    if comp_pos < len(comp_rule) and comp_rule[comp_pos] == lh:
                        comp_state[1] += 1
                        states[k].append((comp_state))
            else:
                cur_pos = state[1]
                cur_char = state[0][1][cur_pos]
                if cur_char.isdigit(): # Non terminal
                    # Predictor
                    rule_list = rules[cur_char].split(" | ")
                    for rule in rule_list:
                        add_state = [(cur_char, string_to_list_helper(rule)),0,k]
                        if not add_state in states[k]:
                            states[k].append([(cur_char, string_to_list_helper(rule)),0,k])
                else:
                    # Scanner
                    if cur_char == word[k]:
                        new_state = state.copy()
                        new_state[1] += 1
                        states[k+1].append(new_state)
            i += 1

    rule = string_to_list_helper(rules["0"])
    # if [("0",rule),len(rule),0] in states[len(word)-1]:
    #     print("{} is a match".format(word))
    return [("0",rule),len(rule),0] in states[len(word)-1]


def verify_messages(rules, messages):
    res = 0
    for message in messages:
        if earley_parse(rules, "".join([x+" " for x in message])):
            res += 1
    return res


if __name__ == "__main__":
    with open("input", "r") as file:
        rules = dict()
        messages = []
        for line in file:
            if line == "\n":
                break
            nr, rule = line.rstrip().split(": ")
            rules[nr] = rule.replace("\"","")

        for line in file:
            messages.append(line.rstrip())

    # part 1
    print(verify_messages(rules, messages))

    # part 2
    rules["8"] = "42 | 42 8"
    rules["11"] = "42 31 | 42 11 31"
    print(verify_messages(rules, messages))