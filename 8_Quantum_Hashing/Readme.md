# Quantum Hashing Program
```
This program provides a quantum simulation-based hashing algorithm. It leverages the Qiskit library to implement a quantum circuit which acts as a hash function. To ensure robust hashing, the program hashes in chunks, ensuring no information is lost for longer strings, and uses a salt for enhanced security.
```

## Installation
```
 1)Ensure you have Python installed.
 2)Install Qiskit:
        pip install qiskit
 3) Clone this repository or copy the Python script to your local machine.
```
## Usage
```
 1) Run the program:
        python3 Code.py
 2)Follow the on-screen prompts. Enter the number of strings you want to hash, and then enter each string one by one.

 3)The program will output the hash and the associated salt for each input string.
```

## Description of Functions
1) string_to_binary(s): Converts a given string into its binary representation.

2) quantum_hash(input_bin): Computes a hash using a quantum circuit for a given binary input of fixed length (32 bits).

3) chunked_quantum_hash(binary_string): Handles binary strings that are longer than 32 bits by dividing them into chunks and hashing each chunk separately.

4) compute_quantum_hashes(strings): Main function to process a list of strings, generate salts, and compute their hashes.

