# Importing necessary modules from Qiskit and numpy.
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
import numpy as np

def string_to_binary(s):
    """
    Convert a string to its binary representation.
    
    Parameters:
    - s (str): The input string to be converted.
    
    Returns:
    - str: Binary representation of the input string.
    """
    # Convert each character in the string to its ASCII value, then to 8-bit binary.
    # Concatenate all these binary strings together.
    return ''.join(format(ord(i), '08b') for i in s)

def quantum_hash(input_bin):
    """
    Compute a quantum hash of the binary input.
    
    Parameters:
    - input_bin (str): Binary representation of the input string.
    
    Returns:
    - str: Quantum hash value.
    """
    # Number of qubits is determined by the length of the binary input.
    n = len(input_bin)
    
    # Initialize a quantum circuit with n qubits and n classical bits.
    qc = QuantumCircuit(n, n)
    
    # Set initial state of the quantum circuit based on the binary input.
    # If a bit in the binary string is '1', flip the corresponding qubit using the X-gate.
    for i, bit in enumerate(input_bin):
        if bit == '1':
            qc.x(i)
    
    # Create a superposition by applying a Hadamard gate to each qubit.
    for i in range(n):
        qc.h(i)
    
    # Introduce a phase shift of pi/4 to each qubit state.
    for i in range(n):
        qc.p(np.pi/4, i)
    
    # Apply controlled operations for entangling qubits and introducing non-linearity.
    if n > 1:
        qc.cx(0, 1)
        if n > 2:
            qc.ccx(0, 1, 2)  # Apply Toffoli gate on first three qubits if there are at least 3 qubits.
    
    # Measure the state of each qubit.
    qc.measure(range(n), range(n))
    
    # Use Aer's qasm_simulator for simulating the quantum circuit.
    backend = Aer.get_backend('qasm_simulator')
    
    # Transpile and assemble the quantum circuit for execution.
    t_qc = transpile(qc, backend)
    qobj = assemble(t_qc)
    
    # Execute the circuit and retrieve the results.
    result = execute(qc, backend).result()
    counts = result.get_counts(qc)
    
    # The hash value is the most frequently observed output state.
    hash_result = max(counts, key=counts.get)
    
    return hash_result

def compute_quantum_hashes(strings):
    """
    Compute quantum hashes for a list of strings.
    
    Parameters:
    - strings (list): List of input strings to be hashed.
    
    Returns:
    - dict: Dictionary with strings as keys and their corresponding quantum hashes as values.
    """
    # Dictionary to store quantum hashes for each string.
    hashes = {}
    
    for s in strings:
        # Convert string to binary.
        binary_repr = string_to_binary(s)
        
        # Compute quantum hash for the binary representation.
        qhash = quantum_hash(binary_repr)
        
        # Store the hash in the dictionary.
        hashes[s] = qhash
    
    return hashes

# Sample execution with input strings.
strings = ["Ab", "Sujeet", "MIT"]
hashes = compute_quantum_hashes(strings)

for s, h in hashes.items():
    print(f"String: {s} | Quantum Hash: {h}")
