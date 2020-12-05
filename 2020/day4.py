
def has_valid_fields(passport):
    return "byr:" in passport and \
           "iyr:" in passport and \
           "eyr:" in passport and \
           "hgt:" in passport and \
           "hcl:" in passport and \
           "ecl:" in passport and \
           "pid:" in passport


def count_valid_p1(passports):
    res = 0
    for pp in passports:
        if has_valid_fields(pp):
            res += 1
    return res


def has_valid_values(passport):
    passport = passport.split()
    for field in passport:
        k,v = field.split(":")
        # print("k={}, v={}|||".format(k,v))
        if k == "byr" and not (len(v) == 4 and (1920 <= int(v) <= 2002)):
            return False
        if k == "iyr" and not (len(v) == 4 and (2010 <= int(v) <= 2020)):
            return False
        if k == "eyr" and not (len(v) == 4 and (2020 <= int(v) <= 2030)):
            return False
        if k == "hgt":
            if v[-2:] == "cm" and not (150 <= int(v[:-2]) <= 193):
                return False
            if v[-2:] == "in" and not (59 <= int(v[:-2]) <= 76):
                return False
            if v[-2:] != "cm" and v[-2:] != "in":
                return False
        if k == "hcl":
            if not (v[0] == "#" and len(v) == 7):
                return False
            for c in v[1:]:
                if c not in "abcdef0123456789":
                    return False
        if k == "ecl" and (v not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]):
            return False
        if k == "pid":
            if len(v) != 9:
                return False
            for c in v:
                if c not in "0123456789":
                    return False
    return True


def count_valid_p2(passports):
    res = 0
    for pp in passports:
        if has_valid_fields(pp) and has_valid_values(pp):
            res += 1
    return res


if __name__ == "__main__":
    passports = []
    with open("input", "r") as file:
        passport = ""
        for line in file:
            if not line.rstrip():
                passports.append(passport)
                passport = ""
            else:
                passport += " " + line.rstrip()
        if passport.rstrip():
            passports.append(passport)

    # part 1
    print(count_valid_p1(passports))
    # part 2
    print(count_valid_p2(passports))