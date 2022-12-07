

def build_filesystem(lines):
    filesystem = dict()
    path = ""
    for line in lines:
        if "$ cd " == line[:5]:
            cur_dir = line[5:]
            if not path:
                path = cur_dir
            elif cur_dir == "..":
                path = path[:path.rfind("/")] if path.count("/") != 1 else "/"
            else:
                path = path + "/" + cur_dir if path != "/" else path + cur_dir
            if path not in filesystem:
                filesystem[path] = []
        elif "$ ls" == line[:4]:
            pass
        elif "dir " == line[:4]:
            filesystem[path].append([line[4:]])
        else:
            filesystem[path].append(line.split(" "))
    return filesystem


def calculate_dir_size(path, filesystem, sizes):
    res = 0
    for entry in filesystem[path]:
        if len(entry) == 1:
            dir = entry[0]
            new_path = path + "/" + dir if path != "/" else path + dir
            res += sizes[new_path] if new_path in sizes else calculate_dir_size(new_path, filesystem, sizes)
        else:
            size, _ = entry
            res += int(size)
    sizes[path] = res
    return res

def calculate_dir_sizes(filesystem):
    sizes = dict()
    calculate_dir_size("/", filesystem, sizes)
    return sizes


def part_one(filesystem):
    res = 0
    for _, size in calculate_dir_sizes(filesystem).items():
        if size <= 100000:
            res += size
    return res


def part_two(filesystem):
    sizes = calculate_dir_sizes(filesystem)
    tot_capacity = 70000000
    target_unused = 30000000
    used = sizes["/"]
    dir_to_delete = "/"
    for path, size in sizes.items():
        if tot_capacity - used + size < target_unused:
            continue
        if size < sizes[dir_to_delete]:
            dir_to_delete = path
    return sizes[dir_to_delete]


if __name__ == "__main__":
    filesystem = None
    with open("input", "r") as fd:
        filesystem = build_filesystem([line.strip() for line in fd])

    print(part_one(filesystem))

    print(part_two(filesystem))