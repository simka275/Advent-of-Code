use std::collections::VecDeque;

fn main() {
    let mut gen_a: u64 = 116;
    let a_factor: u64 = 16807;
    let mut a_queue: VecDeque<u64> = VecDeque::new();
    let mut gen_b: u64 = 299;
    let b_factor: u64 = 48271;
    let mut b_queue: VecDeque<u64> = VecDeque::new();
    let divisor: u64 = 2147483647;

    let mut matches = 0;
    let mut comparisons = 0;
    while comparisons < 5000000 {
        // a
        gen_a = (gen_a*a_factor)%divisor;
        // If multiple of 4 add 16 last bits to queue
        if gen_a % 4 == 0 { a_queue.push_back(gen_a % 65536); }
        // b
        gen_b = (gen_b*b_factor)%divisor;
        if gen_b % 8 == 0 { b_queue.push_back(gen_b % 65536); }

        // check last 16 bits i.e. if nrs modulo 2^16 is equal
        if !a_queue.is_empty() && !b_queue.is_empty() {
            let a = a_queue.pop_front();
            let b = b_queue.pop_front();
            // compare
            if a == b { matches += 1; }
            // done comp
            comparisons += 1;
        }
    }
    println!("{:?}", matches);
}
