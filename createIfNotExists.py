#!/usr/bin/python3
import sys
import time
from br.com.vert.CAIXA.SICRM.Job import Job

cv=Job(sys.argv[1],sys.argv[2])
cv.createJobIfNotExists()
#cv.jobExecute()
#timer=0
#while cv.jobVerify():
#    print("time elapsed: "+str(timer)+"min")
#    time.sleep(60)
#    timer+=1