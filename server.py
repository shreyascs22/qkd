# server.py
import socket
from aes_utils import decrypt_message
from qkd import perform_qkd  # Import the QKD function

def handle_client_connection(client_socket):
    """Handle incoming client connection."""
    try:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            return

        # Compute hash of the received data
        received_hash = decrypt_message(data)

        # Send the hash back to the client
        client_socket.send(received_hash.encode())
    finally:
        client_socket.close()

def start_server(host='127.0.0.1', port=65432):
    """Start the server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        handle_client_connection(client_socket)

if __name__ == "__main__":
    start_server()
