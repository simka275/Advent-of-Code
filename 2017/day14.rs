
fn reverse_list(list: &mut Vec<u8>, index: usize, length: usize) {
    let mut tmp_list: Vec<u8> = Vec::new();
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

fn knot_hash(input: &str) -> Vec<u8> {
    let mut input: Vec<usize> = input.trim().chars().map(|x| x as usize).collect();
    input.push(17);
    input.push(31);
    input.push(73);
    input.push(47);
    input.push(23);
    // Create list of ints
    let mut list: Vec<u8> = Vec::new();
    for i in 0..256 {
        list.push(i as u8);
    }
    let mut index = 0;
    let mut skip_size = 0;
    // Generate the sparse hash
    for _i in 0..64 {
        for length in input.iter() {
            reverse_list(&mut list,index,*length);
            index = (index+*length+skip_size)%list.len();
            skip_size += 1;
        }
    }
    // Perform XOR on each block of 16 elements i.e. generate dense hash
    let mut dense_list: Vec<u8> = Vec::new();
    for block_index in 0..16 {
        let mut xor_res = 0;
        for index in 0..16 {
            xor_res ^= list[16*block_index+index];
        }
        dense_list.push(xor_res);
    }
    return dense_list;
}

fn flood_fill(memory: &mut [[bool;128];128], row: usize, col: usize) {
    if !memory[row][col] {
        return; // no connection
    } else {
        // Change current and add flood fill all neighbors
        memory[row][col] = false;
        if row > 0 { flood_fill(memory, row-1, col); } // up
        if row < memory.len()-1 { flood_fill(memory, row+1, col); } // down
        if col > 0 { flood_fill(memory, row, col-1); } // left
        if col < memory[row].len()-1 { flood_fill(memory, row, col+1); } // right
    }
}

fn find_regions(memory: &mut [[bool;128];128]) -> i32 {
    // Go through memory and flood fill on used squares
    // where flood fill sets conencted squares to unused
    let mut regions = 0;
    for row in 0..memory.len() {
        for col in 0..memory[row].len() {
            if memory[row][col] {
                flood_fill(memory, row, col);
                regions += 1;
            }
        }
    }
    return regions;
}

fn main() {
    let input = "oundnydw";
    let mut memory: [[bool;128];128] = [[false;128];128];
    let mut used_squares = 0;
    for row in 0..128 {
        // Construct row input
        let mut row_input = String::from(input);
        row_input.push_str("-");
        row_input.push_str(row.to_string().as_str());
        // Hash
        let hash = knot_hash(row_input.as_str());
        for i in 0..hash.len() {
            // Check every bit in byte
            let mut byte: u8 = hash[i];
            // part one
            used_squares += byte.count_ones();
            for j in 0..8 {
                memory[row][i*8+j] = (byte & 0b10000000) == 0b10000000;
                byte = byte.rotate_left(1); // left shift
            }
        }
    }
    // part one
    println!("{:?}", used_squares);
    // for row in memory.iter() {
    //     for col in row.iter() {
    //         if *col {
    //             print!("#");
    //         } else {
    //             print!(".");
    //         }
    //     }
    //     println!("");
    // }
    println!("{:?}", find_regions(&mut memory));
}
