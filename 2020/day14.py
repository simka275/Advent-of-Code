
import queue


def mask_memory_p1(mask, pos_nrs_pairs, memory):
    for pn in pos_nrs_pairs:
        res = pn[1]
        # or 1s
        or_mask = int(mask.replace("X","0"), 2)
        res = res | or_mask
        # and 0s
        and_mask = int(mask.replace("X","1"), 2)
        res = res & and_mask
        memory[pn[0]] = res


def part_one():
    memory = dict()
    with open("input", "r") as file:
        pos_nrs_pairs = []
        cur_mask = ""
        for line in file:
            first, second = line.rstrip().split(" = ")
            if first == "mask":
                mask_memory_p1(cur_mask, pos_nrs_pairs, memory)
                pos_nrs_pairs.clear()
                cur_mask = second
            else:
                pos_nrs_pairs.append( (int(first[4:][:-1]), int(second)) )
        mask_memory_p1(cur_mask, pos_nrs_pairs, memory)

    # part 1
    res = 0
    for _,v in memory.items():
        res += v
    print(res)


def mask_memory_p2(mask, pos_nrs_pairs, memory):
    for pn in pos_nrs_pairs:
        addr = bin(pn[0])[2:].zfill(len(mask))
        masked_addr = ""
        for i in range(len(mask)):
            if mask[i] == "0":
                masked_addr = masked_addr + addr[i]
            else:
                masked_addr = masked_addr + mask[i]

        addresses = []
        q = [masked_addr]
        while q:
            addr = q.pop()
            pos = addr.find("X")
            if pos == -1:
                addresses.append(int(addr,2))
            else:
                q.append(addr[:pos] + "0" + addr[pos+1:])
                q.append(addr[:pos] + "1" + addr[pos+1:])

        for addr in addresses:
            memory[addr] = pn[1]


def part_two():
    memory = dict()
    with open("input", "r") as file:
        pos_nrs_pairs = []
        cur_mask = ""
        for line in file:
            first, second = line.rstrip().split(" = ")
            if first == "mask":
                mask_memory_p2(cur_mask, pos_nrs_pairs, memory)
                pos_nrs_pairs.clear()
                cur_mask = second
            else:
                pos_nrs_pairs.append( (int(first[4:][:-1]), int(second)) )
        mask_memory_p2(cur_mask, pos_nrs_pairs, memory)

    res = 0
    for _,v in memory.items():
        res += v
    print(res)


if __name__ == "__main__":
    part_one()
    part_two()


