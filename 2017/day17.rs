
fn spin_lock_one(step_size: usize, end: usize) -> usize {
    let mut list: Vec<usize> = Vec::new();
    let mut current_pos = 0;
    list.push(0);
    for i in 1..end+1 {
        // take steps
        current_pos = (current_pos + step_size) % list.len();
        // insert i after current_pos
        if current_pos+1 == list.len() {
            list.push(i);
        } else {
            list.insert(current_pos+1,i);
        }
        current_pos += 1;
    }
    return list[(current_pos+1)%list.len()];
}

fn spin_lock_two(step_size: usize, end: usize) -> usize {
    let mut current_pos = 0;
    let mut value = 0;
    let mut len = 1;
    for i in 1..end+1 {
        // take steps
        current_pos = (current_pos + step_size) % len;
        // only care if insert at postion 1
        if current_pos == 0 { value = i; }
        // increase length ( fake insert )
        len += 1;
        current_pos += 1;
    }
    return value;
}

fn main() {
    // part one
    println!("{:?}",spin_lock_one(344,2017));
    // part two
    println!("{:?}", spin_lock_two(344,50000000));
}
