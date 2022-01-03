#!/usr/bin/python3
import sys
import time
from br.com.vert.CAIXA.SICRM.Job import *

cv=Job(sys.argv[1],sys.argv[2])
cv.createJobIfNotExist()
#cv.jobExecute()
#timer=0
#while cv.jobVerify():
#    print("time elapsed: "+str(timer)+"min")
#    time.sleep(60)
#    timer+=1