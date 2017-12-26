use std::io;

fn make_grid() -> Vec<Vec<char>> {
    let mut grid: Vec<Vec<char>> = Vec::new();
    loop {
        let mut row = String::new();
        io::stdin().read_line(&mut row).
            expect("Failed to read input");
        // eof
        if row.is_empty() { break; }
        let row: Vec<char> = row.trim().chars().collect();
        grid.push(row);
    }
    return grid;
}

fn expand_grid(grid: &mut Vec<Vec<char>>) {
    // Expand 2 extra columns
    for row in grid.iter_mut() {
        row.insert(0,'.');
        row.push('.');
    }
    // Expand 2 extra rows
    let mut row: Vec<char> = Vec::new();
    for _i in 0..grid[0].len() {
        row.push('.');
    }
    grid.insert(0,row.clone());
    row.clear();
    for _i in 0..grid[0].len() {
        row.push('.');
    }
    grid.push(row);
}

#[allow(dead_code)]
fn print_grid(grid: &Vec<Vec<char>>) {
    for row in grid.iter() {
        println!("{:?}", row);
    }
    println!("");
}

fn turn_right(dir: &str) -> &str {
    let mut res = "";
    match dir {
        "up"    => res = "right",
        "down"  => res = "left",
        "left"  => res = "up",
        "right" => res = "down",
        _       => println!("turn right error"),
    }
    return res;
}

fn turn_left(dir: &str) -> &str {
    let mut res = "";
    match dir {
        "up"    => res = "left",
        "down"  => res = "right",
        "left"  => res = "down",
        "right" => res = "up",
        _       => println!("turn left error"),
    }
    return res;
}

fn turn_back(dir: &str) -> &str {
    let mut res = "";
    match dir {
        "up"    => res = "down",
        "down"  => res = "up",
        "left"  => res = "right",
        "right" => res = "left",
        _       => println!("turn back error"),
    }
    return res;
}

fn traverse() {
    let mut grid = make_grid();
    let mut row = grid.len()/2;
    let mut col = grid.len()/2;
    let mut dir = "up";
    let mut bursts = 10000000;
    let mut infections = 0;
    while bursts > 0 {
        // cleanup or infect
        if grid[row][col] == '#' { // at infected
            dir = turn_right(dir);
            grid[row][col] = 'F';
        } else if grid[row][col] == '.' { // at clean
            dir = turn_left(dir);
            grid[row][col] = 'W';;
        } else if grid[row][col] == 'F' { // at flagged
            dir = turn_back(dir);
            grid[row][col] = '.';
        } else if grid[row][col] == 'W' { // at weak
            grid[row][col] = '#';
            infections += 1;
        }
        // if at edge of grid expand
        if row == 0 || col == 0 || row == grid.len()-1 || col == grid[row].len()-1 {
            expand_grid(&mut grid);
            row += 1;
            col += 1;
        }
        // move
        match dir {
            "up"    => row -= 1,
            "down"  => row += 1,
            "left"  => col -= 1,
            "right" => col += 1,
            _       => println!("move error"),
        }
        // println!("{:?},{:?},{:?}", row,col,dir);
        // print_grid(&grid);
        bursts -= 1;
    }
    println!("{:?}", infections);
}

fn main() {
    traverse();
}
