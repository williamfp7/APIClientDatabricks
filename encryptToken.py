#!/usr/bin/python3
from br.com.vert.CAIXA.SICRM.Krypto.AES256 import AES256
import sys

a=AES256(sys.argv[1])

f=open("sicrm.json","r")
txt=f.read()
f.close()

f=open("sicrm.ini","w")
f.write(a.encrypt(txt))
f.close()