import socket
from aes_utils import encrypt_message, decrypt_message, get_aes_key_from_shared_key
from qkd import perform_qkd

# Generate shared AES key using QKD
shared_key = perform_qkd()
aes_key = get_aes_key_from_shared_key(shared_key)

# Set up server socket to listen for Alice
bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bob_socket.bind(('localhost', 12345))
bob_socket.listen(1)
print("Bob is ready to receive messages from Alice...")

conn, addr = bob_socket.accept()
print("QKD complete. Shared AES key established with Alice.")

def receive_message():
    # Receive enough bytes for IV (16 bytes) and ciphertext
    response = conn.recv(1024)  # Adjust as needed to ensure full message
    iv = response[:16]  # First 16 bytes are the IV
    ciphertext = response[16:]  # Remaining bytes are the ciphertext

    try:
        decrypted_message = decrypt_message(aes_key, iv, ciphertext)
        print(f"Bob (Decrypted): {decrypted_message}")
        return decrypted_message
    except ValueError as e:
        print(f"Decryption failed: {e}")
        return None
def send_message(message):
    iv, ciphertext = encrypt_message(aes_key, message)
    print(f"Bob (Encrypted): {ciphertext}")
    conn.send(iv + ciphertext)

# Bob receives message from Alice
message_from_alice = receive_message()

# Bob sends a reply back to Alice
send_message("Hello Alice")

# Close connection
conn.close()
bob_socket.close()
