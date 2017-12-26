
enum State {
    A,B,C,D,E,F,
}

fn main() {
    let mut state: State = State::A;
    let mut steps = 12994925;
    let mut pos = 0;
    let mut tape: Vec<bool> = Vec::new();
    tape.push(false);
    tape.push(false);
    tape.push(false);
    while steps > 0 {
        match state {
            State::A => {
                if !tape[pos] {
                    tape[pos] = true;
                    if pos == tape.len()-1 { tape.push(false); }
                    pos += 1;
                    state = State::B;
                } else {
                    tape[pos] = false;
                    if pos == 0 { tape.insert(0,false); pos += 1; }
                    pos -= 1;
                    state = State::F;
                }
            },
            State::B => {
                if !tape[pos] {
                    tape[pos] = false;
                    if pos == tape.len()-1 { tape.push(false); }
                    pos += 1;
                    state = State::C;
                } else {
                    tape[pos] = false;
                    if pos == tape.len()-1 { tape.push(false); }
                    pos += 1;
                    state = State::D;
                }
            },
            State::C => {
                if !tape[pos] {
                    tape[pos] = true;
                    if pos == 0 { tape.insert(0,false); pos += 1; }
                    pos -= 1;
                    state = State::D;
                } else {
                    tape[pos] = true;
                    if pos == tape.len()-1 { tape.push(false); }
                    pos += 1;
                    state = State::E;
                }
            },
            State::D => {
                if !tape[pos] {
                    tape[pos] = false;
                    if pos == 0 { tape.insert(0,false); pos += 1; }
                    pos -= 1;
                    state = State::E;
                } else {
                    tape[pos] = false;
                    if pos == 0 { tape.insert(0,false); pos += 1; }
                    pos -= 1;
                    state = State::D;
                }
            },
            State::E => {
                if !tape[pos] {
                    tape[pos] = false;
                    if pos == tape.len()-1 { tape.push(false); }
                    pos += 1;
                    state = State::A;
                } else {
                    tape[pos] = true;
                    if pos == tape.len()-1 { tape.push(false); }
                    pos += 1;
                    state = State::C;
                }
            },
            State::F => {
                if !tape[pos] {
                    tape[pos] = true;
                    if pos == 0 { tape.insert(0,false); pos += 1; }
                    pos -= 1;
                    state = State::A;
                } else {
                    tape[pos] = true;
                    if pos == tape.len()-1 { tape.push(false); }
                    pos += 1;
                    state = State::A;
                }
            },
        }
        // println!("{:?}", steps);
        steps -= 1;
    }
    // count 1's
    let mut ones = 0;
    for p in tape.iter() {
        if *p { ones += 1; }
    }
    println!("{:?}", ones);
}
