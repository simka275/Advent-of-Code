use std::io;

struct Particle {
    px: i32,
    py: i32,
    pz: i32,
    vx: i32,
    vy: i32,
    vz: i32,
    ax: i32,
    ay: i32,
    az: i32,
}

fn make_particles() -> Vec<Particle> {
    let mut particles: Vec<Particle> = Vec::new();
    loop {
        let mut line = String::new();
        io::stdin().read_line(&mut line).
            expect("Failed to read input");
        // eof
        if line.is_empty() { break; }
        let line: Vec<&str> = line.trim().split(", ").collect();
        // println!("{:?}", line);
        // extract position
        let mut pos = String::from(line[0]);
        pos.remove(0);
        pos.remove(0);
        pos.remove(0);
        let end = pos.find('>').unwrap();
        pos.remove(end);
        let pos: Vec<i32> = pos.trim().split(',').map(|x| x.parse::<i32>().unwrap()).collect();
        // extract velocity
        let mut vel = String::from(line[1]);
        vel.remove(0);
        vel.remove(0);
        vel.remove(0);
        let end = vel.find('>').unwrap();
        vel.remove(end);
        let vel: Vec<i32> = vel.trim().split(',').map(|x| x.parse::<i32>().unwrap()).collect();
        // extract acceleration
        let mut acc = String::from(line[2]);
        acc.remove(0);
        acc.remove(0);
        acc.remove(0);
        let end = acc.find('>').unwrap();
        acc.remove(end);
        let acc: Vec<i32> = acc.trim().split(',').map(|x| x.parse::<i32>().unwrap()).collect();
        let particle = Particle {
            px: pos[0],
            py: pos[1],
            pz: pos[2],
            vx: vel[0],
            vy: vel[1],
            vz: vel[2],
            ax: acc[0],
            ay: acc[1],
            az: acc[2],
        };
        // println!("{:?}, {:?}, {:?}", pos, vel, acc);
        particles.push(particle);
    }
    return particles;
}

#[allow(dead_code)]
// return index of particle with slowest acc
fn find_slowest_acc(particles: &Vec<Particle>) -> usize {
    let mut best_i = 0;
    let mut best_mh_acc = particles[0].ax.abs() + particles[0].ay.abs() + particles[0].az.abs();
    for i in 1..particles.len() {
        let cur_mh_acc = particles[i].ax.abs() + particles[i].ay.abs() + particles[i].az.abs();
        if cur_mh_acc < best_mh_acc {
            best_i = i;
            best_mh_acc = cur_mh_acc;
        }
    }
    return best_i;
}

fn tick(particles: &mut Vec<Particle>) {
    for particle in particles {
        particle.vx += particle.ax;
        particle.px += particle.vx;
        particle.vy += particle.ay;
        particle.py += particle.vy;
        particle.vz += particle.az;
        particle.pz += particle.vz;
    }
}

fn is_colliding(p1: &Particle, p2: &Particle) -> bool {
    return p1.px == p2.px && p1.py == p2.py && p1.pz == p2.pz;
}

fn get_colliding_index(particles: &mut Vec<Particle>) -> Vec<usize> {
    let mut colliding: Vec<usize> = Vec::new();
    for i in 0..particles.len() {
        for j in i+1..particles.len() {
            if is_colliding(&particles[i], &particles[j]) {
                if !colliding.contains(&i) {
                    colliding.push(i);
                }
                if !colliding.contains(&j) {
                    colliding.push(j);
                }
            }
        }
    }
    colliding.sort();
    colliding.reverse();
    return colliding;
}

fn main() {
    let mut particles = make_particles();
    // part one
    // println!("{:?}", find_slowest_acc(&particles));
    // part two
    let mut t_limit = 450;
    while t_limit > 0 {
        tick(&mut particles);
        let colliding = get_colliding_index(&mut particles);
        // remove colliding
        if !colliding.is_empty() {
            println!("removing: {:?}", colliding);
            for particle in colliding {
                particles.remove(particle);
            }
            t_limit = 450;
        }
        t_limit -= 1;
    }
    println!("{:?}", particles.len());
}
