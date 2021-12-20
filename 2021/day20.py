
import math

def enhance_image(algorithm, pixels, outside):
    pixel_conversion = {"#": "1", ".":"0"}
    min_x,min_y, = math.inf, math.inf
    max_x,max_y = -math.inf, -math.inf
    for (x,y) in pixels:
        min_x = min(min_x,x)
        min_y = min(min_y,y)
        max_x = max(max_x,x)
        max_y = max(max_y,y)
    enhanced_pixels = dict()
    for (x,y) in pixels:
        # This pixel can update its neighbors so check all neighbors
        neighbors = [(x+dx,y+dy) for dy in range(-1,2) for dx in range(-1,2)]
        for (nx,ny) in neighbors:
            # Skip if already calculated
            if (nx,ny) in enhanced_pixels: continue
            # Determine index
            neighbors_neighbors = [(nx+dx,ny+dy) for dy in range(-1,2) for dx in range(-1,2)]
            index = ""
            for nnx,nny in neighbors_neighbors:
                if nnx < min_x or nnx > max_x:
                    index += pixel_conversion[outside]
                elif nny < min_y or nny > max_y:
                    index += pixel_conversion[outside]
                else:
                    index += pixel_conversion[pixels[nnx,nny]] if (nnx,nny) in pixels else "0"
            tmp = index
            index = int(index,2)
            enhanced_pixels[nx,ny] = algorithm[index]

    return enhanced_pixels


def print_image(pixels):
    min_x,min_y, = math.inf, math.inf
    max_x,max_y = -math.inf, -math.inf
    for x,y in pixels:
        min_x = min(min_x,x)
        min_y = min(min_y,y)
        max_x = max(max_x,x)
        max_y = max(max_y,y)

    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            print(pixels[x,y], end="")
        print()
    print()


def count_lit_pixels(algorithm, _pixels, iterations):
    pixels = _pixels.copy()
    outside = "."
    pixels = enhance_image(algorithm, pixels, outside)
    for i in range(2,iterations+1):
        outside = algorithm[0] if i % 2 == 0 else algorithm[-1]
        pixels = enhance_image(algorithm, pixels, outside)

    res = 0
    for _, pixel in pixels.items():
        if pixel == "#":
            res += 1
    return res

if __name__ == "__main__":
    algorithm = None
    image = []
    with open("input", "r") as file:
        reading_algorithm = True
        for line in file:
            if line == "\n":
                reading_algorithm = False
                continue
            if reading_algorithm:
                algorithm = line.strip()
            else:
                image.append(line.strip())

    pixels = {}
    for y in range(len(image)):
        for x in range(len(image[y])):
            pixels[x,y] = image[y][x]

    # p1
    print(count_lit_pixels(algorithm, pixels, 2))

    # p2
    print(count_lit_pixels(algorithm, pixels, 50))
