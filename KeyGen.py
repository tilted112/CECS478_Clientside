import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def GenerateKeyPair():
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)
    public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
    private_key = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
        
    with open("/private_key2.pem", "w") as file:
        file.write(private_key.decode('utf-8'))
    with open("/public_key2.pem", "w") as file:
        file.write(public_key.decode('utf-8'))
        
GenerateKeyPair()