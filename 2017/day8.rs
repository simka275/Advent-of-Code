use std::io;
use std::cmp;
use std::collections::HashMap;

fn find_max(registers: &HashMap<String,i32>) -> i32 {
    let mut max = i32::min_value();
    for val in registers.values() {
        max = cmp::max(max,*val);
    }
    return max
}

fn main() {
    let mut registers: HashMap<String,i32> = HashMap::new();
    let mut max = i32::min_value();
    loop {
        let mut line = String::new();
        io::stdin().read_line(&mut line)
            .expect("Failed to read input");

        // end case
        if line == "" { break; }
        // into vector where 0: reg, 1: op, 2: val, 3: if, 4: reg, 5: cmp, 6: val
        let line: Vec<&str> = line.trim().split(' ').collect();
        // println!("{:?}", line);

        // Arguments
        let reg = String::from(line[0]);
        registers.entry(reg.clone()).or_insert(0); // Insert reg if not exist
        let op = String::from(line[1]);
        let mut op_val: i32 = line[2].parse().unwrap();
        let cmp_reg = String::from(line[4]);
        registers.entry(cmp_reg.clone()).or_insert(0); // Insert reg if not exist
        let cmp_reg_val = registers.get(cmp_reg.as_str()).unwrap().clone();
        let cmp = String::from(line[5]);
        let cmp_val: i32 = line[6].parse().unwrap();

        // inc/dec
        if op.as_str() == "dec" {
            op_val *= -1;
        }

        // cmp
        match cmp.as_str() {
            "==" => if cmp_reg_val == cmp_val { *registers.entry(reg.clone()).or_insert(0) += op_val; },
            "!=" => if cmp_reg_val != cmp_val { *registers.entry(reg.clone()).or_insert(0) += op_val; },
            "<"  => if cmp_reg_val < cmp_val { *registers.entry(reg.clone()).or_insert(0) += op_val; },
            "<=" => if cmp_reg_val <= cmp_val { *registers.entry(reg.clone()).or_insert(0) += op_val; },
            ">"  => if cmp_reg_val > cmp_val { *registers.entry(reg.clone()).or_insert(0) += op_val; },
            ">=" => if cmp_reg_val >= cmp_val { *registers.entry(reg.clone()).or_insert(0) += op_val; },
            _ => println!("cmp err"),
        }
        // println!("{:?}", registers);
        max = cmp::max(max,find_max(&registers));
    }
    // Part one
    // let final_max = find_max(&registers);
    // println!("{}", final_max);
    // Part two
    println!("{:?}", max);
}
