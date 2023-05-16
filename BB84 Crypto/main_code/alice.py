import socket
import os
import random
from qiskit import QuantumCircuit, Aer, execute

def prepare_qubit(bit, basis):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == 'x':
        qc.h(0)
    return qc

def xor_binary_strings(bin_str1, bin_str2):
    if len(bin_str1) != len(bin_str2):
        raise ValueError("Binary strings must be of the same length")

    xor_result = ''.join('1' if bin_str1[i] != bin_str2[i] else '0' for i in range(len(bin_str1)))
    return xor_result

def text_to_binary(text):
    binary_text = ''.join(format(ord(c), '08b') for c in text)
    return binary_text

def serialize_qubit(qc):
    qasm_str = qc.qasm()
    return qasm_str.encode('utf-8')

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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    string1 = "Sujeet Amberkar"
    string_in_binary = text_to_binary(string1)
    string_len = len(string_in_binary) // 8

    num_bits = string_len * 2 * 8
    print(f"Alice is sending integer: {num_bits}")
    client_socket.sendall(str(num_bits).encode('utf-8'))

    alice_bits = [random.choice([0, 1]) for _ in range(num_bits)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
    alice_qubits = []
    for i in range(len(alice_bits)):
        bit = alice_bits[i]
        basis = alice_bases[i]
        prepared_qubit = prepare_qubit(bit, basis)
        alice_qubits.append(prepared_qubit)

    for qc in alice_qubits:
        data = serialize_qubit(qc)
        client_socket.sendall(data)
        client_socket.recv(1)

    client_socket.sendall(''.join(alice_bases).encode('utf-8'))
    bob_bases = client_socket.recv(1024).decode('utf-8')

    matching_bases = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            matching_bases.append(i)

    alice_key = []
    for i in matching_bases:
        alice_key.append(alice_bits[i])

    key = alice_key[0:string_len * 8]
    print("Alice's key:", key)

    cipher_text = xor_binary_strings(string_in_binary, ''.join(map(str, key)))
    print("\n\n\n Cipher Text: " + cipher_text+'\n\n')

    client_socket.send(cipher_text.encode())

    client_socket.close()

if __name__ == '__main__':
    main()
