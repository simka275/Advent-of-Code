
def flip_tile(tile):
    e, ne = 0, 0
    i = 0
    while i < len(tile):
        if tile[i] == "n":
            if tile[i+1] == "e":
                ne += 1
            elif tile[i+1] == "w":
                e -= 1
                ne += 1
            i += 2
        elif tile[i] == "e":
            e += 1
            i += 1
        elif tile[i] == "s":
            if tile[i+1] == "e":
                e += 1
                ne -= 1
            elif tile[i+1] == "w":
                ne -= 1
            i += 2
        elif tile[i] == "w":
            e -= 1
            i += 1

    return e,ne


def count_black_tiles(tiles):
    black_tiles = set()
    for tile in tiles:
        flipped = flip_tile(tile)
        if flipped in black_tiles:
            black_tiles.remove(flipped)
        else:
            black_tiles.add(flipped)

    return len(black_tiles)


def count_black_neighbors(tile, black_tiles):
    res = 0
    x,y = tile
    # Neighbors:
    # e (x+1,y)
    if (x+1,y) in black_tiles:
        res += 1
    # ne (x,y+1)
    if (x,y+1) in black_tiles:
        res += 1
    # se (x+1,y-1)
    if (x+1,y-1) in black_tiles:
        res += 1
    # w (x-1,y)
    if (x-1,y) in black_tiles:
        res += 1
    # nw (x-1,y+1)
    if (x-1,y+1) in black_tiles:
        res += 1
    # sw (x,y-1)
    if (x,y-1) in black_tiles:
        res += 1
    return res


def tick(tiles, iterations):
    black_tiles = set()
    for tile in tiles:
        flipped = flip_tile(tile)
        if flipped in black_tiles:
            black_tiles.remove(flipped)
        else:
            black_tiles.add(flipped)

    while iterations > 0:
        new_black_tiles = black_tiles.copy()
        # Remove black tiles with 0 or > 2 black neighbors
        for tile in black_tiles:
            black_neighbors = count_black_neighbors(tile, black_tiles)
            if black_neighbors == 0 or black_neighbors > 2:
                new_black_tiles.remove(tile)
        # Add white tiles with 2 black neighbors
        for tile in black_tiles:
            x,y = tile
            neighbor_tiles = [ (x+1,y), (x,y+1), (x+1,y-1), (x-1,y), (x-1,y+1), (x,y-1) ]
            for neighbor in neighbor_tiles:
                if neighbor in black_tiles or neighbor in new_black_tiles:
                    continue
                black_neighbors = count_black_neighbors(neighbor, black_tiles)
                if black_neighbors == 2:
                    new_black_tiles.add(neighbor)
        black_tiles = new_black_tiles
        iterations -= 1
    return len(black_tiles)


if __name__ == "__main__":
    tiles = []
    with open("input", "r") as file:
        for line in file:
            tiles.append(line.rstrip())

    # part 1
    print(count_black_tiles(tiles))
    # parrt 2
    print(tick(tiles, 100))