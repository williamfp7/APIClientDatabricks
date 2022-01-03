#!/usr/bin/python3
import sys
import time
from br.com.vert.CAIXA.SICRM.Job import *

cv=Job(sys.argv[1])
if cv.jobExists()==False:
    raise TypeError("O job não existe")
cv.jobExecute()
timer=0
while cv.jobVerify():
    print("time elapsed: "+str(timer)+"min")
    time.sleep(60)
    timer+=1