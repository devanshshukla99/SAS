#Program for system time clock sync

"""
Requires Internet Connection

Reference
https://pypi.org/project/ntplib/

"""

"""
Devansh Shukla

"""

import os
import ntplib           # pip3 install ntplib
from datetime import datetime, timezone

def check_sync():

    try:

        #print("\n Connecting to NTP Server")
        c = ntplib.NTPClient()
        # Provide the respective ntp server ip in below function
        response = c.request('time.nplindia.org', version=3)
        #print(response.offset) 
        #print(ntplib.leap_to_text(response.leap))

        server_time = datetime.fromtimestamp(response.tx_time) 
        current_time = datetime.now()

        t1 = server_time.timestamp()
        
        #print(t1)
        t2 = current_time.timestamp()
        #print(t2)

        print("Difference in Sync is " , t2 - t1 , "s")

    except:

        print("Required Internet Connection")

        exit(0)

check_sync()
