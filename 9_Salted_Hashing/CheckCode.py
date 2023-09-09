from hashlib import sha512
import random
from qiskit import QuantumCircuit, Aer, execute

def prepare_qubit(bit, basis):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == 'x':
        qc.h(0)
    return qc

def measure_qubit(qc, basis):
    if basis == 'x':
        qc.h(0)
    qc.measure(0, 0)
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1, memory=True)
    result = job.result()
    return int(result.get_memory()[0])

def generate_binary_key():
    num_bits = 256

    alice_bits = [random.choice([0, 1]) for _ in range(num_bits)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
    alice_qubits = [prepare_qubit(alice_bits[i], alice_bases[i]) for i in range(num_bits)]

    bob_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
    bob_bits = [measure_qubit(alice_qubits[i], bob_bases[i]) for i in range(num_bits)]

    shared_key = [alice_bits[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]

    while len(shared_key) < 128:
        additional_key = generate_binary_key()
        shared_key.extend(additional_key)

    return shared_key[:128]

def binary_to_hex(binary_key):
    binary_str = ''.join(map(str, binary_key))
    return hex(int(binary_str, 2))[2:].upper()

def generate_key():
    binary_key = generate_binary_key()
    return binary_to_hex(binary_key)

def hashing(plainText,salt=None):
    if salt is None:
        salt=generate_key()
    hash_value=sha512((str(salt)+plainText).encode()).hexdigest()
    return salt, hash_value

def check_hashing(plainText,salt):
    hash_value=sha512((str(salt)+plainText).encode()).hexdigest()
    return hash_value

if __name__ == '__main__':
    salt_value1,hash_value1=hashing("Sujet")
    print("Salt Value ",salt_value1)
    print("Hash Value ", hash_value1,'\n')
    salt_value2,hash_value2=hashing("Sujet")
    print("Salt Value ",salt_value2)
    print("Hash Value ", hash_value2,'\n')


    chechHash1=check_hashing("Sujeet",salt_value1)
    checkHash2=check_hashing("Sujeet",salt_value1)
    print("Check Hashing")
    print(chechHash1)
    print(checkHash2)