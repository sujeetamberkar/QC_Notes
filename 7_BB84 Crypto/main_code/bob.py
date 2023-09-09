import os
import socket
import random
from qiskit import QuantumCircuit, Aer, execute

def deserialize_qubit(data):
    qasm_str = data.decode('utf-8')
    qc = QuantumCircuit.from_qasm_str(qasm_str)
    return qc

def xor_binary_strings(bin_str1, bin_str2):
    if len(bin_str1) != len(bin_str2):
        raise ValueError("Binary strings must be of the same length")

    xor_result = ''.join('1' if bin_str1[i] != bin_str2[i] else '0' for i in range(len(bin_str1)))
    return xor_result

def measure_qubit(qc, basis):
    if basis == 'x':
        qc.h(0)
    qc.measure(0, 0)
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1, memory=True)
    result = job.result()
    return int(result.get_memory()[0])

def binary_to_text(binary_text):
    text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
    return text

def return_port_no():
    l = int(input('Enter Lower Limit:  \n'))
    while l < 5:
        l = int(input('Retry !\nEnter Lower Limit:  \n'))
    u = int(input('Enter Upper Limit: \n'))
    while u < 25:
        u = int(input('Retry !\nEnter Upper Limit: \n'))
    r = 1000 * (u - l) + l
    return r

def main():
    host = 'localhost'
    port = return_port_no()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Bob is waiting for a connection...")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    num_bits = int(conn.recv(1024).decode('utf-8'))
    print(f"Received integer: {num_bits}")

    bob_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
    bob_bits = []

    for i in range(num_bits):
        data = conn.recv(1024)
        qc = deserialize_qubit(data)
        bit = measure_qubit(qc, bob_bases[i])
        bob_bits.append(bit)
        conn.sendall(b'1')  # send acknowledgement to Alice

    alice_bases = conn.recv(1024).decode('utf-8')
    conn.sendall(''.join(bob_bases).encode('utf-8'))

    matching_bases = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            matching_bases.append(i)
    bob_key = []
    for i in matching_bases:
        bob_key.append(bob_bits[i])

    key = bob_key[0:int(num_bits / 2)]
    print("\n\n\nBob's key:", key)

    cipherText = conn.recv(1024).decode()

    plainText_Binnary = xor_binary_strings(cipherText, ''.join(map(str, key)))
    plainText = binary_to_text(plainText_Binnary)
    print("\n\n\n"+plainText)

    conn.close()
    server_socket.close()

if __name__ == '__main__':
    main()
