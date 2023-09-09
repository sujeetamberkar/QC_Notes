# Quantum Salted Hashing
This module offers functionalities to utilize quantum properties for generating salt values which are then used for creating SHA-512 hashes. The core principle behind the code is Quantum Key Distribution (QKD), a method by which cryptographic keys can be shared securely using quantum mechanics. In this implementation, this property is leveraged to produce unique salts to improve security.

## Requirements:
Python (3.x recommended)
Qiskit library

## How to Install Qiskit:
To install the required Qiskit library, you can use pip:

```
pip install qiskit

```

## Features:

1) prepare_qubit(bit, basis)
    Prepares a qubit based on the given bit and basis.
    bit: 0 or 1, represents the bit value.
    basis: '+' or 'x', represents the measurement basis.
    
2) measure_qubit(qc, basis)
    Measures the qubit in the given basis.
    qc: A QuantumCircuit containing the qubit.
    basis: '+' or 'x', the measurement basis.
3) generate_binary_key()
    Generates a binary key using Quantum Key Distribution.

4) binary_to_hex(binary_key)
    Converts a binary key to its hex representation.
    binary_key: The binary key as a list of 0's and 1's.
5) generate_key()
    Generates a salt key using Quantum Key Distribution and converts it to hexadecimal.
6) hashing(plainText, salt=None)
    Generates a SHA-512 hash of the provided plainText, salted with the provided salt. If no salt is provided, a quantum-generated salt is used.
    plainText: The text to be hashed.
    salt: The salt to use. If not provided, a new quantum-generated salt is created.
7) check_hashing(plainText, salt)
    Generates a SHA-512 hash for the provided plainText using the given salt.
    plainText: The text to be hashed.
    salt: The salt to use for hashing.

### Author
Sujeet Amberkar

