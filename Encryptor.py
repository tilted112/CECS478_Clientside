import json, os, time
from cryptography.hazmat.primitives import serialization, hashes, padding, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as apadding
from cryptography.hazmat.backends import default_backend

def MyencryptMAC(message):
    EncKey = os.urandom(32)
    HMACKey = os.urandom(32)     
    message = bytes(message, 'latin-1')
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(EncKey), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_message) + encryptor.finalize()
    htag = hmac.HMAC(HMACKey, hashes.SHA256(), backend=default_backend())
    htag.update(ct)
    tag = htag.finalize()
    return ct, iv, tag, EncKey, HMACKey
        
def MyRSAEncrypt(message, RSA_Publickey_filePath):
    with open(RSA_Publickey_filePath, 'rb') as file:
        pkey = serialization.load_pem_public_key(
            file.read(),
            backend=default_backend()
        )
    ct, iv, tag, EncKey, HMACKey = MyencryptMAC(message)
    RSACipher = pkey.encrypt(
        EncKey + HMACKey,
        apadding.OAEP(
            mgf=apadding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return RSACipher, ct, iv, tag

def MyJSONEncrypt(message, RSA_Publickey_filePath):
    RSACipher, ct, iv, tag = MyRSAEncrypt(message, 'public_key.pem')
    jason = json.dumps({
            "RSACipher": RSACipher.decode('latin-1'),
            "ct": ct.decode('latin-1'),
            "iv": iv.decode('latin-1'),
            "tag": tag.decode('latin-1')
        })
    rjason = jason.replace("&", "ampersand")
    rrjason = rjason.replace("+", "plusplus")
    time.sleep(.1)
    return rrjason

