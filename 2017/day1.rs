use std::io;

fn part_one(sequence: String){
    let sequence = sequence.trim();
    let mut pre_val = sequence.chars().last().unwrap(); // Last
    let mut counter = 0;
    for val in sequence.chars() {
        // println!("p:{} c:{}", pre_val, val );
        if pre_val == val {
            counter += val.to_digit(10).unwrap();
        }
        pre_val = val;
    }
    println!("{}", counter);
}

fn part_two(sequence: String) {
    let sequence = sequence.trim();

    let first_half = sequence.get(0..sequence.len()/2);
    let second_half = sequence.get(sequence.len()/2..);
    let mut shifted_sequence = String::from(second_half.unwrap());
    shifted_sequence.push_str(first_half.unwrap());
    let mut shifted_sequence = shifted_sequence.chars();

    let mut counter = 0;

    for ch in sequence.chars() {
        let cmp_ch = shifted_sequence.next().unwrap();
        // println!("c:{} cc:{}", ch, cmp_ch);
        if ch == cmp_ch {
            counter += ch.to_digit(10).unwrap();
        }
    }
    println!("{}", counter);
}

fn main() {
    let mut sequence = String::new();

    io::stdin().read_line(&mut sequence)
        .expect("Failed to read input");

    // part_one(sequence);
    part_two(sequence);
}
