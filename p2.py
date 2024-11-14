import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import os

# Ports and passwords for each user
ports = {"Alice": 12345, "Bob": 12346, "Tom": 12347, "David": 12348}
pwds = {"Alice": 123, "Bob": 234, "Tom": 345, "David": 456}
stop_event = threading.Event()  # Event to signal the thread to stop

# QKD key generation between Bob and Alice
# QKD key generation between Alice and Bob
def perform_qkd_with_alice(connection):
    # Receive Alice's bases as a string
    alice_bases_data = connection.recv(1024)
    alice_bases_str = alice_bases_data.decode()
    alice_bases = np.array([int(x) for x in alice_bases_str])

    # Debug: Print Alice's received bases
    #print("Alice's bases: ", alice_bases)

    # Bob generates his own bases and sends them to Alice as a string
    n_bits = 100
    bob_bases = np.random.randint(2, size=n_bits)
    bob_bases_str = ''.join(map(str, bob_bases))

    # Send Bob's bases to Alice as a string
    connection.sendall(bob_bases_str.encode())

    # Receive Alice's bits as a string
    alice_bits_data = connection.recv(1024)
    alice_bits_str = alice_bits_data.decode()
    alice_bits = np.array([int(x) for x in alice_bits_str])

    # Debug: Print Alice's bits received
    #print("Alice's bits: ", alice_bits)

    alice_qubits = []
    for i in range(n_bits):
        bit = alice_bits[i]
        basis = alice_bases[i]
    
        qc = QuantumCircuit(1, 1)
    
        if bit == 1:
            qc.x(0)  # Apply X gate if the bit is 1
    
        if basis == 1:
            qc.h(0)  # Apply H gate if the basis is 1
    
        alice_qubits.append(qc)

    transpiled_qubits = [transpile(qc, Aer.get_backend('aer_simulator')) for qc in alice_qubits]

    results = []
    for i in range(n_bits):
        qc = transpiled_qubits[i]
        if bob_bases[i] == 1:
            qc.h(0)  # Apply H gate if Bob's basis is 1
        qc.measure(0, 0)
        job = Aer.get_backend('aer_simulator').run(qc)
        result = job.result()
        measured_result = list(result.get_counts(qc).keys())[0]
        results.append(int(measured_result))

    matching_indices = [i for i in range(n_bits) if alice_bases[i] == bob_bases[i]]
    shared_key = ''.join(str(results[i]) for i in matching_indices)

    # Debug: Print the shared key generated
    #print("Shared key (Bob): ", shared_key)
    return shared_key


# AES key setup
def get_aes_key(shared_key):
    return hashlib.sha256(shared_key.encode()).digest()

# AES encryption
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return iv + ciphertext  # Send IV and ciphertext together

# AES decryption
def decrypt_message(key, data):
    iv = data[:16]  # Extract the IV
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

def receive_message():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(("127.0.0.1", ports[uname]))
    receiver_socket.listen(1)
    print(f"{uname} listening for incoming messages on 127.0.0.1:{ports[uname]}")
    
    while not stop_event.is_set():  # Run until stop_event is set
        receiver_socket.settimeout(1.0)
        try:
            conn, addr = receiver_socket.accept()

            # Perform QKD to generate shared AES key
            shared_key = perform_qkd_with_alice(conn)
            aes_key = get_aes_key(shared_key)

            data = conn.recv(1024)
            if data:
                decrypted_message = decrypt_message(aes_key, data)
                print(f"{uname} received: {decrypted_message}")
            conn.close()
        except socket.timeout:
            continue
    receiver_socket.close()

def send_message(peer_ip, peer_port, message):
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((peer_ip, peer_port))
    
    # Perform QKD to generate shared AES key
    shared_key = perform_qkd_with_alice(sender_socket)
    aes_key = get_aes_key(shared_key)

    encrypted_message = encrypt_message(aes_key, message)
    sender_socket.send(encrypted_message)
    sender_socket.close()

def main():
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()
    
    while True:
        message = input()
        if message.lower() == "exit":
            print("Exiting chat.")
            stop_event.set()  # Signal the receive thread to stop
            break
        send_message("127.0.0.1", ports[receiver_name], message)
    
    receive_thread.join()  # Wait for the receive thread to finish

if __name__ == "__main__":
    uname = input("Enter username : ")
    pwd = int(input("Enter password : "))
    if (uname in pwds.keys()) and (pwd == pwds[uname]):
        receiver_name = input("Enter receiver name : ")
        if receiver_name in pwds:
            main()
        else:
            print("Receiver not in your contacts")
    else:
        print("Username or password was incorrect")
