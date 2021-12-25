
from queue import PriorityQueue
from time import perf_counter

def organize_shrimps(_shrimps, bucket_size = 2):
    shrimps = _shrimps.copy()
    move_costs = {"A":1, "B":10, "C":100, "D":1000}
    home_bucket_x = {"A":3, "B":5, "C":7, "D":9}
    pqueue = PriorityQueue()
    visited = dict()
    pqueue.put((0,shrimps))

    def occupied(pos, shrimps):
        for other in shrimps:
            if pos == (other[0],other[1]):
                return other[2]
        return None

    def is_finished(shrimps):
        for (x,y, shrimp_type) in shrimps:
            if y == 0 or x != home_bucket_x[shrimp_type]: return False
        return True

    assert(is_finished([(3, 1, 'A'), (5, 1, 'B'), (7, 1, 'C'), (9, 1, 'D'), (3, 2, 'A'), (5, 2, 'B'), (7, 2, 'C'), (9, 2, 'D')]))

    def in_correct_spot(shrimp, shrimps): # True if pos in bucket below y are correct
        x,y,shrimp_type = shrimp
        if x == home_bucket_x[shrimp_type]:
            for yy in range(y+1,bucket_size+1):
                if occupied((x,yy), shrimps) != shrimp_type:
                    return False
            return True
        return False

    if bucket_size == 2:
        assert(in_correct_spot((3, 1, 'A'), [(3, 1, 'A'), (5, 1, 'B'), (7, 1, 'C'), (9, 1, 'D'), (3, 2, 'A'), (5, 2, 'B'), (7, 2, 'C'), (9, 2, 'D')]))
        assert(not in_correct_spot((2, 0, 'A'), [(2, 0, 'A'), (5, 1, 'B'), (7, 1, 'C'), (9, 1, 'D'), (3, 2, 'A'), (5, 2, 'B'), (7, 2, 'C'), (9, 2, 'D')]))
        assert(not in_correct_spot((3, 1, 'A'), [(3, 1, 'A'), (5, 1, 'B'), (7, 1, 'C'), (9, 1, 'D'), (3, 2, 'D'), (5, 2, 'B'), (7, 2, 'C'), (9, 2, 'A')]))

    def get_bucket_pos(shrimp_type, shrimps): # Get available bucket pos for given type
        x = home_bucket_x[shrimp_type]
        for y in range(bucket_size,0,-1):
            if not occupied((x,y), shrimps):
                return (x,y)
            if occupied((x,y), shrimps) != shrimp_type:
                break
        return None

    if bucket_size == 2:
        assert(get_bucket_pos("A", [(2, 0, 'A'), (5, 1, 'B'), (7, 1, 'C'), (9, 1, 'D'), (3, 2, 'A'), (5, 2, 'B'), (7, 2, 'C'), (9, 2, 'D')]) == (3,1))
        assert(get_bucket_pos("A", [(2, 0, 'A'), (5, 1, 'B'), (7, 1, 'C'), (9, 1, 'D'), (3, 2, 'D'), (5, 2, 'B'), (7, 2, 'C'), (9, 2, 'A')]) == None)

    def can_exit_bucket(pos, shrimps):
        x,y = pos
        for yy in range(y-1,0,-1):
            if occupied((x,yy), shrimps):
                return False
        return True

    if bucket_size == 2:
        assert(not can_exit_bucket((3, 2), [(3, 1, 'A'), (5, 1, 'B'), (7, 1, 'C'), (9, 1, 'D'), (3, 2, 'A'), (5, 2, 'B'), (7, 2, 'C'), (9, 2, 'D')]))
        assert(can_exit_bucket((3, 2), [(2, 0, 'A'), (5, 1, 'B'), (7, 1, 'C'), (9, 1, 'D'), (3, 2, 'A'), (5, 2, 'B'), (7, 2, 'C'), (9, 2, 'D')]))

    while not pqueue.empty():
        cost, shrimps = pqueue.get()
        if is_finished(shrimps):
            return cost

        if tuple(shrimps) in visited and visited[tuple(shrimps)] <= cost:
            continue

        visited[tuple(shrimps)] = cost

        for i in range(len(shrimps)):
            x,y,shrimp_type = shrimps[i]

            if in_correct_spot(shrimps[i], shrimps): continue

            if y == 0: # In the corridor
                goal_pos = get_bucket_pos(shrimp_type, shrimps)
                if not goal_pos: continue
                new_x, new_y = goal_pos[0], goal_pos[1]
                path = [(sx,0) for sx in range(x+1,new_x+1)] if x < new_x else [(sx,0) for sx in range(x-1,new_x-1,-1)]
                if not all(not occupied(step, shrimps) for step in path): continue # A spot between shrimp and goal is occupied
                for yy in range(1,new_y+1):
                    path.append((new_x,yy))
                pqueue.put((cost + move_costs[shrimp_type]*len(path), shrimps[:i] + [(new_x,new_y,shrimp_type)] + shrimps[i+1:]))
            else: # In a bucket
                if not can_exit_bucket((x,y),shrimps): continue

                up_path = []
                for yy in range(y-1,0,-1):
                    up_path.append((x,yy))

                # Left
                left_path = []
                for new_x in range(x,0,-1):
                    if occupied((new_x,0), shrimps): break
                    left_path.append((new_x,0))
                for j in range(len(left_path)):
                    new_x, new_y = left_path[j]
                    if new_x in [3,5,7,9]: continue
                    cur_path = up_path + left_path[:j+1]
                    pqueue.put((cost + move_costs[shrimp_type]*len(cur_path), shrimps[:i] + [(new_x,new_y,shrimp_type)] + shrimps[i+1:]))

                # Right
                right_path = []
                for new_x in range(x,12):
                    if occupied((new_x,0), shrimps): break
                    right_path.append((new_x,0))
                for j in range(len(right_path)):
                    new_x, new_y = right_path[j]
                    if new_x in [3,5,7,9]: continue
                    cur_path = up_path + right_path[:j+1]
                    pqueue.put((cost + move_costs[shrimp_type]*len(cur_path), shrimps[:i] + [(new_x,new_y,shrimp_type)] + shrimps[i+1:]))


# assert(organize_shrimps([(3, 1, 'B'), (5, 1, 'C'), (7, 1, 'B'), (9, 1, 'D'), (3, 2, 'A'), (5, 2, 'D'), (7, 2, 'C'), (9, 2, 'A')]) == 12521)

# assert(organize_shrimps([(3, 1, 'B'), (5, 1, 'C'), (7, 1, 'B'), (9, 1, 'D'), (3, 2, 'D'), (5, 2, 'C'), (7, 2, 'B'), (9, 2, 'A'), (3, 3, 'D'), (5, 3, 'B'), (7, 3, 'A'), (9, 3, 'C'), (3, 4, 'A'), (5, 4, 'D'), (7, 4, 'C'), (9, 4, 'A')], 4) == 44169)


if __name__ == "__main__":
    shrimps = []
    with open("input", "r") as file:
        file.readline()
        file.readline()
        layer_1 = file.readline().strip()[3:-3].split("#")
        shrimps.append((3,1,layer_1[0]))
        shrimps.append((5,1,layer_1[1]))
        shrimps.append((7,1,layer_1[2]))
        shrimps.append((9,1,layer_1[3]))

        layer_2 = file.readline().strip()[1:-1].split("#")
        shrimps.append((3,2,layer_2[0]))
        shrimps.append((5,2,layer_2[1]))
        shrimps.append((7,2,layer_2[2]))
        shrimps.append((9,2,layer_2[3]))

        line = file.readline()
        if line.count("#") < 6: # 4 rows
            layer_3 = line.strip()[1:-1].split("#")
            shrimps.append((3,3,layer_3[0]))
            shrimps.append((5,3,layer_3[1]))
            shrimps.append((7,3,layer_3[2]))
            shrimps.append((9,3,layer_3[3]))

            layer_4 = file.readline().strip()[1:-1].split("#")
            shrimps.append((3,4,layer_4[0]))
            shrimps.append((5,4,layer_4[1]))
            shrimps.append((7,4,layer_4[2]))
            shrimps.append((9,4,layer_4[3]))

    # p1
    # print(organize_shrimps(shrimps))

    # p2
    start = perf_counter()
    print(organize_shrimps(shrimps,4))
    stop = perf_counter()
    print("Elapsed time: ", stop-start)