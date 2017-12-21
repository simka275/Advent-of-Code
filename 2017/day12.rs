use std::io;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;

fn connected_nodes(graph: &HashMap<i32,Vec<i32>>, start: i32) -> HashSet<i32> {
    let mut visited: HashSet<i32> = HashSet::new(); // Nodes already seen
    let mut unvisited: VecDeque<i32> = VecDeque::new(); // Nodes to visit
    // Start with 0
    unvisited.push_back(start);
    // While still are nodes to visit
    while !unvisited.is_empty() {
        let current = unvisited.pop_front().unwrap(); // Pop queue
        // println!("{:?}", current);
        // If already visited continue to next
        if visited.contains(&current) { continue; }
        // else add to visited
        visited.insert(current);
        // println!("{:?}", visited);
        // Add each neighbor not yet visited to queue
        for neighbor in graph.get(&current).unwrap() {
            if !visited.contains(neighbor) {
                unvisited.push_back(*neighbor);
            }
        }
    }
    return visited;
}

fn main() {
    let mut graph: HashMap<i32,Vec<i32>> = HashMap::new();
    loop {
        let mut line = String::new();
        io::stdin().read_line(&mut line)
        .expect("Failed to read input");
        if line == "" { break; }
        let progs: Vec<&str> = line.trim().split(" <-> ").collect();
        let prog: i32 = progs[0].parse().unwrap();
        let neighbors: Vec<i32> = progs[1].split(',').map(|w| w.trim().parse().unwrap()).collect();
        // println!("{:?}", prog);
        // println!("{:?}", neighbors);
        graph.insert(prog,neighbors);
    }
    // part one
    // println!("{:?}", connected_nodes(graph,0).len());
    // part two
    let mut groups = 0;
    // Go through graph and remove each connected group
    while !graph.is_empty() {
        groups += 1;
        // Get connections from random node still in graph
        let connections = connected_nodes(&graph,*graph.clone().keys().nth(0).unwrap());
        // Remove connected nodes
        for node in connections {
            graph.remove(&node);
        }
    }
    println!("{:?}", groups);
}
