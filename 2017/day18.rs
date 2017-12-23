use std::io;
use std::collections::HashMap;
use std::collections::VecDeque;

#[allow(dead_code)]
// return value in register
fn snd(registers: &mut HashMap<String,i64>, register: String) -> i64 {
    return get_value(registers, register);
}

// add reg val to message queue and then return registers value
fn snd_msg(registers: &mut HashMap<String,i64>, register: String, msg_queue: &mut VecDeque<i64>) -> i64 {
    let value = get_value(registers, register);
    msg_queue.push_back(value);
    return value;
}

fn set(registers: &mut HashMap<String,i64>, register: String, value: i64) {
    let current = registers.entry(register).or_insert(0);
    *current = value;
}

fn add(registers: &mut HashMap<String,i64>, register: String, value: i64) {
    let current = registers.entry(register).or_insert(0);
    *current += value;
}

fn mul(registers: &mut HashMap<String,i64>, register: String, value: i64) {
    let current = registers.entry(register).or_insert(0);
    *current *= value;
}

fn modu(registers: &mut HashMap<String,i64>, register: String, value: i64) {
    let current = registers.entry(register).or_insert(0);
    *current = *current % value;
}

fn rcv_msg(registers: &mut HashMap<String,i64>, register: String, msg_queue: &mut VecDeque<i64>) -> i64 {
    let value = msg_queue.pop_front().unwrap();
    registers.insert(register,value);
    return value;
}

// return how many steps to jump if register[val] > 0
fn jgz(registers: &mut HashMap<String,i64>, register: String, jmp: i64) -> i64 {
    let value = get_value(registers, register);
    if value > 0 {
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

#[allow(dead_code)]
// part one
fn execute_instructions(instructions: &Vec<String>) -> i64 {
    let mut registers: HashMap<String,i64> = HashMap::new();
    let mut last_freq = 0;
    let mut i: i64 = 0;
    while i >= 0 && i < instructions.len() as i64 {
        let args: (String,String,i64) = parse_instruction(&instructions[i as usize], &mut registers);
        let cmd = args.0;
        let reg = args.1;
        let value = args.2;
        // execute cmd
        match cmd.as_str() {
            "snd" => { last_freq = snd(&mut registers, reg); i+=1; },
            "set" => { set(&mut registers, reg, value); i+=1; },
            "add" => { add(&mut registers, reg, value); i+=1; },
            "mul" => { mul(&mut registers, reg, value); i+=1; },
            "mod" => { modu(&mut registers, reg, value); i+=1; },
            "rcv" => { i+=1; if *registers.entry(reg).or_insert(0) != 0 { return last_freq; }},
            "jgz" => { if *registers.entry(reg).or_insert(0) > 0 { i += value } else { i+=1; }},
            _     => println!("cmd error"),
        }
    }
    return -1;
}

// executes instruction and return new program_counter offset
fn execute_instruction(instruction: &String, registers: &mut HashMap<String,i64>,
                       snd_queue: &mut VecDeque<i64>, rcv_queue: &mut VecDeque<i64>) -> i64
{
    let mut pc_offset = 0;
    let args: (String,String,i64) = parse_instruction(instruction,registers);
    let cmd = args.0;
    let reg = args.1;
    let value = args.2;
    // if cmd is rcv and rcv_queue is empty than wait i.e. return offset 0
    if cmd == "rcv" && rcv_queue.is_empty() { return 0; }
    // execute cmd
    match cmd.as_str() {
        "snd" => { snd_msg(registers, reg, snd_queue); pc_offset+=1; },
        "set" => { set(registers, reg, value); pc_offset+=1; },
        "add" => { add(registers, reg, value); pc_offset+=1; },
        "mul" => { mul(registers, reg, value); pc_offset+=1; },
        "mod" => { modu(registers, reg, value); pc_offset+=1; },
        "rcv" => { rcv_msg(registers, reg, rcv_queue); pc_offset+=1; },
        "jgz" => { pc_offset += jgz(registers, reg, value); },
        _     => println!("cmd error"),
    }
    return pc_offset;
}

fn main() {
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
    // part one
    println!("{:?}", execute_instructions(&instructions));

    // part two
    // msg queues
    let mut msg_queue_0: VecDeque<i64> = VecDeque::new();
    let mut msg_queue_1: VecDeque<i64> = VecDeque::new();
    // program counters
    let mut pc_0: i64 = 0;
    let mut pc_1: i64 = 0;
    // registers
    let mut registers_0: HashMap<String,i64> = HashMap::new();
    registers_0.insert(String::from("p"),0);
    let mut registers_1: HashMap<String,i64> = HashMap::new();
    registers_1.insert(String::from("p"),1);
    // # sends by prog i
    let mut send_count_0 = 0;
    let mut send_count_1 = 0;

    loop {
        // println!("pc0: {:?}, pc1: {:?}", pc_0, pc_1);
        // println!("ins0: {:?}, ins1: {:?}", &instructions[pc_0 as usize], &instructions[pc_1 as usize]);
        let cmd_0 = parse_instruction(&instructions[pc_0 as usize], &mut registers_0).0;
        let cmd_1 = parse_instruction(&instructions[pc_1 as usize], &mut registers_1).0;
        // part two
        if cmd_0 == "snd" {
            send_count_0 += 1;
        }
        if cmd_1 == "snd" {
            send_count_1 += 1;
        }
        // program 0
        let pc_offset_0 = execute_instruction(&instructions[pc_0 as usize], &mut registers_0,
                                            &mut msg_queue_1, &mut msg_queue_0);

        // program 1
        let pc_offset_1 = execute_instruction(&instructions[pc_1 as usize], &mut registers_1,
                                            &mut msg_queue_0, &mut msg_queue_1);

        // println!("regs0: {:?}, regs1: {:?}", registers_0, registers_1);
        // println!("queue0: {:?}, queue1: {:?} \n", msg_queue_0, msg_queue_1);

        // If both programs are waiting -> deadlock -> break
        if cmd_0 == "rcv" && pc_offset_0 == 0 &&
           cmd_1 == "rcv" && pc_offset_1 == 0 { break; }
        // inc pc
        pc_0 += pc_offset_0;
        pc_1 += pc_offset_1;
        // if pc out of range -> program finished
        let finished_0 = pc_0 < 0 || pc_0 >= instructions.len() as i64;
        let finished_1 = pc_1 < 0 || pc_1 >= instructions.len() as i64;
        // if both finished -> break;
        if finished_0 && finished_1 { break; }
    }
    println!("0: {:?}, 1: {:?}", send_count_0, send_count_1);
}
