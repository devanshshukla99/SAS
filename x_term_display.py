#Program for x-term Display

import subprocess
import datetime
import sys
import time
from numpy import *
#import __main__

"""
Devansh Shukla

"""

"""
Useage

python3 x_term_display.py YYYY MM DD HH MM' SS'' RFI/ACQ

"""

def x_term_display():

    data = load("data.npy" , allow_pickle=True).item()

    print("\n\nProject = ", str(data["project"]))
    if(int(sys.argv[7]) == 0):
            
        print("FC = ", str(data["fc"]/10**6) + " MHz ")
        print("FS = ", str(data["fs"]/10**6) + " MHz ")
    
    else:
        print("Start = " , str(data["start"]/10**6) + " MHz ")
        print("Stop = " , str(data["stop"]/10**6) + " MHz ")
        print("Step =  " , str(data["step"]/10**6) + " MHz ")

    print("Integration Time = ", data["integration_time"] , "**Currently Not Working**")
    print("Total Time for Obs = ", data["time_for_obs"] , " s")
    print("Data Acquiring Method = " , data["which_method"] , "\n\n")

    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    sec = int(sys.argv[6]) 

    if(sec >= 60):
        sec -= 60
        minute += 1
        if(minute >= 60):
            minute -= 60
            hour += 1
            if(hour >= 24):
                hour -= 24
                day += 1

    sch_time = datetime.datetime(year , month , day , hour , minute , sec, 0)
    
    # if(int(sys.argv[6]) + data["time_for_obs"] >= 60):
    #     stop_time = datetime.datetime(year , month , day , hour , minute + 1 , sec + data["time_for_obs"] - 60, 0)
    
    incre_sec = data["time_for_obs"]
    incre_min = 0
    incre_hour = 0
    incre_day = 0

    if(incre_sec >= 60):
        incre_min = int(incre_sec/60)
        incre_sec = incre_sec%60
        
        if(incre_min >= 60):
            incre_hour = int(incre_min/60)
            incre_min = incre_min%60

            if(incre_hour >= 24):
                incre_day = int(incre_hour/24)
                incre_hour = int(incre_hour%60)

    stop_time = datetime.datetime(year , month , day + incre_day, hour + incre_hour , minute + incre_min , sec + incre_sec , 0)

    print("Sch Execution Time = " , sch_time , "\n")
    print("\n\nSch Stop Time = " , stop_time , "\n")
    print("\033[F\033[F\033[F\033[F\033[F")
    
    while True:

        try:
                
            current_time = datetime.datetime.now()

            print("Current Time   = " , current_time , end="\r")

            time.sleep(0.1)

        except KeyboardInterrupt:

            print("\n\n\n\nExiting ....")
            exit(0)

x_term_display()