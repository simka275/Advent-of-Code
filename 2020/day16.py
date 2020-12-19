
def valid_value(fields, value):
    for _,v in fields.items():
        for r in v:
            if r[0] <= value <= r[1]:
                return True
    return False


def invalid_values(fields, tickets):
    res = 0
    for ticket in tickets:
        for value in ticket:
            if not valid_value(fields, value):
                res += value
    return res


def field_find(fields, my_ticket, tickets):
    # Remove invalid tickets
    valid_tickets = []
    for ticket in tickets:
        valid = True
        for value in ticket:
            if not valid_value(fields, value):
                valid = False
                break
        if valid:
            valid_tickets.append(ticket)

    # Use list of columns instead if list of rows (tickets)
    columns = []
    for i in range(len(valid_tickets[0])):
        columns.append([row[i] for row in valid_tickets])

    # for every field
    field_pos = dict()
    for f, rs in fields.items():
        # check if column in ticket array have no invalid value
        field_pos[f] = []
        for i in range(len(columns)):
            valid_column = True
            for v in columns[i]:
                if not ((rs[0][0] <= v <= rs[0][1]) or (rs[1][0] <= v <= rs[1][1])):
                    valid_column = False
                    break
            if valid_column:
                field_pos[f].append(i)

    # iterate over potential field pos and remove if used by other field
    valid_field_pos = dict()
    while field_pos:
        # find a field wiht only one possible column
        for field in field_pos:
            if len(field_pos[field]) == 1:
                current_column = field_pos.pop(field)[0]
                valid_field_pos[field] = current_column
                break
        # remove this column value from every other list of possibles
        for field in field_pos:
            if current_column in field_pos[field]:
                field_pos[field].remove(current_column)

    # mult departure fields
    res = 1
    for field,pos in valid_field_pos.items():
        if field.find("departure") == 0:
            res *= my_ticket[pos]

    return res


if __name__ == "__main__":
    fields = dict()
    my_ticket = []
    tickets = []
    with open("input", "r") as file:
        while True:
            field = file.readline()
            if field == "\n":
                break
            name, rest = field.split(":")
            first, second = rest.strip().split(" or ")
            n1,n2 = first.split("-")
            n3,n4 = second.split("-")
            fields[name] = [(int(n1), int(n2)), (int(n3), int(n4))]

        file.readline()
        my_ticket = [int(x) for x in file.readline().rstrip().split(",")]

        file.readline()
        file.readline()
        for ticket in file:
            tickets.append([int(x) for x in ticket.rstrip().split(",")])

    # part 1
    print(invalid_values(fields, tickets))

    # part 2
    print(field_find(fields, my_ticket, tickets))