use std::io;

fn make_map() -> Vec<Vec<char>> {
    let mut map: Vec<Vec<char>> = Vec::new();
    loop {
        let mut line = String::new();
        io::stdin().read_line(&mut line).
            expect("Failed to read input");
        // eof
        if line.is_empty() { break; }
        // add row to map
        let row: Vec<char> = line.trim_matches('\n').chars().collect();
        println!("{:?}", row.len());
        map.push(row);
    }
    return map;
}

// travels map and returns encountered letters
fn traverse(map: &Vec<Vec<char>>) -> (String,u32) {
    let mut letters = String::new();
    let mut cur_row: usize = 0;
    let mut cur_col: usize = 0;
    let mut cur_dir: String = String::from("down");
    let mut fin = false;
    let mut steps: u32 = 1; // count step into map from outside
    // find start position
    for col in 0..map[cur_row].len() {
        if map[cur_row][col] == '|' {
            cur_col = col;
            break;
        }
    }
    // travel
    loop {
        // take a step
        match cur_dir.as_str() {
            "up"    => {
                if cur_row > 0 && map[cur_row-1][cur_col] != ' ' { // up
                    cur_row -= 1;
                } else if cur_col > 0 && map[cur_row][cur_col-1] != ' ' { // left
                    cur_col -= 1;
                    cur_dir = String::from("left");
                } else if cur_col < (map[cur_row].len()-1) && map[cur_row][cur_col+1] != ' ' { // right
                    cur_col += 1;
                    cur_dir = String::from("right");
                } else { // end
                    fin = true;
                }
            },
            "down"  => {
                if cur_row < (map.len()-1) && map[cur_row+1][cur_col] != ' ' { // down
                    cur_row += 1;
                } else if cur_col > 0 && map[cur_row][cur_col-1] != ' ' { // left
                    cur_col -= 1;
                    cur_dir = String::from("left");
                } else if cur_col < (map[cur_row].len()-1) && map[cur_row][cur_col+1] != ' ' { // right
                    cur_col += 1;
                    cur_dir = String::from("right");
                } else { // end
                    fin = true;
                }
            },
            "left"  => {
                if cur_col > 0 && map[cur_row][cur_col-1] != ' ' { // left
                    cur_col -= 1;
                } else if cur_row > 0 && map[cur_row-1][cur_col] != ' ' { // up
                    cur_row -= 1;
                    cur_dir = String::from("up");
                } else if cur_row < (map.len()-1) && map[cur_row+1][cur_col] != ' ' { // down
                    cur_row += 1;
                    cur_dir = String::from("down");
                } else { // end
                    fin = true;
                }
            },
            "right" => {
                if cur_col < (map[cur_row].len()-1) && map[cur_row][cur_col+1] != ' ' {
                    cur_col += 1;
                } else if cur_row > 0 && map[cur_row-1][cur_col] != ' ' { // up
                    cur_row -= 1;
                    cur_dir = String::from("up");
                } else if cur_row < (map.len()-1) && map[cur_row+1][cur_col] != ' ' { // down
                    cur_row += 1;
                    cur_dir = String::from("down");
                } else { // end
                    fin = true;
                }
            },
            _       => println!("dir error"),
        }
        // if at end
        if fin { break; }
        // add new pos letter to letters
        let cur_char = map[cur_row][cur_col];
        if cur_char != '+' && cur_char != '|' && cur_char != '-' {
            letters.push(cur_char);
        }
        steps += 1;
    }
    return (letters,steps);
}

fn main() {
    let map = make_map();
    let sol: (String,u32) = traverse(&map);
    println!("{:?}", sol.0); // part one
    println!("{:?}", sol.1); // part two
}
