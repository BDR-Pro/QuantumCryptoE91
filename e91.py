from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

# Initialize a quantum circuit with 8 qubits
n = 8
circuit = QuantumCircuit(n, n)

# Create an entangled state (Bell state) between qubits 0 and 1
circuit.h(0)
circuit.cx(0, 1)

# Create Bell states between other pairs of qubits
for i in range(2, n, 2):
    circuit.h(i)
    circuit.cx(i, i + 1)

# Measure all qubits
circuit.measure(range(n), range(n))

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
shots = 1024
job = execute(circuit, simulator, shots=shots)
result = job.result()
counts = result.get_counts()

# Print the measurement results
print("Measurement results:")
print(counts)

# Analyze the results to detect Bell inequalities violation
def check_violation(counts):
    expected_counts = {'00000000': shots / 2, '11111111': shots / 2}
    observed_counts = counts.get('00000000', 0) + counts.get('11111111', 0)
    return observed_counts < expected_counts['00000000'] - shots / 3 or observed_counts > expected_counts['11111111'] + shots / 3

if check_violation(counts):
    print("Bell inequalities violated! Secure key exchange possible.")
else:
    print("Bell inequalities not violated. Key exchange not secure.")
