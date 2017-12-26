use std::io;
use std::collections::HashMap;

fn set(registers: &mut HashMap<String,i64>, register: String, value: i64) {
    let current = registers.entry(register).or_insert(0);
    *current = value;
}

fn sub(registers: &mut HashMap<String,i64>, register: String, value: i64) {
    let current = registers.entry(register).or_insert(0);
    *current -= value;
}

fn mul(registers: &mut HashMap<String,i64>, register: String, value: i64) {
    let current = registers.entry(register).or_insert(0);
    *current *= value;
}

// return how many steps to jump if register[val] > 0
fn jnz(registers: &mut HashMap<String,i64>, register: String, jmp: i64) -> i64 {
    let value = get_value(registers, register);
    if value != 0 {
        return jmp;
    } else {
        return 1;
    }
}

#[allow(unused_assignments)]
fn get_value(registers: &mut HashMap<String,i64>, value: String) -> i64 {
    let is_digit = value.parse::<i64>();
    let mut res: i64 = 0;
    // if number
    if !is_digit.is_err() {
        res = value.parse().unwrap();
    } else { // if reg
        res = *registers.entry(String::from(value)).or_insert(0);
    }
    return res;
}

fn parse_instruction(instruction: &String, registers: &mut HashMap<String,i64>) -> (String,String,i64) {
    let args: Vec<&str> = instruction.split(' ').collect();
    let cmd = String::from(args[0]);
    let reg = String::from(args[1]);
    let mut value: i64 = 0;
    if args.len() > 2 {
        value = get_value(registers, String::from(args[2]));
    }
    return (cmd,reg,value);
}

// executes instruction and return new program_counter offset
fn execute_instruction(instruction: &String, registers: &mut HashMap<String,i64>) -> i64 {
    let mut pc_offset = 0;
    let args: (String,String,i64) = parse_instruction(instruction,registers);
    let cmd = args.0;
    let reg = args.1;
    let value = args.2;
    // execute cmd
    match cmd.as_str() {
        "set" => { set(registers, reg, value); pc_offset+=1; },
        "sub" => { sub(registers, reg, value); pc_offset+=1; },
        "mul" => { mul(registers, reg, value); pc_offset+=1; },
        "jnz" => { pc_offset += jnz(registers, reg, value); },
        _     => println!("cmd error"),
    }
    return pc_offset;
}

fn read_instructions() -> Vec<String> {
    let mut instructions: Vec<String> = Vec::new();
    loop {
        let mut line = String::new();
        io::stdin().read_line(&mut line).
            expect("Failed to read input");
        // eof
        if line == "" { break; }
        // add to list
        instructions.push(String::from(line.trim()));
    }
    return instructions;
}

#[allow(dead_code)]
fn execute_instructions() {
    let instructions = read_instructions();
    let mut registers: HashMap<String,i64> = HashMap::new();
    let mut pc: i64 = 0;
    let mut mul_count = 0;
    while pc >= 0 && pc < instructions.len() as i64 {
        if parse_instruction(&instructions[pc as usize],&mut registers).0 == "mul" {
            mul_count += 1;
        }
        pc += execute_instruction(&instructions[pc as usize], &mut registers);
    }
    println!("{:?}", mul_count);
}

// returns h reg content
// fn execute_optimized_assembly() -> i64 {
//     // registers
//     // let mut a: i64 = 1;
//     let mut b: i64 = 65*100+100000;
//     let mut c: i64 = 65*100+100000+17000;
//     let mut d: i64 = 0;
//     let mut e: i64 = 0;
//     let mut f: i64 = 0;
//     let mut g: i64 = 0;
//     let mut h: i64 = 0;
//     // // 0,1
//     // b = 65;
//     // c = b;
//     // // 2 -> 7
//     // if a != 0 {
//     //     b *= 100;
//     //     b += 100000;
//     //     c = b;
//     //     c += 17000;
//     // }
//     loop {
//         // 8 -> 9
//         f = 1;
//         d = 2;
//         loop {
//             // 10
//             e = 2;
//             // 11 -> 19
//             loop {
//                 // g = d;
//                 // g *= e;
//                 // g -= b;
//                 g = d*e-b;
//                 if g == 0 { f = 0; }
//                 e += 1;
//                 // g = e;
//                 // g -= b;
//                 g = e-b;
//                 if g == 0 { break; }
//             }
//             // 20 -> 23
//             d += 1;
//             // g = d;
//             // g -= b;
//             g = d-b;
//             if g == 0 { break; }
//         }
//         // 24, 25
//         if f == 0 { h += 1; }
//         // 26, 27
//         // g = b;
//         // g -= c;
//         g = b-c;
//         // 28
//         if g == 0 { return h; }
//         // 30
//         b += 17;
//     }
// }

// returns amount of products that can be factored into 2 nrs
// in set start+step*n for all n where product <= end
fn count_factors(start: i64, end: i64, step: i64) -> i64 {
    let mut b = start;
    let mut h = 0; //
    while b <= end {
        for d in 2..b {
            if b % d == 0 { // d divides b -> d*b/d=b where b/d is int
                h += 1;
                break;
            }
        }
        b += step;
    }
    return h;
}

fn main() {
    // execute_instructions(); // part one
    println!("{:?}", count_factors(106500,106500+17000,17));
}
