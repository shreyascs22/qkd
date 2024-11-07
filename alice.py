import socket
from aes_utils import encrypt_message, decrypt_message, get_aes_key_from_shared_key
from qkd import perform_qkd

# Generate shared AES key using QKD
shared_key = perform_qkd()
aes_key = get_aes_key_from_shared_key(shared_key)

# Set up connection to Bob (Server)
alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_socket.connect(('localhost', 12345))

print("QKD complete. Shared AES key established with Bob.")

def send_message(message):
    iv, ciphertext = encrypt_message(aes_key, message)
    print(f"Alice (Encrypted): {ciphertext}")
    # Send IV (16 bytes) + ciphertext
    alice_socket.send(iv + ciphertext)

def receive_message():
    try:
        response = alice_socket.recv(1024)  # Adjust as needed to receive the full message
        iv = response[:16]  # First 16 bytes are the IV
        ciphertext = response[16:]  # Remaining bytes are the ciphertext

        decrypted_message = decrypt_message(aes_key, iv, ciphertext)
        print(f"Alice (Decrypted): {decrypted_message}")
    except ConnectionResetError:
        print("Connection was forcibly closed by the remote host. Please check if Bob's server is running.")

# Alice sends a message to Bob
send_message("Hello Bob")
receive_message()  # Wait for Bob's reply

alice_socket.close()
