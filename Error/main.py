from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
import numpy as np

def string_to_binary(s):
    return ''.join(format(ord(i), '08b') for i in s)

def quantum_hash(input_bin):
    n = len(input_bin)
    qc = QuantumCircuit(n, n)
    
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
    result = execute(qc, backend,shots=100000).result()
    counts = result.get_counts(qc)
    hash_result = max(counts, key=counts.get)
    
    return hash_result

def compute_quantum_hashes(strings):
    hashes = {}
    for s in strings:
        binary_repr = string_to_binary(s)
        qhash = quantum_hash(binary_repr)
        hashes[s] = qhash
    return hashes

def test_quantum_hashes():
    """
    Test the compute_quantum_hashes function and print the hash results.
    """
    strings = ["Ab", "Sujeet", "MIT"]
    hashes = compute_quantum_hashes(strings)
    for s, h in hashes.items():
        print(f"String: {s} | Quantum Hash: {h}")
    print("------")  # Just for separation between outputs

# Call the test function thrice
for _ in range(3):
    test_quantum_hashes()
