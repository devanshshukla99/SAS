import asyncio
import datetime
import time
import sys
import os
import math
import __main__

"""
Devansh Shukla

"""

def exec(_sch_h , _sch_m , _sch_s):
    
    now_ = (datetime.datetime.now())

    y = int(str(now_)[0:4])
    m = int(str(now_)[5:7])
    d = int(str(now_)[8:10])
    
    exec_time = datetime.datetime(y, m, d, _sch_h, _sch_m, _sch_s, 0)
    
    print("Sch Execution Time = " , exec_time)
    print("Current Time   = " , now_ , end="\r")

    while True:

        now_ = (datetime.datetime.now())

        #print("Current Time   = " , now_ , end="\r")
        
        if(math.isclose((now_.timestamp()) ,(exec_time.timestamp()) , rel_tol=1e-14 , abs_tol=0)):
            #__main__.t1 = time.perf_counter()
            break
           
    print("\n\nVoila")

    __main__.log("Scheduled Execution Time = " , exec_time.timestamp())
    __main__.log("Real Execution Time   = " , now_.timestamp())


#exec()

print("Imported")


