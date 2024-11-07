# aes_encryption.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from qkd import perform_qkd

def get_aes_key_from_shared_key(shared_key):
    """Generate a 256-bit AES key from the shared QKD key."""
    return hashlib.sha256(shared_key.encode()).digest()

def encrypt_message(key, message):
    """Encrypt a message using AES encryption (ECB mode)."""
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return ciphertext

def decrypt_message(key, ciphertext):
    """Decrypt a message using AES decryption (ECB mode)."""
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

# Example usage:

# Obtain shared key from QKD (simulated by the function)
shared_key = perform_qkd()

# Generate AES key from shared QKD key
aes_key = get_aes_key_from_shared_key(shared_key)
print(shared_key, aes_key)

message = "Hello, this is a test message!"

# Encrypt the message
ciphertext = encrypt_message(aes_key, message)
print(ciphertext)
print("Encrypted (hex):", ciphertext.hex())

# Decrypt the message
decrypted_message = decrypt_message(aes_key, ciphertext)
print("Decrypted:", decrypted_message)
