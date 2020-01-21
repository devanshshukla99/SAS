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

def sys_sync_():

    try:

        print("Connecting to NTP Server")
        
        os.system("sudo ntpdate -d -u -q time.nplindia.org")

        print("System Time Synced\n")

    except:

        print("Required Internet Connection")

        exit(0)

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

        global __t__
        __t__ = t2 - t1                         # System Time - Server Time

        #print("Difference in Sync is " , __t__ , "s")

    except:

        print("Required Internet Connection")

        exit(0)

__t__ = 0.5

#while(abs(__t__) >= 0.5):
    
sys_sync_()

check_sync()

print("Difference in Sync is " , __t__ , "s " , "(SysT - ServerT)\n")

corrected_time = datetime.now().timestamp() - __t__


