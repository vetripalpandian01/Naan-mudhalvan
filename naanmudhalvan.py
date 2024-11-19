# -*- coding: utf-8 -*-
"""NaanMudhalvan.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/140k_5KlXDJnRC5sAWSkU8Y_aojw5q28-
"""

import pandas as pd

import numpy as np

!pip install pycryptodome

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

def setup_group():
    key = RSA.generate(2048)  # Generate a 2048-bit RSA key pair
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key, private_key

def encrypt_data(data, public_key):
    # Generate a random symmetric key (AES-256) for data encryption
    symmetric_key = get_random_bytes(32)

    # Encrypt data using AES
    cipher_aes = AES.new(symmetric_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode())

    # Encrypt the symmetric key with RSA public key
    rsa_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)

    # Return ciphertext, RSA-encrypted AES key, tag, and nonce
    return b64encode(ciphertext).decode(), b64encode(encrypted_symmetric_key).decode(), b64encode(tag).decode(), b64encode(cipher_aes.nonce).decode()

def decrypt_data(ciphertext, encrypted_symmetric_key, tag, nonce, private_key):
    # Import the private RSA key
    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)

    # Decrypt the symmetric key with RSA private key
    symmetric_key = cipher_rsa.decrypt(b64decode(encrypted_symmetric_key))

    # Decrypt the data using AES
    cipher_aes = AES.new(symmetric_key, AES.MODE_GCM, nonce=b64decode(nonce))
    decrypted_data = cipher_aes.decrypt_and_verify(b64decode(ciphertext), b64decode(tag))
    return decrypted_data.decode()

if __name__ == "__main__":
    # Step 1: Setup group keys
    public_key, private_key = setup_group()

    # Data to be shared
    data = "Confidential data for group members only."

    # Encrypt data for the group
    ciphertext, encrypted_symmetric_key, tag, nonce = encrypt_data(data, public_key)
    print("Encrypted Data:", ciphertext)
    print("Encrypted Symmetric Key:", encrypted_symmetric_key)
    print("Tag:", tag)
    print("Nonce:", nonce)

    # Decrypt data as a group member with access to the private key
    decrypted_data = decrypt_data(ciphertext, encrypted_symmetric_key, tag, nonce, private_key)
    print("Decrypted Data:", decrypted_data)