use std::io;
use std::collections::HashMap;

struct Node {
    name: String,
    weight: i32,
    parent: String,
    children: Vec<String>,
}

fn create_tree() -> HashMap<String,Node> {
    let mut nodes: HashMap<String,Node> = HashMap::new();
    // Read all nodes
    loop {
        let mut line = String::new();
        io::stdin().read_line(&mut line)
            .expect("Failed to read input");
        // End case
        if line == "" { break; }
        // do
        let node: Vec<&str> = line.trim().split(" ").collect();
        let name = node[0];
        // Remove brackets and parse to integer
        let weight: i32 = node[1][1..node[1].len()-1].parse().unwrap();
        // Add children to children list if node has any
        let mut children: Vec<String> = Vec::new();
        if node.len() > 3 {
            for i in 3..node.len() {
                // Remove ',' and add to children list
                children.push(node[i].split(',').collect());
            }
        }

        // If node exist update info else create node
        if nodes.contains_key(name) {
            nodes.get_mut(name).unwrap().weight = weight;
            nodes.get_mut(name).unwrap().children = children.clone();
        } else {
            let node = Node {
                name: String::from(name),
                weight,
                parent: String::from(""),
                children: children.clone(),
            };
            nodes.insert(String::from(node.name.as_str()),node);
        }

        // If node has children update/create children
        for child in children {
            if nodes.contains_key(child.as_str()) {
                nodes.get_mut(child.as_str()).unwrap().parent = String::from(name);
            } else {
                let node = Node {
                    name: child,
                    weight: 0,
                    parent: String::from(name),
                    children: Vec::new()
                };
                nodes.insert(String::from(node.name.as_str()),node);
            }
        }
    }
    return nodes;
}

fn find_root(nodes: &HashMap<String,Node>) -> &str {
    // Start at first node in node collection
    let mut current_node = nodes.values().nth(0).unwrap();
    while current_node.parent != "" {
        current_node = nodes.get(current_node.parent.as_str()).unwrap();
    }
    return current_node.name.as_str();
}

fn calc_weight(nodes: &HashMap<String,Node>, name: &str) -> i32 {
    let current_node = nodes.get(name).unwrap();
    // Base case
    if current_node.children.is_empty() {
        return current_node.weight;
    } else {
        let mut weight = current_node.weight;
        for child in current_node.children.clone() {
            weight += calc_weight(&nodes, child.as_str()    );
        }
        return weight;
    }
}

// Return name and weight diff of differing node
fn find_unique(node_weights: &Vec<(String,i32)>) -> (String,i32) {
    let mut unique_node = (String::from("error"),0);
    for node in node_weights.clone() {
        let mut diff_count = 0;
        for neighbor in node_weights.clone() {
            let diff = node.1-neighbor.1;
            if diff != 0 {
                diff_count += 1;
            }
            if diff_count > 1 {
                unique_node = (node.0.clone(),diff);
            }
        }
    }
    return unique_node;
}

// Returns name and weight diff of unbalanced
fn find_unbalanced(nodes: &HashMap<String,Node>) -> (String,i32) {
    let mut current_node = nodes.get(find_root(&nodes)).unwrap();
    let mut unbalanced_node = (String::from("error"),0);
    // Start at root and go down the unbalanced branch
    loop {
        // Calculate weights of all children
        let mut children_weights: Vec<(String,i32)> = Vec::new();
        for child in current_node.children.clone() {
            children_weights.push((child.clone(),calc_weight(&nodes, child.as_str())))
        }

        // If no unique node than current unbalanced_node is source of error
        // else traverse down the tree to unbalanced child
        if find_unique(&children_weights).1 == 0 {
            break;
        } else {
            unbalanced_node = find_unique(&children_weights);
            current_node = nodes.get(unbalanced_node.0.as_str()).unwrap();
        }
    }
    return unbalanced_node;
}

fn main() {
    // Contains all nodes with name as key
    let nodes: HashMap<String,Node> = create_tree();

    // for node in nodes.values() {
    //     println!("n:{}, p:{}, c:{:?} ", node.name, node.parent, node.children);
    // }
    // println!("node:{}, w:{}", find_root(&nodes), calc_weight(&nodes, find_root(&nodes)));

    // println!("{:?}", find_root(nodes)); // part one

    // part two
    let unbalanced = find_unbalanced(&nodes);
    println!("{:?}", nodes.get(unbalanced.0.as_str()).unwrap().weight-unbalanced.1);
}
