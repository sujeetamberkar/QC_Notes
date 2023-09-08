
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
import numpy as np
import random
import string

def string_to_binary(s):
    return ''.join(format(ord(i), '08b') for i in s)

def quantum_hash(input_bin, shots=4096):  # Increased shots for more deterministic results
    n = 32
    qc = QuantumCircuit(n, n)
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
    result = execute(qc, backend, shots=shots).result()
    counts = result.get_counts(qc)
    hash_result = max(counts, key=counts.get)
    
    return hash_result

class Block:
    def __init__(self, transactions, previous_hash=""):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.hash = self.compute_hash()
    
    def compute_hash(self):
        content = str(self.transactions) + self.previous_hash + self.salt
        return quantum_hash(string_to_binary(content))

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        
    def create_genesis_block(self):
        return Block(transactions="Genesis Block")
    
    def add_block(self, transactions):
        previous_hash = self.chain[-1].hash
        new_block = Block(transactions, previous_hash)
        self.chain.append(new_block)
    
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.compute_hash():
                print("Invalid block hash detected at block", i)
                print("Current hash:", current_block.hash)
                print("Computed hash:", current_block.compute_hash())
                return False
            
            if current_block.previous_hash != previous_block.hash:
                print("Invalid previous hash detected at block", i)
                print("Previous hash:", current_block.previous_hash)
                print("Expected:", previous_block.hash)
                return False
        
        return True

# Sample usage
my_blockchain = Blockchain()
my_blockchain.add_block(transactions={"sender": "Alice", "receiver": "Bob", "amount": 10})
my_blockchain.add_block(transactions={"sender": "Bob", "receiver": "Charlie", "amount": 5})

if my_blockchain.is_valid():
    print("Blockchain is valid!")
else:
    print("Blockchain is invalid!")
