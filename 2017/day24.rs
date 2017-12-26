use std::io;
use std::cmp;
use std::collections::HashSet;

fn read_connections() -> HashSet<(u32,u32)> {
    let mut connections: HashSet<(u32,u32)> = HashSet::new();
    loop {
        let mut connection = String::new();
        io::stdin().read_line(&mut connection).
            expect("Failed to read input");
        // eof
        if connection.is_empty() { break; }
        let connection: Vec<u32> = connection.trim().split('/').map(|n| n.parse::<u32>().unwrap()).collect();
        connections.insert((connection[0],connection[1]));
    }
    return connections;
}

fn max_strength(pins: u32, connections: HashSet<(u32,u32)>) -> u32 {
    let mut max = 0;
    // calc strength for all possible connections
    for con in connections.iter() {
        let mut subset_connections = connections.clone();
        if con.0 == pins {
            subset_connections.remove(con);
            max = cmp::max(max,con.0+con.1+max_strength(con.1,subset_connections));
        } else if con.1 == pins {
            subset_connections.remove(con);
            max = cmp::max(max,con.0+con.1+max_strength(con.0,subset_connections));
        }
    }
    return max;
}

fn calc_bridge_strength(bridge: &Vec<(u32,u32)>) -> u32 {
    let mut res = 0;
    for con in bridge.iter() {
        res += con.0;
        res += con.1;
    }
    return res;
}

fn gen_max_bridge(pins: u32, connections: HashSet<(u32,u32)>) -> Vec<(u32,u32)> {
    let mut max_bridge: Vec<(u32,u32)> = Vec::new();
    for con in connections.iter() {
        let mut subset_connections = connections.clone();
        if con.0 == pins || con.1 == pins {
            let mut bridge: Vec<(u32,u32)> = Vec::new();
            subset_connections.remove(con);
            if con.0 == pins {
                bridge = gen_max_bridge(con.1,subset_connections);
            } else if con.1 == pins {
                bridge = gen_max_bridge(con.0,subset_connections);
            }
            bridge.push(*con);
            if bridge.len() > max_bridge.len() {
                max_bridge = bridge;
            } else if bridge.len() == max_bridge.len() {
                if calc_bridge_strength(&bridge) > calc_bridge_strength(&max_bridge) {
                    max_bridge = bridge;
                }
            }
        }
    }
    return max_bridge;
}

fn main() {
    let connections = read_connections();
    // println!("{:?}", connections);
    // println!("{:?}", max_strength(0,connections)); // part one
    println!("{:?}", calc_bridge_strength(&gen_max_bridge(0,connections)));
}
