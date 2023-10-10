from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import numpy as np

# Create a quantum circuit with 2 qubits
n = 2
circ = QuantumCircuit(n, n)

# Alice prepares an entangled pair of qubits (Bell state)
circ.h(0)  # Apply a Hadamard gate to the first qubit
circ.cx(0, 1)  # Apply a CNOT gate to create an entangled pair

# Alice measures her qubits in the Bell basis
circ.h(0)  # Apply Hadamard gate before measurement
circ.measure([0, 1], [0, 1])

# Bob randomly chooses a basis to measure the received qubits
# 0 represents the standard basis, and 1 represents the Hadamard basis
basis_choices = np.random.randint(2, size=n)
for i in range(n):
    if basis_choices[i] == 1:
        circ.h(i)  # Apply Hadamard gate before measurement

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
shots = 1024
job = execute(circ, simulator, shots=shots)
result = job.result()

# Bob measures the received qubits
bob_results = [result.get_counts(i) for i in range(n)]

# Bob and Alice publicly reveal their basis choices
print("Alice's basis choices:", basis_choices)
print("Bob's measurement results:", bob_results)

# Alice and Bob discard the results when their basis choices don't match
final_key = []
for i in range(n):
    if basis_choices[i] == 0:
        final_key.append(int(list(bob_results[i].keys())[0]))
        
print("Final shared key:", final_key)
