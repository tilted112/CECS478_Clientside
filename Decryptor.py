import json, os, time
from cryptography.hazmat.primitives import serialization, hashes, padding, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as apadding
from cryptography.hazmat.backends import default_backend

def MydecryptMAC(ct, iv, tag, EncKey, HMACKey):
    if (len(EncKey) < 32) or (len(HMACKey) < 32):
        print("Error: Keys must be at least 32 bytes long.")
        exit()
    htag = hmac.HMAC(HMACKey, hashes.SHA256(), backend=default_backend())
    htag.update(ct)
    htag.verify(tag)
    cipher = Cipher(algorithms.AES(EncKey), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    message = unpadder.update(padded_message)
    message += unpadder.finalize()
    return bytes(message)
        
def MyRSADecrypt(RSACipher, ct, iv, RSA_Privatekey_filePath, tag):
    with open('private_key.pem', 'rb') as file:
        pkey = serialization.load_pem_private_key(
            file.read(),
            password=None,
            backend=default_backend()
        )
    key = pkey.decrypt(
        RSACipher,
        apadding.OAEP(
            mgf=apadding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return MydecryptMAC(ct, iv, tag, key[0:32], key[len(key[0:32]):])

def MyJSONDecrypt(message, private_key):
    encrypted = json.loads(message)
    return MyRSADecrypt(bytes(encrypted["RSACipher"], 'latin-1'), bytes(encrypted["ct"], 'latin-1'), bytes(encrypted["iv"], 'latin-1'), private_key, bytes(encrypted["tag"], 'latin-1'))
