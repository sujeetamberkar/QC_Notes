import socket
import random
import time
from qiskit import QuantumCircuit, Aer, execute

def prepare_qubit(bit, basis):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == 'x':
        qc.h(0)
    return qc

def serialize_qubit(qc):
    qasm_str = qc.qasm()
    return qasm_str.encode('utf-8')

def main():
    num_bits = 20 ## Length of the key depends on num_bits, it will always be less that num_bits most probably num_bits/2

    alice_bits = [random.choice([0, 1]) for _ in range(num_bits)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]

    alice_qubits = []
    for i in range(len(alice_bits)):
        bit = alice_bits[i]
        basis = alice_bases[i]
        prepared_qubit = prepare_qubit(bit, basis)
        alice_qubits.append(prepared_qubit)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12331))

        # Step 2: Alice sends her qubits to Bob
        for qc in alice_qubits:
            data = serialize_qubit(qc)
            s.sendall(data)
            time.sleep(0.1)  # small delay to ensure Bob has time to process each qubit
            s.recv(1)  # wait for Bob's acknowledgement

        # Step 4: Alice sends her bases to Bob and receives Bob's bases
        s.sendall(''.join(alice_bases).encode('utf-8'))
        bob_bases = s.recv(num_bits).decode('utf-8')

    matching_bases = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            matching_bases.append(i)

    alice_key = []
    for i in matching_bases:
        alice_key.append(alice_bits[i])
    print("Alice's key:", alice_key)



    



if __name__ == '__main__':
    main()
