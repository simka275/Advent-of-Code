use std::io;
use std::cmp;

fn part_one(matrix: Vec<Vec<i32>>) {
    let mut sum = 0;
    for row in 0..matrix.len() {
        let mut min = matrix[row][0]; // init min
        let mut max = matrix[row][0]; // init max
        for col in 0..matrix[row].len() {
            min = cmp::min(min, matrix[row][col]);
            max = cmp::max(max,matrix[row][col]);
        }
        sum += max;
        sum -= min;
    }
    println!("{:?}", sum);
}

fn part_two(matrix: Vec<Vec<i32>>) {
    let mut sum = 0;
    for row in 0..matrix.len() {
        'num: for num_i in matrix[row].iter() {
            for den_i in matrix[row].iter() {
                // println!("{:?} {:?}", num_i, den_i);
                if num_i == den_i {
                    continue;
                } else if num_i % den_i == 0 {
                    sum += num_i/den_i;
                    break 'num;
                }
            }
        }
    }
    println!("{:?}", sum);
}

fn main() {
    let mut matrix: Vec<Vec<i32>> = Vec::new();
    // Read input
    loop {
        let mut row = String::new();
        io::stdin().read_line(&mut row)
        .expect("Failed to read input");
        // Abort if no input
        if row == "" { break; }
        // collect strings
        let row: Vec<&str> = row.split('\t').collect();
        // conv to int
        let row: Vec<i32> = row.into_iter().map(|x| x.trim().parse().unwrap()).collect();
        matrix.push(row);
        // println!("{:?}", row);
    }

    // part_one(matrix);
    part_two(matrix);
}
