from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

# Initialize a quantum circuit with 8 qubits
n = 8
alice_circuit = QuantumCircuit(n, n)
bob_circuit = QuantumCircuit(n, n)

# Create an entangled state (Bell state) between qubits 0 and 1 (Alice and Bob share this pair)
alice_circuit.h(0)
alice_circuit.cx(0, 1)

# Alice measures her qubits
alice_circuit.measure(range(n), range(n))

# Bob measures his qubits
bob_circuit.measure(range(n), range(n))

# Simulate Alice's circuit
simulator = Aer.get_backend('qasm_simulator')
shots = 1024
alice_job = execute(alice_circuit, simulator, shots=shots)
alice_result = alice_job.result()
alice_counts = alice_result.get_counts()

# Simulate Bob's circuit
bob_job = execute(bob_circuit, simulator, shots=shots)
bob_result = bob_job.result()
bob_counts = bob_result.get_counts()

# Print the measurement results for Alice and Bob
print("Alice's measurement results:")
print(alice_counts)
print("Bob's measurement results:")
print(bob_counts)

# Analyze the results to detect Bell inequalities violation
def check_violation(alice_counts, bob_counts):
    # Define expected Bell states for violations
    expected_counts = {'00000000': shots / 2, '11111111': shots / 2}
    
    # Calculate observed counts for Alice and Bob
    alice_observed_counts = alice_counts.get('00000000', 0) + alice_counts.get('11111111', 0)
    bob_observed_counts = bob_counts.get('00000000', 0) + bob_counts.get('11111111', 0)
    
    # Check for Bell inequalities violation
    return (
        alice_observed_counts < expected_counts['00000000'] - shots / 3
        or alice_observed_counts > expected_counts['11111111'] + shots / 3
        or bob_observed_counts < expected_counts['00000000'] - shots / 3
        or bob_observed_counts > expected_counts['11111111'] + shots / 3
    )

if check_violation(alice_counts, bob_counts):
    print("Bell inequalities violated! Secure key exchange possible.")
else:
    print("Bell inequalities not violated. Key exchange may not be secure.")
