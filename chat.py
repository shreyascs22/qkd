import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

# User data for authorized contacts
user_data = {
    "Alice": {"password": "alice_pass", "contacts": ["Bob", "David"], "port": 12345},
    "Bob": {"password": "bob_pass", "contacts": ["Alice", "David", "Tom"], "port": 12346},
    "David": {"password": "david_pass", "contacts": ["Alice", "Bob"], "port": 12347},
    "Tom": {"password": "tom_pass", "contacts": ["Bob"], "port": 12348},
}

# AES Encryption/Decryption functions
def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    encrypted_message = cipher.iv + ct_bytes
    print(f"[ENCRYPT] IV: {cipher.iv.hex()}")
    print(f"[SEND] Encrypted message: {encrypted_message.hex()}")
    return encrypted_message

def decrypt_message(key, ciphertext, padding_check=True):
    if len(ciphertext) < AES.block_size * 2:
        print("[ERROR] Ciphertext too short for valid decryption.")
        return None

    iv = ciphertext[:AES.block_size]
    ct = ciphertext[AES.block_size:]

    # print(f"[DECRYPT] IV: {iv.hex()}")
    # print(f"[DECRYPT] Ciphertext: {ct.hex()}")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = cipher.decrypt(ct)

    # Print raw decrypted message in hexadecimal for inspection
    print(f"[DECRYPT] Raw decrypted message (hex): {decrypted_message.hex()}")

    if not padding_check:
        return decrypted_message

    # Attempt unpadding with PKCS#7
    try:
        unpadded_message = unpad(decrypted_message, AES.block_size)
        print(f"[DECRYPT] Unpadded message: {unpadded_message.decode('latin-1')}")
        return unpadded_message
    except ValueError as e:
        print("Padding error during decryption:", e)
        return None

# Receive messages
def receive_message(username, key, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(1)
    print(f"{username} is listening for messages...")

    while True:
        conn, addr = server_socket.accept()
        data = b''
        while True:
            packet = conn.recv(1024)
            if not packet:
                break
            data += packet

        print(f"[RECEIVE] Raw data: {data.hex()}")
        if data:
            message = decrypt_message(key, data, padding_check=False)
            if message:
                try:
                    print(f"MESSAGE: {message.decode('utf-8')}")
                except UnicodeDecodeError:
                    print("Decryption successful, but message contains non-UTF-8 bytes:")
                    print(message)
            else:
                print("Failed to decrypt the message.")
        conn.close()

# Send messages
def send_message(username, key, target_port):
    while True:
        message = input("Enter a message (type 'exit' to quit): ")
        if message.lower() == "exit":
            break
        encrypted_message = encrypt_message(key, message)
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", target_port))
        client_socket.sendall(encrypted_message)
        client_socket.close()

# Main function
def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Authenticate user
    if username not in user_data or user_data[username]["password"] != password:
        print("Invalid username or password.")
        return

    # Generate encryption key and start listening thread
    key = generate_key(password)
    port = user_data[username]["port"]
    threading.Thread(target=receive_message, args=(username, key, port), daemon=True).start()

    # Show contacts and initiate chat
    contacts = user_data[username]["contacts"]
    print(f"Your contacts: {', '.join(contacts)}")
    while True:
        contact = input("Enter the contact name to chat with (or 'exit' to quit): ")
        if contact == "exit":
            break
        if contact in contacts:
            target_port = user_data[contact]["port"]
            print(f"Starting chat with {contact}...")
            send_message(username, key, target_port)
        else:
            print("Contact not available.")

if __name__ == "__main__":
    main()
