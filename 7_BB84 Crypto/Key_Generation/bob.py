import socket
import random
from qiskit import QuantumCircuit, Aer, execute

def deserialize_qubit(data):
    qasm_str = data.decode('utf-8')
    qc = QuantumCircuit.from_qasm_str(qasm_str)
    return qc

def measure_qubit(qc, basis):
    if basis == 'x':
        qc.h(0)
    qc.measure(0, 0)
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1, memory=True)
    result = job.result()
    return int(result.get_memory()[0])

def main():
    num_bits = 20 ## Length of the key depends on num_bits, it will always be less that num_bits most probably num_bits/2

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12331))
        s.listen()
        conn, addr = s.accept()

        with conn:
            # Step 3: Bob measures Alice's qubits
            bob_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
            bob_bits = []

            for i in range(num_bits):
                data = conn.recv(1024)
                qc = deserialize_qubit(data)
                bit = measure_qubit(qc, bob_bases[i])
                bob_bits.append(bit)
                conn.sendall(b'1')  # send acknowledgement to Alice

            # Step 4: Bob receives Alice's bases and sends his bases to Alice
            alice_bases = conn.recv(num_bits).decode('utf-8')
            conn.sendall(''.join(bob_bases).encode('utf-8'))

    matching_bases = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            matching_bases.append(i)
    bob_key = []
    for i in matching_bases:
        bob_key.append(bob_bits[i])

    print("Bob's key:", bob_key)

if __name__ == '__main__':
    main()
