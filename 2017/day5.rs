use std::io;

fn traverse_list(list: &mut Vec<i32>) -> i32 {
    let mut hops = 0;
    let mut index: i32 = 0;
    loop {
        let value = list[index as usize];
        // Update value
        if value > 2 { // Remove for part one
            list[index as usize] -= 1;
        } else {
            list[index as usize] += 1;
        }
        // Increas
        index += value;
        // Increase hop ctr
        hops += 1;

        // for nr in list.into_iter() {
        //     print!("{:?} ", nr);
        // }
        // println!("index: {:?}", index);

        // End cond
        if index < 0 || index >= list.len() as i32 {
            break;
        }
    }
    return hops;
}

fn main() {
    let mut list: Vec<i32> = Vec::new();
    let mut n = String::new();
    loop {
        io::stdin().read_line(&mut n)
        .expect("Failed to read input");
        // EOF
        if n == "" { break; };
        list.push(n.trim().parse().unwrap());
        n.clear();
    }
    println!("{:?}", traverse_list(&mut list));
}
