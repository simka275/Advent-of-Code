use std::io;

/*
fn calc_square(n: i32) -> i32 {
    let n: f64 = n as f64;
    let square: i32 = (((n.sqrt()-1.0_f64)/2.0_f64)+0.49_f64).round() as i32;
    return square;
}

fn calc_mh_dist(n: i32) -> i32 {
    if n < 2 { return 0; } // Trivial case
    let square_num = calc_square(n); // n belongs in square num s
    let pre_square_val = (2*square_num-1).pow(2); // End value in square before
    let tot_steps = n -pre_square_val; // Total nr of steps in square to get to n
    let side_steps = tot_steps % (2*square_num); // Steps along last side to get to n
    let to_mid_steps = (square_num-side_steps).abs(); // In square s the middle is s steps in from corner
    // Go to middle and then for square s distance to middle of all
    // squares are s steps
    let distance = to_mid_steps + square_num;
    // println!("sqn, psqv, ts, ss, tms, d");
    // println!("{:?}, {:?}, {:?}, {:?}, {:?}, {:?}",square_num, pre_square_val, tot_steps, side_steps, to_mid_steps, distance );
    return distance;
}

fn part_one() -> () {
    let mut n = String::new();
    io::stdin().read_line(&mut n)
    .expect("Failed to read input");
    let n: i32 = n.trim().parse().unwrap();
    println!("{:?}", calc_mh_dist(n));
}
*/

fn sum_of_neighbors(row: i32, col: i32, matrix: &mut Vec<Vec<i32>>) -> i32 {
    // Sum around curpos
    let mut res: i32 = 0;

    for row_offset in -1..2 {
        // Check if valid row
        if row+row_offset < 0 || row+row_offset >= matrix.len() as i32 {
            continue;
        }
        let r_o = (row+row_offset) as usize;
        for col_offset in -1..2 {
            // Check if valid column
            if col+col_offset < 0 || col+col_offset >= matrix[r_o].len() as i32 {
                continue;
            }
            let c_o = (col+col_offset) as usize;
            res += matrix[r_o][c_o]; // Add neighbor
        }
    }
    return res;
}

// Returns first nr greater than n in a spiralsum square of odd size
// Returns -1 if square is to small and doesn't contain nr > n
// Undefined for squares with even side length
fn calc_spiralsum(n :i32, square_size: i32) -> i32 {
    // Init
    let mut matrix: Vec<Vec<i32>> = Vec::new();
    for _row in 0..square_size {
        let mut column: Vec<i32> = Vec::new();
        for _col in 0..square_size {
            column.push(0);
        }
        matrix.push(column);
    }
    matrix[(square_size/2) as usize][(square_size/2) as usize] = 1;

    // Start position
    let mut cur_row = square_size/2 +1;
    let mut cur_col = square_size/2 +1;
    let mut side_steps = 2; // First square has size 3 so 2 steps to get to end

    while cur_row < matrix.len() as i32 {
        // Up
        for _step in 0..side_steps {
            cur_row -= 1;
            // Sum around curpos
            matrix[cur_row as usize][cur_col as usize] = sum_of_neighbors(cur_row, cur_col, &mut matrix);
            // Check if nr > n found if so return it
            if matrix[cur_row as usize][cur_col as usize] > n {
                return matrix[cur_row as usize][cur_col as usize];
            }
        }
        // Left
        for _step in 0..side_steps {
            cur_col -= 1;
            // Sum around curpos
            matrix[cur_row as usize][cur_col as usize] = sum_of_neighbors(cur_row, cur_col, &mut matrix);
            // Check if nr > n found if so return it
            if matrix[cur_row as usize][cur_col as usize] > n {
                return matrix[cur_row as usize][cur_col as usize];
            }
        }
        // Down
        for _step in 0..side_steps {
            cur_row += 1;
            // Sum around curpos
            matrix[cur_row as usize][cur_col as usize] = sum_of_neighbors(cur_row, cur_col, &mut matrix);
            // Check if nr > n found if so return it
            if matrix[cur_row as usize][cur_col as usize] > n {
                return matrix[cur_row as usize][cur_col as usize];
            }
        }
        // Right
        for _step in 0..side_steps {
            cur_col += 1;
            // Sum around curpos
            matrix[cur_row as usize][cur_col as usize] = sum_of_neighbors(cur_row, cur_col, &mut matrix);
            // Check if nr > n found if so return it
            if matrix[cur_row as usize][cur_col as usize] > n {
                return matrix[cur_row as usize][cur_col as usize];
            }
        }
        // Next square
        cur_row += 1;
        cur_col += 1;
        side_steps += 2;
    }

    // for row in 0..matrix.len() {
    //     for col in 0..matrix[row].len() {
    //         print!("{:?} ", matrix[row][col]);
    //     }
    //     println!("");
    // }

    // Failed to find nr > n if got here
    return -1;
}

fn part_two() -> () {
    let mut n = String::new();
    io::stdin().read_line(&mut n)
        .expect("Failed to read input");
    let n: i32 = n.trim().parse().unwrap();
    let mut square_size = 3;
    let mut res = calc_spiralsum(n,square_size);
    while res < 0 {
        square_size += 2;
        res = calc_spiralsum(n,square_size);
    }
    println!("{:?}", res);
}

fn main() {
    // part_one();
    part_two();
}
