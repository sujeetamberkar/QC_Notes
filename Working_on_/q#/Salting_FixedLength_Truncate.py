from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
import numpy as np
import random
import string

def string_to_binary(s):
    return ''.join(format(ord(i), '08b') for i in s)

def quantum_hash(input_bin):
    n = 32  # Fixed number of qubits for a consistent hash length.
    qc = QuantumCircuit(n, n)

    # If input binary length is greater than n, we'll truncate it.
    # If it's less than n, we'll pad it with zeros.
    input_bin = (input_bin + '0'*n)[:n]

    for i, bit in enumerate(input_bin):
        if bit == '1':
            qc.x(i)
    
    for i in range(n):
        qc.h(i)
    
    for i in range(n):
        qc.p(np.pi/4, i)
    
    if n > 1:
        qc.cx(0, 1)
        if n > 2:
            qc.ccx(0, 1, 2)

    qc.measure(range(n), range(n))
    
    backend = Aer.get_backend('qasm_simulator')
    t_qc = transpile(qc, backend)
    qobj = assemble(t_qc)
    result = execute(qc, backend).result()
    counts = result.get_counts(qc)
    hash_result = max(counts, key=counts.get)
    
    return hash_result

def compute_quantum_hashes(strings):
    hashes = {}
    
    for s in strings:
        # Generate a random salt of length 8.
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # Convert string concatenated with salt to binary.
        binary_repr = string_to_binary(s + salt)
        
        qhash = quantum_hash(binary_repr)
        
        # Store the hash and the salt in the dictionary.
        hashes[s] = {'hash': qhash, 'salt': salt}
    
    return hashes

strings = ["My name is SUjeet Sanjay Amberkar", "Sujeet", "MIT"]
hashes = compute_quantum_hashes(strings)

for s, h in hashes.items():
    print(f"String: {s} | Salt: {h['salt']} | Quantum Hash: {h['hash']}")

