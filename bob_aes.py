import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

listen_ip = "127.0.0.1"
listen_port = 12346  # Port Bob listens on
peer_ip = "127.0.0.1"
peer_port = 12345  # Port Alice listens on

# AES key setup
def get_aes_key():
    # Replace with an actual shared key in a secure setup
    return hashlib.sha256("sharedsecretkey".encode()).digest()

aes_key = get_aes_key()

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
    receiver_socket.bind((listen_ip, listen_port))
    receiver_socket.listen(1)
    print(f"Alice listening for incoming messages on {listen_ip}:{listen_port}")
    while True:
        conn, addr = receiver_socket.accept()
        data = conn.recv(1024)
        if data:
            decrypted_message = decrypt_message(aes_key, data)
            print(f"Alice received: {decrypted_message}")
            print(f"MESSAGE : {decrypted_message}")
        conn.close()

def send_message(peer_ip, peer_port, message):
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((peer_ip, peer_port))
    encrypted_message = encrypt_message(aes_key, message)
    sender_socket.send(encrypted_message)
    sender_socket.close()

def main():
    threading.Thread(target=receive_message).start()
    while True:
        message = input()
        if message.lower() == "exit":
            print("Exiting chat.")
            break
        send_message(peer_ip, peer_port, message)

if __name__ == "__main__":
    main()
