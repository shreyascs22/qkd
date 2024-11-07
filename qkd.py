# import numpy as np
# from qiskit import QuantumCircuit, transpile
# from qiskit_aer import Aer

# # Number of bits in the quantum communication
# n_bits = 100

# # Alice generates random bits and bases
# alice_bits = np.random.randint(2, size=n_bits)
# alice_bases = np.random.randint(2, size=n_bits)

# # Bob generates his random bases
# bob_bases = np.random.randint(2, size=n_bits)

# # Setup the Aer simulator backend
# backend = Aer.get_backend('aer_simulator')

# # Function to prepare Alice's qubits based on her bits and bases
# def prepare_qubit(bit, basis):
#     qc = QuantumCircuit(1, 1)
#     if bit == 1:
#         qc.x(0)  # X-gate for bit 1
#     if basis == 1:
#         qc.h(0)  # Hadamard for X-basis preparation
#     return qc

# # Prepare Alice's qubits
# alice_qubits = [prepare_qubit(alice_bits[i], alice_bases[i]) for i in range(n_bits)]

# # Transpile Alice's circuits for the backend
# transpiled_alice_qubits = [transpile(qc, backend) for qc in alice_qubits]

# # Simulate Bob's measurement of Alice's qubits
# bob_results = []

# # Loop to measure Bob's qubits
# for i in range(n_bits):
#     qc = transpiled_alice_qubits[i]
    
#     # If Bob's basis is 1, apply a Hadamard gate before measurement
#     if bob_bases[i] == 1:
#         qc.h(0)  # Change to X-basis for measurement if needed
    
#     # Measure qubit
#     qc.measure(0, 0)
    
#     # Run the circuit and get the result
#     job = backend.run(qc)
#     result = job.result()
#     measured_value = result.get_counts(qc)
    
#     # Record the measurement result (either 0 or 1)
#     measured_result = list(measured_value.keys())[0]
#     bob_results.append(int(measured_result))

# # Generate shared key between Alice and Bob based on matching bases
# matching_indices = [i for i in range(n_bits) if alice_bases[i] == bob_bases[i]]
# shared_key = [bob_results[i] for i in matching_indices]

# # Output the results
# print("Alice's Bits:", alice_bits)
# print("Alice's Bases:", alice_bases)
# print("Bob's Bases:", bob_bases)
# print("Bob's Measurement Results:", bob_results)
# print("Shared Key between Alice and Bob:", shared_key)
# print(f"Length of Shared Key: {len(shared_key)}")

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def perform_qkd(n_bits=100):
    # Alice and Bob's QKD setup
    alice_bits = np.random.randint(2, size=n_bits)
    alice_bases = np.random.randint(2, size=n_bits)
    bob_bases = np.random.randint(2, size=n_bits)

    # Aer simulator backend for QKD
    backend = Aer.get_backend('aer_simulator')

    def prepare_qubit(bit, basis):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if basis == 1:
            qc.h(0)
        return qc

    # Preparing Alice's qubits and transpiling
    alice_qubits = [prepare_qubit(alice_bits[i], alice_bases[i]) for i in range(n_bits)]
    transpiled_qubits = [transpile(qc, backend) for qc in alice_qubits]

    # Bob's measurements
    bob_results = []
    for i in range(n_bits):
        qc = transpiled_qubits[i]
        if bob_bases[i] == 1:
            qc.h(0)
        qc.measure(0, 0)
        job = backend.run(qc)
        result = job.result()
        measured_result = list(result.get_counts(qc).keys())[0]
        bob_results.append(int(measured_result))

    # Generate shared key based on matching bases
    matching_indices = [i for i in range(n_bits) if alice_bases[i] == bob_bases[i]]
    shared_key = ''.join(str(bob_results[i]) for i in matching_indices)
    return shared_key[:32]  # Return a 256-bit shared key for AES


