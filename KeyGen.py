from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def GenerateKeyPair(filenamePrivK, filenamePK):
    privk, pk = GenKey()
    SavePrivateKey(privk, filenamePrivK)
    SavePublicKey(pk, filenamePK)
    return 'bla'
    
def GenKey():
    private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def SavePrivateKey(private_key, filename):
    pem_obj = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename + '.pem', 'wb') as fileout:
        fileout.write(pem_obj)

def SavePublicKey(public_key, filename):
    pem_obj = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename + '.pem', 'wb') as fileout:
        fileout.write(pem_obj)    