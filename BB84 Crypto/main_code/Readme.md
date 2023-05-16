# BB84 Quantum Key Distribution Simulation
This repository, created by Sujeet Amberkar, contains two Python scripts, alice.py and bob.py, which simulate the BB84 quantum key distribution protocol. The BB84 protocol allows two parties, Alice and Bob, to securely exchange a secret key over a potentially insecure communication channel. The security of the key exchange is guaranteed by the principles of quantum mechanics

The simulation uses the Qiskit library to create and manipulate quantum circuits, while socket programming is used to establish communication between Alice and Bob
## Getting Started
## Prerequisites
Before running the scripts, ensure that you have Python 3.6 or higher installed. You also need to install the Qiskit library. You can install it using pip:

pip install qiskit

## Running the Simulation
1) Open two terminal windows or command prompts.
2) In one of the terminal windows, navigate to the directory containing the bob.py script and run it:
python bob.py
Bob's script will prompt you to enter the lower and upper limits for the port number. Make sure to choose valid and available port numbers.
3)In the other terminal window, navigate to the directory containing the alice.py script and run it:
python alice.py
Alice's script will prompt you to enter the lower and upper limits for the port number. Make sure to enter the same values as provided in Bob's script
4)Observe the output in both terminal windows. Alice and Bob will exchange quantum states and classical information, and at the end, they will both have the same secret key. Alice will use the key to encrypt a message and send it to Bob, who will decrypt it using his key.

## About the Author
Sujeet Amberkar created this BB84 Quantum Key Distribution Simulation. If you have any questions or suggestions, feel free to reach out or contribute to the project.
