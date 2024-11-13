import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from qkd import perform_qkd
import os

# Ports and passwords for each user
ports = {"Alice": 12345, "Bob": 12346, "Tom": 12347, "David": 12348}
pwds = {"Alice": 123, "Bob": 234, "Tom": 345, "David": 456}
stop_event = threading.Event()  # Event to signal the thread to stop

# AES key setup
def get_aes_key(shared_key):
    # Replace with an actual shared key in a secure setup
    return hashlib.sha256(shared_key.encode()).digest()

if os.path.exists("sharedkey.txt"):
    with open("sharedkey.txt",'r') as file:
        shared_key = file.read()
else:
    with open("sharedkey.txt",'w') as file:
        shared_key = perform_qkd()
        file.write(shared_key)
    with open("sharedkey.txt",'r') as file:
        shared_key = file.read()

aes_key = get_aes_key(shared_key)

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
        receiver_socket.settimeout(1.0)  # Prevent blocking indefinitely
        try:
            conn, addr = receiver_socket.accept()
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