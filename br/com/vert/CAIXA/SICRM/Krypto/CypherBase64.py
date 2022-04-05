import base64
from .iKrypto import iKrypto

class CypherBase64(iKrypto):
    def encrypt(self,raw):
        return bytes.decode(base64.b64encode(bytes(raw,encoding="utf-8")))

    def decrypt(self,enc):
        return bytes.decode(base64.b64decode(enc))