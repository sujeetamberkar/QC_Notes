from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
import numpy as np

def string_to_binary(s):
    """Convert a string to its 8-bit binary representation."""
    return ''.join(format(ord(char), '08b') for char in s)

def quantum_hash(input_bin, shots=1024):
    """Compute a quantum hash of the binary input."""
    n = len(input_bin)
    
    # Create the quantum circuit.
    qc = QuantumCircuit(n, n)

    # Initialize qubits based on the input string.
    for i, bit in enumerate(input_bin):
        if bit == '1':
            qc.x(i)

    # Apply Hadamard gates to create superposition.
    qc.h(range(n))

    # Introduce a phase shift.
    qc.p(np.pi/4, range(n))

    # Entangle qubits for non-linearity.
    if n > 1:
        qc.cx(0, 1)
        if n > 2:
            qc.ccx(0, 1, 2)
    
    # Measure the qubits.
    qc.measure(range(n), range(n))
    
    # Execute the quantum circuit.
    backend = Aer.get_backend('qasm_simulator')
    t_qc = transpile(qc, backend)
    qobj = assemble(t_qc, shots=shots)
    result = execute(qc, backend, shots=shots).result()
    counts = result.get_counts()

    # Return the most frequently observed state.
    return max(counts, key=counts.get)

def compute_quantum_hashes(strings):
    """Compute and return quantum hashes for a list of strings."""
    return {s: quantum_hash(string_to_binary(s)) for s in strings}

# Test the function.
strings = ["Ab", "Sujeet", "MIT"]
hashes = compute_quantum_hashes(strings)

for s, h in hashes.items():
    print(f"String: {s} | Quantum Hash: {h}")
