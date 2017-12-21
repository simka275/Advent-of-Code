use std::io;

fn main() {
    let mut stream = String::new();
    io::stdin().read_line(&mut stream)
        .expect("Failed to read input");

    let mut score = 0;
    let mut garbage_counter = 0;
    let mut depth = 0;
    let mut garbage = false;
    let mut ignore = false;
    for ch in stream.trim().chars() {
        // Ignore case
        if ignore {
            ignore = false;
            continue;
        }
        // Inside garbage
        if garbage {
            if ch == '>' {
                garbage = false;
            } else if ch == '!' {
                ignore = true;
            } else {
                garbage_counter += 1;
            }
            continue;
        }
        // Standard case
        match ch {
            '{' => {
                depth += 1;
            },
            '}' => {
                score += depth;
                depth -= 1;
            },
            '<' => {
                garbage = true;
            },
            _ => continue,
        }
    }
    // part one
    // println!("{:?}", score);
    // part two
    println!("{:?}", garbage_counter);
}
