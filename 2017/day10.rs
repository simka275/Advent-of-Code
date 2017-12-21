use std::io;

fn reverse_list(list: &mut Vec<i32>, index: usize, length: usize) {
    let mut tmp_list: Vec<i32> = Vec::new();
    let list_len = list.len();
    // Affected items are [index..index+length[
    // add them to tmp
    for i in 0..length {
        tmp_list.push(list[(index+i)%list_len]);
    }
    // reverse tmp
    tmp_list.reverse();
    // add them back to list
    for i in 0..length {
        list[(index+i)%list_len] = tmp_list[i];
    }
}

fn main() {
    // Create list of ints
    let mut list: Vec<i32> = Vec::new();
    for i in 0..256 {
        list.push(i);
    }
    // Create list of lengths
    let mut line = String::new();
    io::stdin().read_line(&mut line)
        .expect("Failed to read input");
    let mut lengths: Vec<usize> = line.trim().chars().map(|x| x as usize).collect();
    // The extra static lengths
    lengths.push(17);
    lengths.push(31);
    lengths.push(73);
    lengths.push(47);
    lengths.push(23);
    // println!("{:?}", lengths);
    let mut index = 0;
    let mut skip_size = 0;

    // Generate the sparse hash
    for _i in 0..64 {
        for length in lengths.iter() {
            reverse_list(&mut list,index,*length);
            index = (index+*length+skip_size)%list.len();
            skip_size += 1;
            // println!("{:?}", list);
        }
    }
    println!("{:?}", list);
    // Perform XOR on each block of 16 elements i.e. generate dense hash
    let mut dense_list: Vec<i32> = Vec::new();
    for block_index in 0..16 {
        let mut xor_res = 0;
        for index in 0..16 {
            xor_res ^= list[16*block_index+index];
        }
        dense_list.push(xor_res);
    }
    // println!("{:?}", dense_list);
    // print as hex, part two
    for n in dense_list {
        if n < 16 { print!("{}", 0);} // always 2 hex chars
        print!("{:x}", n);
    }
    println!("");

    // println!("{:?}", list[0]*list[1]); // part one
}
