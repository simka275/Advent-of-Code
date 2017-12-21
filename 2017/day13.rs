use std::io;
use std::cmp;
use std::collections::HashMap;

fn traverse_firewall(firewall: &HashMap<i32,i32>, end_layer: i32) -> i32 {
    // let mut layer = 0;
    let mut severity_sum = 0;
    for layer in 0..end_layer+1 {
        // If no scanner than get through
        if !firewall.get(&layer).is_none() {
            // Collision if scan pos == 0
            let range = firewall.get(&layer).unwrap();
            let scan_pos = layer%(2*(*range-1));
            // If scan pos after ticks is 0 then collision
            if scan_pos == 0 {
                severity_sum += range*layer;
            }
        }
    }
    return severity_sum;
}

fn can_pass(firewall: &HashMap<i32,i32>, delay: i32, end_layer: i32) -> bool {
    // println!("{:?}", firewall);
    for layer in 0..end_layer+1 {
        // If no scanner than get through
        if !firewall.get(&layer).is_none() {
            // Collision if scan pos == 0
            let ticks = delay + layer;
            let range = firewall.get(&layer).unwrap();
            let scan_pos = ticks%(2*(*range-1));
            // println!("l:{:?}, sp:{}", layer, scan_pos);
            // If scan pos after ticks is 0 then collision
            if scan_pos == 0 { return false; }
        }
    }
    return true;
}

fn find_delay(firewall: &HashMap<i32,i32>, end_layer: i32) -> i32 {
    let mut delay = 0;
    while !can_pass(firewall,delay,end_layer) {
        // println!("{:?}", delay);
        delay += 1;
    }
    return delay
}

fn main() {
    // key: layer, value:(range, scanner position,going_up)
    let mut firewall: HashMap<i32,i32> = HashMap::new();
    let mut end_layer = 0;
    loop {
        let mut line = String::new();
        io::stdin().read_line(&mut line)
            .expect("Failed to read input");
        // end case
        if line == "" { break; }
        let args: Vec<i32> = line.trim().split(": ").map(|x| x.parse().unwrap()).collect();
        // println!("{:?}", args);
        firewall.insert(args[0],args[1]);
        end_layer = cmp::max(end_layer,args[0]);
    }
    // part one
    println!("{:?}", traverse_firewall(&firewall, end_layer));
    // part twos
    println!("{:?}", find_delay(&firewall, end_layer));
}
