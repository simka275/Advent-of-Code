use std::io;
use std::collections::HashMap;

fn balance_banks(banks: &mut Vec<i32>) {
    // Find index of max nr of blocks
    let mut max_blocks_index = 0;
    for i in 0..banks.len() {
        if banks[i] > banks[max_blocks_index] {
            max_blocks_index = i;
        }
    }
    let mut blocks = banks[max_blocks_index];
    banks[max_blocks_index] = 0;
    let mut current_index = max_blocks_index;
    while blocks > 0 {
        current_index = (current_index+1) % banks.len();
        banks[current_index] += 1;
        blocks -= 1;
    }

    // for i in 0..banks.len() {
    //     print!("{:?} ", banks[i]);
    // }
    // println!("");
}

fn get_state(banks: &Vec<i32>) -> String {
    let mut state: String = String::new();
    for i in 0..banks.len() {
        state.push_str(banks[i].to_string().as_str());
        state.push('.');
    }
    return state;
}

fn main() {
    let mut line = String::new();
    let mut states: HashMap<String,i32> = HashMap::new();

    io::stdin().read_line(&mut line)
        .expect("Failed to read input");

    let mem_banks: Vec<&str> = line.trim().split(' ').collect();
    let mut mem_banks: Vec<i32> = mem_banks.into_iter().map(|n| n.parse().unwrap()).collect();

    let mut counter = 0;
    loop {
        let state = get_state(&mem_banks);
        // Break if already seen state
        if states.contains_key(&state) {
            // println!("{:?}", counter); // Part one
            println!("{:?}", counter-states.get(&state).unwrap()); // Part two
            break;
        }
        // Insert current state
        states.insert(state,counter);
        // Balance blocks
        balance_banks(&mut mem_banks);
        counter += 1;
    }
}
