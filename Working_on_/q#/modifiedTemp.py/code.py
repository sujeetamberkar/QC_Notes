from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
import hashlib

def string_to_binary(s):
    """
    Convert a string to its binary representation.
    """
    return ''.join(format(ord(i), '08b') for i in s)

def quantum_process(input_bin):
    """
    A deterministic quantum process that generates a value based on input.
    """
    n = len(input_bin)
    
    qc = QuantumCircuit(n)
    
    for i, bit in enumerate(input_bin):
        if bit == '1':
            qc.x(i)
    
    qc.h(range(n))
    
    backend = Aer.get_backend('statevector_simulator')
    t_qc = transpile(qc, backend)
    qobj = assemble(t_qc)
    statevector = execute(qc, backend).result().get_statevector()
    
    # Convert the statevector into a deterministic seed
    # Here, we'll just use the squared magnitude of the first entry, ensuring it's deterministic
    magnitude_squared = abs(statevector[0])**2
    seed = int(magnitude_squared * 1e6)  # Convert it to a larger integer for better seeding
    
    return seed

def classical_hash(input_str, seed):
    """
    A deterministic hash function that uses a seed value.
    """
    hasher = hashlib.sha256()
    hasher.update(input_str.encode('utf-8'))
    hasher.update(str(seed).encode('utf-8'))  # Incorporate the seed into the hash
    return hasher.hexdigest()

def quantum_inspired_hash(input_str):
    input_bin = string_to_binary(input_str)
    seed = quantum_process(input_bin)
    return classical_hash(input_str, seed)

# Test
input_strings = ["Alice", "Bob", "Charlie"]
for s in input_strings:
    print(f"String: {s} | Quantum-Inspired Hash: {quantum_inspired_hash(s)}")
