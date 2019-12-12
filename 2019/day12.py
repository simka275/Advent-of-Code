
def gcd(a, b):
    if b==0:
        return a
    else:
        return gcd(b, a%b)


def lcm(a, b):
    g = gcd(a,b)
    return int((a*b)/g)

assert lcm(210, 45) == 630


class Moon():
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = 0, 0, 0


    def __str__(self):
        return "pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>".format(self.x, self.y, self.z, self.vx, self.vy, self.vz)

    def tick(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def update_velocity(self, x, y, z):
        if self.x < x:
            self.vx += 1
        elif self.x > x:
            self.vx -= 1
            
        if self.y < y:
            self.vy += 1
        elif self.y > y:
            self.vy -= 1
            
        if self.z < z:
            self.vz += 1
        elif self.z > z:
            self.vz -= 1

    def kin_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def pot_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)
        

def gravity(moons):
    for m in moons:
        for n in moons:
            if m is n:
                continue
            m.update_velocity(n.x, n.y, n.z)


def tick(moons):
    for m in moons:
        m.tick()


def create_moon(s):
    x, y, z = [ int(x[2:]) for x in s.strip("\n").strip("<").strip(">").split(", ") ]
    return Moon(x, y, z)


def print_moons(moons):
    for m in moons:
        print(m)


def calc_tot_energy(moons):
    res = 0
    for m in moons:
        res += m.kin_energy()*m.pot_energy()
    return res


def create_moon_x_string(moons):
    res = ":"
    for moon in moons:
        res += "{}:{}:".format(moon.x, moon.vx)
    return res

    
def create_moon_y_string(moons):
    res = ":"
    for moon in moons:
        res += "{}:{}:".format(moon.y, moon.vy)
    return res
    

def create_moon_z_string(moons):
    res = ":"
    for moon in moons:
        res += "{}:{}:".format(moon.z, moon.vz)
    return res


"""
{Insert explenation why the movement is periodic}. The periodicity of each axis is
also indepent of the others. So determine every axis (pos, vel) periodicity by calculating
how many steps until we see the start (pos, vel). Then find the least common multiple of
the periodicity of the periodicity of the axi. This will be when the periodicities overlap
and therefore when the moons position in space and their velocities are the same as the start
values. {Insert reasoning why the periodicity includes the start values, can't there be a case where
the system stabilies after n steps and thereafter becomes periodic?}
"""
if __name__ == "__main__":
    with open("input", "r") as file:
        moons = []
        moon_strings = set()
        x_strings = set()
        y_strings = set()
        z_strings = set()

        for line in file:
            moons.append(create_moon(line))

        x_strings.add(create_moon_x_string(moons))
        y_strings.add(create_moon_y_string(moons))
        z_strings.add(create_moon_z_string(moons))

        x_period, y_period, z_period = None, None, None

        step = 1
        while True:
            gravity(moons)
            tick(moons)

            x_string = create_moon_x_string(moons)
            y_string = create_moon_y_string(moons)
            z_string = create_moon_z_string(moons)

            if x_string in x_strings:
                x_period = step
            if y_string in y_strings:
                y_period = step
            if z_string in z_strings:
                z_period = step

            if x_period and y_period and z_period:
                break

            step += 1

        # print(calc_tot_energy(moons))
        print("xp: {}, yp: {}, zp: {}".format(x_period, y_period, z_period))
        print("lcm: {}".format(lcm(lcm(x_period, y_period), z_period)))
        