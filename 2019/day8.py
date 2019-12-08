
import math

def create_layers(data, width, height):
    layers = []
    n_of_layers = len(data) // (width*height)
    for i in range(n_of_layers):
        layer = data[i*width*height:(i+1)*width*height]
        layers.append(layer)
    return layers


def determine_pixel(p1,p2):
    if p1 in "01":
        return p1
    elif p1 in "2":
        return p2
    else:
        raise Exception("Unknown pixel code")


def overlay_layer(l1, l2):
    res = ""
    for p1, p2 in zip(l1, l2):
        res += (determine_pixel(p1,p2))
    return res


def overlay_img(layers):
    img = layers[0]
    for i in range(1,len(layers)):
        img = overlay_layer(img, layers[i])
    return img


def part_one():
    with open("input", "r") as file:
        img = file.readline().strip()
        layers = create_layers(img, 25, 6)

        min_zeroes, min_layer = math.inf, ""
        for layer in layers:
            n_of_zeroes = layer.count("0")
            if n_of_zeroes < min_zeroes:
                min_zeroes = n_of_zeroes
                min_layer = layer
        
        assert min_zeroes < math.inf
        assert min_layer != ""

        print(min_layer.count("1")*min_layer.count("2"))


def part_two():
    with open("input", "r") as file:
        img = file.readline().strip()
        width, height = 25, 6
        layers = create_layers(img, width, height)
        img = overlay_img(layers)

        # Render image
        for y in range(height):
            for x in range(width):
                if img[y*width+x] == "0":
                    print(" ", end="")
                elif img[y*width+x] == "1":
                    print("X", end="")
                else:
                    raise Exception("Unknown pixel code: {}".format(img[y*width+x]))
            print("")



assert create_layers("123456789012", 3, 2) == ["123456", "789012"]

assert overlay_img(create_layers("0222112222120000", 2, 2)) == "0110"

if __name__ == "__main__":
    # part_one()
    part_two()