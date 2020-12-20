
def parse_expression(expression):
    res = []
    tmp = ""
    for c in expression:
        if c == "+" or c == "*" or c == "(" or (c == ")" and not tmp):
            res.append(c)
        elif c == ")" and tmp:
            res.append(int(tmp))
            tmp = ""
            res.append(c)
        elif c != " ":
            tmp += c
        elif c == " " and tmp:
            res.append(int(tmp))
            tmp = ""
    if tmp:
        res.append(int(tmp))
    return res


def calc_p1(stack):
    while len(stack) > 1:
        lh = stack.pop()
        if lh == "(":
            paran = []
            par_depth = 0
            while True:
                r = stack.pop()
                if r == ")" and par_depth == 0:
                    stack.append(calc_p1(paran))
                    break
                elif r == ")":
                    par_depth -= 1
                    paran.insert(0,r)
                elif r == "(":
                    par_depth += 1
                    paran.insert(0,r)
                else:
                    paran.insert(0,r)
            continue

        op = stack.pop()
        rh = stack.pop()
        if rh == "(":
            paran = []
            par_depth = 0
            while True:
                r = stack.pop()
                if r == ")" and par_depth == 0:
                    stack.append(calc_p1(paran))
                    stack.append(op)
                    stack.append(lh)
                    break
                elif r == ")":
                    par_depth -= 1
                    paran.insert(0,r)
                elif r == "(":
                    par_depth += 1
                    paran.insert(0,r)
                else:
                    paran.insert(0,r)
            continue

        if op == "+":
            stack.append(lh+rh)
        if op == "*":
            stack.append(lh*rh)

    return stack.pop()

exp1 = parse_expression("1 + 2 * 3 + 4 * 5 + 6")
exp1.reverse()
assert(calc_p1(exp1) == 71)
exp2 = parse_expression("1 + (2 * 3) + (4 * (5 + 6))")
exp2.reverse()
assert(calc_p1(exp2) == 51)
exp3 = parse_expression("2 * 3 + (4 * 5)")
exp3.reverse()
assert(calc_p1(exp3) == 26)
exp4 = parse_expression("5 + (8 * 3 + 9 + 3 * 4 * 3)")
exp4.reverse()
assert(calc_p1(exp4) == 437)
exp5 = parse_expression("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
exp5.reverse()
assert(calc_p1(exp5) == 12240)
exp6 = parse_expression("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
exp6.reverse()
assert(calc_p1(exp6) == 13632)


def p1(expressions):
    res = 0
    for exp in expressions:
        stack = parse_expression(exp)
        stack.reverse()
        res += calc_p1(stack)
    return res


def calc_p2(exp):
    while True:
        # remove ()
        if "(" in exp:
            par_depth = 0
            start_i = exp.index("(")
            stop_i = 0
            for i in range(start_i+1,len(exp)):
                if exp[i] == ")" and par_depth == 0:
                    stop_i = i
                    break
                elif exp[i] == "(":
                    par_depth += 1
                elif exp[i] == ")":
                    par_depth -= 1
            exp = exp[:start_i] + [calc_p2(exp[start_i+1:stop_i])] + exp[stop_i+1:]
        # addtion prio
        elif "+" in exp:
            op_i = exp.index("+")
            lh = exp[op_i-1]
            rh = exp[op_i+1]
            exp = exp[:op_i-1] + [lh+rh] + exp[op_i+2:]

        elif "*" in exp:
            op_i = exp.index("*")
            lh = exp[op_i-1]
            rh = exp[op_i+1]
            exp = exp[:op_i-1] + [lh*rh] + exp[op_i+2:]

        else:
            return exp[0]


exp1 = parse_expression("1 + 2 * 3 + 4 * 5 + 6")
assert(calc_p2(exp1) == 231)
exp2 = parse_expression("1 + (2 * 3) + (4 * (5 + 6))")
assert(calc_p2(exp2) == 51)
exp3 = parse_expression("2 * 3 + (4 * 5)")
assert(calc_p2(exp3) == 46)
exp4 = parse_expression("5 + (8 * 3 + 9 + 3 * 4 * 3)")
assert(calc_p2(exp4) == 1445)
exp5 = parse_expression("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
assert(calc_p2(exp5) == 669060)
exp6 = parse_expression("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
assert(calc_p2(exp6) == 23340)


def p2(expressions):
    res = 0
    for exp in expressions:
        res += calc_p2(parse_expression(exp))
    return res

if __name__ == "__main__":
    with open("input", "r") as file:
        expressions = [line.rstrip() for line in file]

    # part 1
    print(p1(expressions))

    # part 2
    print(p2(expressions))

