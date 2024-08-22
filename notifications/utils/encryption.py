from cryptography.fernet import Fernet
import base64
import os


# Generate a key for encryption/decryption. This should be kept safe.
key = base64.urlsafe_b64encode(os.urandom(32))
cipher = Fernet(key)

def encrypt_message(message):
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    return cipher.decrypt(encrypted_message.encode()).decode()