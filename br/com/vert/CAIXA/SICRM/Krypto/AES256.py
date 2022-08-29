# AES 256 encryption/decryption using pycrypto library
 
import base64
import random
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from .iKrypto import iKrypto

class AES256(iKrypto):
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self,password):
        self.__password=password

    
    BLOCK_SIZE = 16
    pad = lambda self, s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
    unpad = lambda self, s: s[:-ord(s[len(s) - 1:])]

    def __init__(self, password):
        #msg=self.pad(message)
        self.password = self.get_private_key(password) #Chave de 32 bits -> AES-256
    
    def get_private_key(self,password):
        salt = b"this is a salt"
        kdf = PBKDF2(password, salt, 64, 1000)
        key = kdf[:32]
        return key
    
    
    def encrypt(self,raw):
        raw = self.pad(raw)
        try:
            iv = Random.new().read(AES.block_size)
        except:
            iv =str("%016.0f" % int(random.random()*10**16)).encode("utf-8")
        cipher = AES.new(self.password, AES.MODE_CBC, iv)
        return bytes.decode(base64.b64encode(iv + cipher.encrypt(raw)))
    
    
    def decrypt(self,enc):
        enc = base64.b64decode(enc)
        iv = enc[:16] #initial value
        cipher = AES.new(self.password, AES.MODE_CBC, iv)
        return self.unpad(bytes.decode(cipher.decrypt(enc[16:])))
 


# First let us encrypt secret message
#encrypted = encrypt("This is a secret message", input("Enter encryption password: "))
#print(encrypted)
 
# Let us decrypt using our original password
#decrypted = decrypt(encrypted, password)
#print(bytes.decode(decrypted))