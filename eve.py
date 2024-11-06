import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Number of bits in the quantum communication
n_bits = 100

# Alice generates random bits and bases
alice_bits = np.random.randint(2, size=n_bits)
alice_bases = np.random.randint(2, size=n_bits)

# Bob and Eve generate their random bases
bob_bases = np.random.randint(2, size=n_bits)
eve_bases = np.random.randint(2, size=n_bits)

# Setup the Aer simulator backend
backend = Aer.get_backend('aer_simulator')

# Function to prepare Alice's qubits based on her bits and bases
def prepare_qubit(bit, basis):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)  # X-gate for bit 1
    if basis == 1:
        qc.h(0)  # Hadamard for X-basis preparation
    return qc

# Prepare Alice's qubits
alice_qubits = [prepare_qubit(alice_bits[i], alice_bases[i]) for i in range(n_bits)]
bob_results = []

# Simulate Bob's measurement of Alice's qubits
for i in range(n_bits):
    qc = alice_qubits[i]
    if bob_bases[i] == 1:
        qc.h(0)  # Change to X-basis for measurement if needed
    qc.measure(0, 0)
    transpiled_qc = transpile(qc, backend)
    job = backend.run(transpiled_qc)
    result = job.result()
    measured_value = result.get_counts(transpiled_qc)
    measured_result = list(measured_value.keys())[0]
    bob_results.append(int(measured_result))

# Generate shared key between Alice and Bob
matching_indices = [i for i in range(n_bits) if alice_bases[i] == bob_bases[i]]
shared_key = [bob_results[i] for i in matching_indices]

print("Alice's Bits:", alice_bits)
print("Alice's Bases:", alice_bases)
print("Bob's Bases:", bob_bases)
print("Bob's Measurement Results:", bob_results)
print("Shared Key between Alice and Bob:", shared_key)
print(f"Length of Shared Key: {len(shared_key)}")

# Simulate Eve's interception and measurement
eve_results = []
for i in range(n_bits):
    qc = prepare_qubit(alice_bits[i], alice_bases[i])
    if eve_bases[i] == 1:
        qc.h(0)  # Eve measures in X-basis if her basis is 1
    qc.measure(0, 0)
    transpiled_qc = transpile(qc, backend)
    job = backend.run(transpiled_qc)
    result = job.result()
    measured_value = result.get_counts(transpiled_qc)
    measured_result = list(measured_value.keys())[0]
    eve_result = int(measured_result)

    # Eve may flip the bit with a 50% chance
    if np.random.rand() < 0.5:
        eve_result = 1 - eve_result  # Flip the bit
        print(f"Eve changed bit from {measured_result} to {eve_result} (Bit flipped)")

    eve_results.append(eve_result)

# Generate Eve's key by matching her bases with Alice's
eve_matching_indices = [i for i in range(n_bits) if alice_bases[i] == eve_bases[i]]
eve_shared_key = [eve_results[i] for i in eve_matching_indices]

print("\nEve's Bases:", eve_bases)
print("Eve's Measurement Results:", eve_results)
print("Eve's Shared Key with Alice:", eve_shared_key)
print(f"Length of Eve's Shared Key: {len(eve_shared_key)}")

# Check for discrepancies between the shared keys of Alice-Bob and Alice-Eve
discrepancies = sum(1 for i in range(len(shared_key)) if i < len(eve_shared_key) and shared_key[i] != eve_shared_key[i])

if discrepancies > 0:
    print(f"\nWarning: {discrepancies} bits were altered by Eve!")
else:
    print("\nNo changes detected by Eve.")
