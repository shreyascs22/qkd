from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Function to encrypt a message
def encrypt_message(key, message):
    """
    Encrypts a message using AES in EAX mode with the given key.

    Args:
        key (bytes): AES encryption key (must be 16, 24, or 32 bytes).
        message (str): The plaintext message to encrypt.

    Returns:
        tuple: Contains the nonce, ciphertext, and authentication tag.
    """
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce  # This is required for decryption
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())  # Encrypt and generate tag

    return nonce, ciphertext, tag

# Function to decrypt a message
def decrypt_message(key, nonce, ciphertext, tag):
    """
    Decrypts a message encrypted with AES in EAX mode.

    Args:
        key (bytes): AES decryption key (must be the same key used for encryption).
        nonce (bytes): The nonce used during encryption.
        ciphertext (bytes): The encrypted message.
        tag (bytes): The authentication tag generated during encryption.

    Returns:
        str: The decrypted plaintext message.
    """
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)  # Decrypt and verify the message

    return decrypted_message.decode()  # Convert from bytes to string
