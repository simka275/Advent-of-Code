use std::io;
use std::cmp;

fn optimize_steps(steps:  &mut [i32;3]) {
    // convert nw+ne to n
    while steps[0] > 0 && steps[2] > 0 {
        steps[0] -= 1; // dec nw
        steps[2] -= 1; // dec ne
        steps[1] += 1; // inc n
    }
    // convert se+sw to s
    while steps[0] < 0 && steps[2] < 0 {
        steps[0] += 1; // dec se
        steps[2] += 1; // dec sw
        steps[1] -= 1; // inc s
    }
    // convert ne+s to se
    while steps[2] > 0 && steps[1] < 0 {
        steps[2] -= 1; // dec ne
        steps[1] += 1; // dec s
        steps[0] -= 1; // inc se
    }
    // convert nw+s to sw
    while steps[0] > 0 && steps[1] < 0 {
        steps[0] -= 1; // dec nw
        steps[1] += 1; // dec s
        steps[2] -= 1;// inc sw
    }
    // convert se+n to ne
    while steps[0] < 0 && steps[1] > 0 {
        steps[0] += 1; // dec se
        steps[1] -= 1; // dec n
        steps[2] += 1; // inc ne
    }
    // convert sw+n to nw
    while steps[2] < 0 && steps[1] > 0 {
        steps[2] += 1; // dec sw
        steps[1] -= 1; // dec n
        steps[0] += 1; // inc nw
    }
}

fn calc_steps(steps: [i32;3]) -> i32{
    let mut res = 0;
    for step in steps.iter() {
        res += step.abs();
    }
    return res;
}

fn main() {
    let mut path = String::new();
    io::stdin().read_line(&mut path)
        .expect("Failed to read input");
    let path: Vec<&str> = path.trim().split(',').collect();
    // println!("{:?}", path);
    let mut max_dist = 0;
    //steps: [#nw,#n,#ne]
    let mut steps: [i32;3] = [0,0,0];
    for step in path {
        match step {
            "nw" => steps[0] += 1,
            "n"  => steps[1] += 1,
            "ne" => steps[2] += 1,
            "sw" => steps[2] -= 1,
            "s"  => steps[1] -= 1,
            "se" => steps[0] -= 1,
            _    => println!("step error"),
        }
        optimize_steps(&mut steps);
        max_dist = cmp::max(max_dist, calc_steps(steps));
    }
    // part two
    println!("{:?}", max_dist);
    // part one
    // optimize_steps(&mut steps);
    // println!("{:?}", calc_steps(steps));
}
