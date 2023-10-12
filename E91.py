import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

# Define the number of qubits
num_qubits = 2

# Step 1: E91 Entangled State Preparation
qr = QuantumRegister(num_qubits)
cr = ClassicalRegister(num_qubits)
qc = QuantumCircuit(qr, cr)

group_same_basis = []  # Qubits with the same measurement basis
group_diff_basis = []  # Qubits with different measurement bases

# Create lists for Alice's and Bob's measurement results
alice_results = []
bob_results = []

alice_basis_list = []
bob_basis_list = []

shared_key = []

for x in range(30):
    alice_basis = []  # Alice's measurement basis for each qubit
    bob_basis = []    # Bob's measurement basis for each qubit

    # Reset the quantum circuit for a new iteration
    qc.reset(qr)

    # Prepare the E91 entangled state
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])

    for i in range (1):
        alice_basis = random.choice(['X', 'Z'])
        alice_basis_list.append(alice_basis)
        bob_basis = random.choice(['X', 'Z'])
        bob_basis_list.append(bob_basis)

        # Apply gates X and Z for the measurement bases
        if alice_basis == 'X':
            qc.x(qr[i])
        elif alice_basis == 'Z':
            qc.z(qr[i])
        if bob_basis == 'X':
            qc.x(qr[i])
        elif bob_basis == 'Z':
            qc.z(qr[i])

    qc.measure(qr, cr)

    if alice_basis == bob_basis:
        group_same_basis.append(alice_basis)
    else:
        group_diff_basis.append(alice_basis)

    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1)
    result = job.result()
    counts = result.get_counts(qc)

    alice_results.append(list(counts.keys())[0])
    bob_results.append(list(counts.keys())[0])

for i in range(len(alice_results)):
    if alice_results[i] == '00' or alice_results[i] == '11':
        shared_key.append(alice_results[i])

bobs_key = []
alice_key = []

for i in (shared_key):
    if i == '00':
        bobs_key.append(0)
        alice_key.append(0)
    elif i == '11':
        bobs_key.append(1)
        alice_key.append(1)


print('Alice\'s measurement basis:', alice_basis_list)
print('Bob\'s measurement basis:  ', bob_basis_list)
print('--------------------------------------------------------------------')
print('same basis:', group_same_basis)
print('diff basis:', group_diff_basis)
print('length of same basis:', len(group_same_basis))
print('--------------------------------------------------------------------')
print('length of the sherad key:', len(shared_key))
print('--------------------------------------------------------------------')
print('Alice\'s key:', alice_key)
print('Bob\'s key:  ', bobs_key)
print('sherd key:  ', alice_key)


