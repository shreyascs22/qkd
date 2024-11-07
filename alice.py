# import socket
# from aes_utils import encrypt_message, decrypt_message, get_aes_key_from_shared_key
# from qkd import perform_qkd

# # Generate shared AES key using QKD
# shared_key = perform_qkd()
# aes_key = get_aes_key_from_shared_key(shared_key)

# # Set up connection to Bob (Server)
# alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# alice_socket.connect(('localhost', 12345))

# print("QKD complete. Shared AES key established with Bob.")

# def send_message(message):
#     iv, ciphertext = encrypt_message(aes_key, message)
#     print(f"Alice (Encrypted): {ciphertext}")
#     # Send IV (16 bytes) + ciphertext
#     alice_socket.send(iv + ciphertext)

# def receive_message():
#     try:
#         response = alice_socket.recv(1024)  # Adjust as needed to receive the full message
#         iv = response[:16]  # First 16 bytes are the IV
#         ciphertext = response[16:]  # Remaining bytes are the ciphertext

#         decrypted_message = decrypt_message(aes_key, iv, ciphertext)
#         print(f"Alice (Decrypted): {decrypted_message}")
#     except ConnectionResetError:
#         print("Connection was forcibly closed by the remote host. Please check if Bob's server is running.")

# # Alice sends a message to Bob
# send_message("Hello Bob")
# receive_message()  # Wait for Bob's reply

# alice_socket.close()

import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from qkd import perform_qkd

# AES Encryption Setup
def get_aes_key(shared_key):
    return hashlib.sha256(shared_key.encode()).digest()  # 256-bit key

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # Get the IV used for encryption
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return iv, ciphertext

def decrypt_message(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()  # Unpad the decrypted message
        return decrypted_message
    except ValueError:
        raise ValueError("Padding is incorrect.")

# Socket Setup for Alice (Client)
def send_message(message):
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alice_socket.connect(('localhost', 12345))  # Connect to Bob's server
    shared_key = perform_qkd()
    aes_key = get_aes_key(shared_key)
    iv, ciphertext = encrypt_message(aes_key, message)
    alice_socket.send(iv + ciphertext)  # Send IV + Ciphertext to Bob
    print(f"Alice (Sent - Encrypted): {ciphertext}")

    # Receive reply from Bob
    data = alice_socket.recv(1024)
    iv_reply = data[:16]  # First 16 bytes are IV
    ciphertext_reply = data[16:]  # Rest is the ciphertext
    decrypted_reply = decrypt_message(aes_key, iv_reply, ciphertext_reply)
    
    print(f"Alice (Received - Encrypted): {ciphertext_reply}")
    print(f"Alice (Received - Decrypted): {decrypted_reply}")

    alice_socket.close()

# Main Function
def main():
    message = input("Alice, enter your message: ")
    send_message(message)

if __name__ == "__main__":
    main()

