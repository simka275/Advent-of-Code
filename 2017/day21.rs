use std::io;
use std::collections::HashMap;

fn make_rules() -> HashMap<String,String> {
    let mut rules: HashMap<String,String> = HashMap::new();
    loop {
        let mut line = String::new();
        io::stdin().read_line(&mut line).
        expect("Failed to read input");
        // eof
        if line.is_empty() { break; }
        let rule: Vec<&str> = line.trim().split(" => ").collect();
        let key: String = rule[0].split('/').collect();
        rules.insert(String::from(key),String::from(rule[1]));
    }
    return rules;
}

// clockwise
fn rotate_2(square: String) -> String {
    let square = square.as_bytes();
    let mut res: Vec<u8> = Vec::new();
    res.push(square[2]);
    res.push(square[0]);
    res.push(square[3]);
    res.push(square[1]);
    return String::from_utf8(res).unwrap();
}

// clockwise
fn rotate_3(square: String) -> String {
    let square = square.as_bytes();
    let mut res: Vec<u8> = Vec::new();
    res.push(square[6]);
    res.push(square[3]);
    res.push(square[0]);
    res.push(square[7]);
    res.push(square[4]);
    res.push(square[1]);
    res.push(square[8]);
    res.push(square[5]);
    res.push(square[2]);
    return String::from_utf8(res).unwrap();
}

fn flip_2_v(square: String) -> String {
    let square = square.as_bytes();
    let mut res: Vec<u8> = Vec::new();
    res.push(square[2]);
    res.push(square[3]);
    res.push(square[0]);
    res.push(square[1]);
    return String::from_utf8(res).unwrap();
}

fn flip_3_v(square: String) -> String {
    let square = square.as_bytes();
    let mut res: Vec<u8> = Vec::new();
    res.push(square[6]);
    res.push(square[7]);
    res.push(square[8]);
    res.push(square[3]);
    res.push(square[4]);
    res.push(square[5]);
    res.push(square[0]);
    res.push(square[1]);
    res.push(square[2]);
    return String::from_utf8(res).unwrap();
}

fn enhance_2(square: &Vec<Vec<char>>, rules: &HashMap<String,String>) -> Vec<Vec<char>> {
    let mut res: Vec<Vec<char>> = Vec::new();
    // fill res with empty vectors
    for _i in 0..square.len()+(square.len()/2) {
        res.push(Vec::new());
    }
    let mut row = 0;
    let mut new_row = 0;
    while row < square.len() {
        let mut col = 0;
        while col < square[row].len() {
            // Construct 2x2 square
            let mut tmp = String::new();
            for r in 0..2 {
                for c in 0..2 {
                    tmp.push(square[row+r][col+c]);
                }
            }
            // println!("{:?}", tmp);
            // Three rotates
            let mut rot_count = 0;
            while !rules.contains_key(tmp.as_str()) && rot_count < 3{
                tmp = rotate_2(tmp);
                rot_count += 1;
            }
            // One flip
            if !rules.contains_key(tmp.as_str()) {
                tmp = flip_2_v(tmp);
            }
            // Three rotates again
            rot_count = 0;
            while !rules.contains_key(tmp.as_str()) && rot_count < 3 {
                tmp = rotate_2(tmp);
                rot_count += 1;
            }
            let new_square = rules.get(tmp.as_str()).unwrap();
            let new_square: Vec<&str> = new_square.split('/').collect();
            // now push rule lookup to res
            for r in 0..new_square.len() {
                for c in new_square[r].chars() {
                    res[new_row+r].push(c);
                }
            }

            col += 2;
        }
        row += 2;
        new_row += 3;
    }
    return res;
}

fn enhance_3(square: &Vec<Vec<char>>, rules: &HashMap<String,String>) -> Vec<Vec<char>> {
    let mut res: Vec<Vec<char>> = Vec::new();
    // fill res with empty vectors
    for _i in 0..square.len()+(square.len()/3) {
        res.push(Vec::new());
    }
    let mut row = 0;
    let mut new_row = 0;
    while row < square.len() {
        let mut col = 0;
        while col < square[row].len() {
            // Construct 3x3 square
            let mut tmp = String::new();
            for r in 0..3 {
                for c in 0..3 {
                    tmp.push(square[row+r][col+c]);
                }
            }
            // println!("{:?}", tmp);
            // Three rotates
            let mut rot_count = 0;
            while !rules.contains_key(tmp.as_str()) && rot_count < 3{
                tmp = rotate_3(tmp);
                rot_count += 1;
            }
            // One flip
            if !rules.contains_key(tmp.as_str()) {
                tmp = flip_3_v(tmp);
            }
            // Three rotates again
            rot_count = 0;
            while !rules.contains_key(tmp.as_str()) && rot_count < 3 {
                tmp = rotate_3(tmp);
                rot_count += 1;
            }
            let new_square = rules.get(tmp.as_str()).unwrap();
            let new_square: Vec<&str> = new_square.split('/').collect();
            // now push rule lookup to res
            for r in 0..new_square.len() {
                for c in new_square[r].chars() {
                    res[new_row+r].push(c);
                }
            }

            col += 3;
        }
        row += 3;
        new_row += 4;
    }
    return res;
}

fn print_square(square: &Vec<Vec<char>>) {
    for row in square.iter() {
        println!("{:?}", row);
    }
    println!("");
}

fn count_on(square: &Vec<Vec<char>>) -> usize {
    let mut count = 0;
    for row in square.iter() {
        for ch in row.iter() {
            if *ch == '#' { count += 1; }
        }
    }
    return count;
}

fn main() {
    let rules = make_rules();
    let mut square: Vec<Vec<char>> = Vec::new();
    square.push(['.','#','.'].to_vec());
    square.push(['.','.','#'].to_vec());
    square.push(['#','#','#'].to_vec());
    print_square(&square);
    // all combos with org + 3 rotate + flip + 3 rotate
    let mut iterations = 0;
    while iterations < 18 {
        if square.len() % 2 == 0 {
            square = enhance_2(&square, &rules);
        }
        else if square.len() % 3 == 0 {
            square = enhance_3(&square, &rules);
        }
        iterations += 1;
        print_square(&square);
    }
    println!("{:?}", count_on(&square));
}
