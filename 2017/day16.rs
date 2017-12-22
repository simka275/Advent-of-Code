use std::io;
use std::collections::HashMap;

fn spin(programs: &mut Vec<char>, spins: usize) {
    let len = programs.len();
    let spins = spins % len;
    // Store char at index 0 new place
    let mut tmp = programs.clone();
    // Go through word and set cur pos to vec[(cur+spins)%len]
    for i in 0..len {
        tmp[i] = programs[(len+i-spins)%len];
    }
    // copy to program
    for i in 0..len {
        programs[i] = tmp[i];
    }
}

fn swap_pos(programs: &mut Vec<char>, i: usize, j: usize) {
    let tmp = programs[i];
    programs[i] = programs[j];
    programs[j] = tmp;
}

fn swap_progs(programs: &mut Vec<char>, ch_1: char, ch_2: char) {
    let programs_string: String = programs.iter().collect();
    let i = programs_string.find(ch_1);
    let j = programs_string.find(ch_2);
    // Make sure programs exist
    if i.is_none() || j.is_none() { return; }
    swap_pos(programs, i.unwrap(), j.unwrap());
}

fn dance(programs: &mut Vec<char>, moves: &Vec<&str>) {
    for dance_move in moves.iter() {
        // 0: move, 1: arg1, [2: sepper 3: arg2]
        let dance_move: Vec<char> = dance_move.chars().collect();
        let op = dance_move[0];
        let mut arg1 = String::new();
        let mut arg2 = String::new();
        let mut seperator = false;
        for i in 1..dance_move.len() {
            if dance_move[i] == '/' {
                seperator = true;
                continue;
            }
            if !seperator {
                arg1.push(dance_move[i]);
            } else {
                arg2.push(dance_move[i]);
            }
        }
        match op {
            // spin
            's' => spin(programs, arg1.parse::<usize>().unwrap()),
            // swap pos
            'x' => swap_pos(programs, arg1.parse::<usize>().unwrap(), arg2.parse::<usize>().unwrap()),
            // swap prog
            'p' => swap_progs(programs, arg1.chars().next().unwrap(), arg2.chars().next().unwrap()),
            // default
            _   => println!("move error"),
        }
    }
}

fn dance_n(programs: &mut Vec<char>, moves: &Vec<&str>, dance_count: u32) {
    // <permutation, iteration>
    let mut seen_perms: HashMap<String,u32> = HashMap::new();
    let mut programs_string: String = programs.iter().collect();
    seen_perms.insert(programs_string,0);
    let mut iteration = 1;
    let mut extra_iterations = 0;
    while iteration <= dance_count {
        dance(programs, &moves);
        programs_string = programs.iter().collect();
        // if permuation seen
        if seen_perms.contains_key(programs_string.as_str()) {
            let cycle_start = seen_perms.get(programs_string.as_str()).unwrap();
            let cycle_len = iteration-cycle_start;
            // Remove iters already done then mod with cycle len to get nr of extra iter to do
            extra_iterations = (dance_count-iteration) % cycle_len;
            // println!("cycle at {:?}, start: {:?}, len: {:?}", programs_string, cycle_start, cycle_len );
            break;
        }
        // add to seen
        seen_perms.insert(programs_string,iteration);
        iteration += 1;
    }
    for _i in 0..extra_iterations {
        dance(programs, &moves);
    }
}

fn main() {
    let mut programs: Vec<char> = "abcdefghijklmnop".chars().collect();
    let mut moves = String::new();
    io::stdin().read_line(&mut moves)
        .expect("Failed to read input");

    let moves: Vec<&str> = moves.trim().split(',').collect();

    // dance_n(&mut programs,&moves); // part one
    dance_n(&mut programs,&moves,1000000000); // part two

    let programs: String = programs.iter().collect();
    println!("{}", programs);
}
