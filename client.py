# client.py
import socket
from aes_utils import encrypt_message
from qkd import perform_qkd  # Import the QKD function
from Crypto.Random import get_random_bytes

def start_client(server_host='127.0.0.1', server_port=65432):
    """Start the client and send data to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    try:
        # Define the data to send
        # data = b"Hello, Server! This is a test message."
        shared_key = perform_qkd(100)
        print(shared_key)
        data = input("Enter message : ")
        # PS - Actual data is above commented copy that
        key = get_random_bytes(16)
        # Compute hash of the data before sending
        expected_hash = encrypt_message(key,data)

        # Send data to the server
        data = bytes(data, 'utf-8')
        client_socket.send(data)

        # Receive the hash from the server
        received_hash = client_socket.recv(64).decode()

        # Verify the hash
        if expected_hash == received_hash:
            print("Data integrity verified. No corruption or tampering detected.")
        else:
            print("Data integrity check failed. Possible corruption or tampering.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()