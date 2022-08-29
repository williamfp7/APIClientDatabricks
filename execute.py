#!/usr/bin/python3
from br.com.vert.CAIXA.SICRM.Krypto.AES256 import AES256
from br.com.vert.CAIXA.SICRM.API import API
from br.com.vert.CAIXA.SICRM.Job import Job
import time
import sys

cifra=AES256(sys.argv[1])
API=API(cifra,"sicrm.ini")
cv=Job(API,sys.argv[2])
cv.execute()
timer=0
while cv.verify():
    print("time elapsed: "+str(timer)+"min")
    time.sleep(60)
    timer+=1