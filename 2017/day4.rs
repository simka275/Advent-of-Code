use std::io;
use std::collections::HashSet;

/*
fn is_valid_passphrase(passphrase: String) -> bool {
    let mut passwords: HashSet<&str> = HashSet::new();
    let passphrase: Vec<&str> = passphrase.trim().split(' ').collect();
    // Check if word in set if true then return false else check next
    for word in passphrase {
        if passwords.contains(word) {
            return false;
        }
        passwords.insert(word);
    }
    return true;
}

fn part_one() {
    let mut valid_passphrases = 0;
    loop {
        let mut passphrase = String::new();
        io::stdin().read_line(&mut passphrase)
            .expect("Failed to read input");
        // Break if no line read
        if passphrase == "" { break; }

        if is_valid_passphrase(passphrase) {
            valid_passphrases += 1;
        }
    }
    println!("{}", valid_passphrases);
}
*/

fn sort_word(word: String) -> String {
    // Sort word
    let mut sorted_word: Vec<char> = word.chars().collect();
    sorted_word.sort();
    let sorted_word = sorted_word.into_iter().collect();
    return sorted_word;
}

fn no_anagrams(passphrase: String) -> bool {
    let mut passwords: HashSet<String> = HashSet::new();
    let passphrase: Vec<String> = passphrase.trim().split(' ').map(|w| sort_word(String::from(w))).collect();
    for word in passphrase {
        if passwords.contains(word.as_str()) {
            return false;
        }
        passwords.insert(word);
    }
    return true;
}

fn part_two() {
    let mut valid_passphrases = 0;
    loop {
        let mut passphrase = String::new();
        io::stdin().read_line(&mut passphrase)
            .expect("Failed to read input");
        // Break if no line read
        if passphrase == "" { break; }

        if no_anagrams(passphrase) {
            valid_passphrases += 1;
        }
    }
    println!("{}", valid_passphrases);
}

fn main() {
    // part_one();
    part_two();
}
