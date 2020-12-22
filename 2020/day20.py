
class Tile:
    def __init__(self, id, tile):
        self.id = id
        self.tile = tile

    def __str__(self):
        res = "Tile {}:\n".format(self.id)
        for row in self.tile:
            res += "".join(row)
            res += "\n"
        return res

    def top(self):
        return "".join(self.tile[0])

    def bottom(self):
        return "".join(self.tile[-1])

    def left(self):
        return "".join([x[0] for x in self.tile])

    def right(self):
        return "".join([x[-1] for x in self.tile])

    # Flip vertical = flip_horizontal + 2*rotate_right
    def flip_horizontal(self):
        self.tile.reverse()

    # Rotate left = 3*rotate_right
    def rotate_right(self):
        res = []
        for row in self.tile:
            res.append(row.copy())
        for y in range(len(self.tile)):
            for x in range(len(self.tile[y])):
                res[x][len(self.tile)-1-y] = self.tile[y][x]
        self.tile = res

    def trim_outer(self):
        res = []
        for y in range(1,len(self.tile)-1):
            row = []
            for x in range(1,len(self.tile[y])-1):
                row.append(self.tile[y][x])
            res.append(row)
        self.tile = res

    def height(self):
        return len(self.tile)

    def row_str(self, row):
        return "".join(self.tile[row])


# Choose tile
# Test every other tile if match by rotate * 4 and flip + rotate * 4
# Below not needed if unique matches
# if match check if edge ok ex. if new tile matches chosen top to bottom
# verify that placing new tile is ok by checking if tile to left or right of new tile
# exist and if exist then must match before placing new tile
def connect_tiles(tiles):
    edges = dict()
    for tile in tiles:
        edges[tile.id] = {"top":"", "bottom":"", "right":"", "left":""}

    placed = [tiles[0]]
    queue = [tiles[0]]
    while queue:
        tile = queue.pop(0)
        # connect with others in placed
        for pot_neighbor in placed:
            if pot_neighbor.id == tile.id:
                continue
            # top
            if tile.top() == pot_neighbor.bottom():
                edges[tile.id]["top"] = pot_neighbor.id
                edges[pot_neighbor.id]["bottom"] = tile.id
            # right
            if tile.right() == pot_neighbor.left():
                edges[tile.id]["right"] = pot_neighbor.id
                edges[pot_neighbor.id]["left"] = tile.id
            # bottom
            if tile.bottom() == pot_neighbor.top():
                edges[tile.id]["bottom"] = pot_neighbor.id
                edges[pot_neighbor.id]["top"] = tile.id
            # left
            if tile.left() == pot_neighbor.right():
                edges[tile.id]["left"] = pot_neighbor.id
                edges[pot_neighbor.id]["right"] = tile.id

        # top
        if not edges[tile.id]["top"]:
            top = tile.top()
            for new_tile in tiles:
                tile_placed = False
                if new_tile in placed:
                    continue
                for _ in range(4):
                    if top == new_tile.bottom():
                        placed.append(new_tile)
                        queue.append(new_tile)
                        edges[tile.id]["top"] = new_tile.id
                        edges[new_tile.id]["bottom"] = tile.id
                        tile_placed = True
                        break
                    new_tile.rotate_right()
                if tile_placed:
                    break
                new_tile.flip_horizontal()
                for _ in range(4):
                    if top == new_tile.bottom():
                        placed.append(new_tile)
                        queue.append(new_tile)
                        edges[tile.id]["top"] = new_tile.id
                        edges[new_tile.id]["bottom"] = tile.id
                        tile_placed = True
                        break
                    new_tile.rotate_right()
                if tile_placed:
                    break
        # right
        if not edges[tile.id]["right"]:
            right = tile.right()
            for new_tile in tiles:
                tile_placed = False
                if new_tile in placed:
                    continue
                for _ in range(4):
                    if right == new_tile.left():
                        placed.append(new_tile)
                        queue.append(new_tile)
                        edges[tile.id]["right"] = new_tile.id
                        edges[new_tile.id]["left"] = tile.id
                        tile_placed = True
                        break
                    new_tile.rotate_right()
                if tile_placed:
                    break
                new_tile.flip_horizontal()
                for _ in range(4):
                    if right == new_tile.left():
                        placed.append(new_tile)
                        queue.append(new_tile)
                        edges[tile.id]["right"] = new_tile.id
                        edges[new_tile.id]["left"] = tile.id
                        tile_placed = True
                        break
                    new_tile.rotate_right()
                if tile_placed:
                    break
        # bottom
        if not edges[tile.id]["bottom"]:
            bottom = tile.bottom()
            for new_tile in tiles:
                tile_placed = False
                if new_tile in placed:
                    continue
                for _ in range(4):
                    if bottom == new_tile.top():
                        placed.append(new_tile)
                        queue.append(new_tile)
                        edges[tile.id]["bottom"] = new_tile.id
                        edges[new_tile.id]["top"] = tile.id
                        tile_placed = True
                        break
                    new_tile.rotate_right()
                if tile_placed:
                    break
                new_tile.flip_horizontal()
                for _ in range(4):
                    if bottom == new_tile.top():
                        placed.append(new_tile)
                        queue.append(new_tile)
                        edges[tile.id]["bottom"] = new_tile.id
                        edges[new_tile.id]["top"] = tile.id
                        tile_placed = True
                        break
                    new_tile.rotate_right()
                if tile_placed:
                    break
        # left
        if not edges[tile.id]["left"]:
            left = tile.left()
            for new_tile in tiles:
                tile_placed = False
                if new_tile in placed:
                    continue
                for _ in range(4):
                    if left == new_tile.right():
                        placed.append(new_tile)
                        queue.append(new_tile)
                        edges[tile.id]["left"] = new_tile.id
                        edges[new_tile.id]["right"] = tile.id
                        tile_placed = True
                        break
                    new_tile.rotate_right()
                if tile_placed:
                    break
                new_tile.flip_horizontal()
                for _ in range(4):
                    if left == new_tile.right():
                        placed.append(new_tile)
                        queue.append(new_tile)
                        edges[tile.id]["left"] = new_tile.id
                        edges[new_tile.id]["right"] = tile.id
                        tile_placed = True
                        break
                    new_tile.rotate_right()
                if tile_placed:
                    break

    # for edge in edges:
    #     print("{}:".format(edge))
    #     print(edges[edge])

    res = 1
    for tid in edges:
        n_of_paths = 0
        for _,value in edges[tid].items():
            if value:
                n_of_paths += 1
        if n_of_paths == 2: # corner tile
            res *= int(tid)
    return res, placed, edges


def monster_track(tiles, edges):
    # trim borders
    for tile in tiles:
        tile.trim_outer()

    # find topleft
    for tile_id, edge in edges.items():
        if not edge["left"] and not edge["top"]:
            topleft_id = tile_id
            break

    current_id = topleft_id
    row = 0
    tiles_pos = []
    while current_id:
        # travel all the way to the right
        tiles_pos.append([])
        tmp_id = current_id
        while tmp_id:
            tiles_pos[row].append(tmp_id)
            tmp_id = edges[tmp_id]["right"]
        # step down one
        current_id = edges[current_id]["bottom"]
        row += 1

    # combine
    mega_tile = []
    for _ in range(tiles[0].height()*len(tiles_pos)):
        mega_tile.append([])
    for row in range(len(tiles_pos)):
        for tile_id in tiles_pos[row]:
            # find current tile
            for tile in tiles:
                if tile_id == tile.id:
                    break
            for y in range(len(tile.tile)):
                mega_tile[row*tile.height() + y] += tile.tile[y].copy()

    mega_tile = Tile(0, mega_tile)

    # find monsters
    for _ in range(4):
        mark_monster(mega_tile)
        mega_tile.rotate_right()
    mega_tile.flip_horizontal()
    for _ in range(4):
        mark_monster(mega_tile)
        mega_tile.rotate_right()

    # mega_tile.flip_horizontal()
    # mega_tile.rotate_right()
    # print(mega_tile)

    # calc water roughness
    res = 0
    for y in range(len(mega_tile.tile)):
        for x in range(len(mega_tile.tile[y])):
            if mega_tile.tile[y][x] == "#":
                res += 1
    return res


def mark_monster(tile):
    monster_pattern = []
    monster_pattern.append([18])
    monster_pattern.append([0,5,6,11,12,17,18,19])
    monster_pattern.append([1,4,7,10,13,16])
    for y in range(tile.height()-2):
        for x in range(len(tile.tile[y])-monster_pattern[0][0]):
            if tile.tile[y][x+monster_pattern[0][0]] == "#": # potential monster eye
                found = True
                for dy in range(1,len(monster_pattern)):
                    for dx in monster_pattern[dy]:
                        if tile.tile[y+dy][x+dx] != "#":
                            found = False
                            break
                    if not found:
                        break

                if found:
                    tile.tile[y][x+monster_pattern[0][0]] = "O"
                    for dy in range(1,len(monster_pattern)):
                        for dx in monster_pattern[dy]:
                            tile.tile[y+dy][x+dx] = "O"


if __name__ == "__main__":
    tiles = []
    with open("input", "r") as file:
        nr = ""
        tile = []
        for line in file:
            line = line.rstrip()
            if "Tile" in line:
                _, nr = line.split()
                nr = nr[:-1]
                tile = []
            elif line:
                tile.append([x for x in line])
            else:
                tiles.append(Tile(nr, tile))
        tiles.append(Tile(nr, tile))

    v, completed, edges = connect_tiles(tiles)
    # part 1
    print(v)
    # part 2
    print(monster_track(completed, edges))
