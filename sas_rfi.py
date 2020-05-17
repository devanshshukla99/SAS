# Program for Data Acquisation from RTL-SDR With RFI ACQ

"""

Created By Dev and Yash

Change Log

Adding data["project"] Name with its Folder
Using Dictionaries

"""

"""
-ns : No Sync
-sch : Scheduled Time || now
-rfi : RFI Module
"""


def for_time():

    _a_ = datetime.datetime.now()

    _a_ = _a_.strftime("%Y%m%d:%H%M%S")
    
    return _a_

from numpy import *
from pylab import *
import time
import os
import subprocess
import io
import sync_6
import sys
import datetime
import rfi
#import x_term_display

os.system("clear")

if(len(sys.argv) > 1 and "-h" in sys.argv):
    
    print("Useage")

    print("\t\t-ns No NTP Sync")
    print("\t\t-rfi Start:Stop:Step")
    print("\t\t-sch now | hh:mm:ss")

    exit(0)

print(sys.argv)

_rfi_ = False

if(len(sys.argv) > 1 and "-ns" in sys.argv):
    pass
else:
    import sys_sync

def find_in_array(__A__ , s):

    for _i_ in range(0, len(__A__)):

        _n_ = __A__[_i_].find(s)

        if(_n_ != -1):
            return _i_, _n_

    if(_n_ == -1):
        return -1, -1
    
_pos_, _n_ = find_in_array(sys.argv , "-rfi")

# print(_pos_ , _n_)

if(len(sys.argv) > 1 and _n_ != -1):
    
    _rfi_ = True

    _freq_string = sys.argv[_pos_ + 1]
    _freq_string = _freq_string.split(":")
    
    start = int(_freq_string[0]) * 10**6
    stop = int(_freq_string[1]) * 10**6
    step = int(_freq_string[2]) * 10**6

    # print(start , stop , step)
            
else:
    _rfi_ = False

_pos_, _n_ = find_in_array(sys.argv , "-sch")

# print(_pos_ , _n_)

scheduled_time = ""
sch_h = 0
sch_m = 0
sch_s = 0

x_term_pid = 0

_sch_ = True

if(len(sys.argv) > 1 and _n_ != -1):
    
    _sch_ = True
    _sch_cli = True

    _freq_string = sys.argv[_pos_ + 1]
    
    if(_freq_string == "now"):
    
        _sch_ = False
        _sch_cli = False
        scheduled_time = "now"
    
    else:

        _freq_string = _freq_string.split(":")
        
        sch_h = int(_freq_string[0])
        sch_m = int(_freq_string[1])
        sch_s = int(_freq_string[2])
        
            
else:
     _sch_cli = False


if(_rfi_ == False):
    
    data = {"project" : "" , "fc" : 34.5e6 , "fs" : 2.4e6 , "integration_time" : 1.0 , "time_for_obs" : 10 , "which_method" : 0}

elif(_rfi_ == True):

    data = {"project" : "" , "start" : 0 , "stop" : 0 , "step" : 0 , "integration_time" : 1.0 , "time_for_obs" : 10 , "which_method" : 2}
    
    data["start"] = start
    data["stop"] = stop
    data["step"] = step

now_ = datetime.datetime.now()
    
y = int(str(now_)[0:4])
m = int(str(now_)[5:7])
d = int(str(now_)[8:10])
    
t1 = 0.0
t2 = 0.0

no_of_sdr_devices = 0
flag = 0
flag2 = 1

# which_method = 0            # 0 for rtl_sdr 1 for rlt_power_fftw

# check_and_read_data()

if(os.path.isdir("./logs") == False):
    os.system("mkdir logs")

time_of_creation = for_time()

file_log = open("./logs/log" + str(time_of_creation) + ".txt", "w")
file_log.write(time.ctime())
file_log.write("\n")


#file_data = open("data.txt" , "w")
file_data_name = "data"

def data_acq_int_time_same_as_total_time(_fc_, _fs_, _bw_=3.0e6):

    #file_name = "obs"
    os.system("rtl_power_fftw -f " + str(_fc_ - 1.0) + ":" + str(_fc_ + 1.0) + " -t " + str(data["time_for_obs"]) + " -m " + "obs" + " -g " + str(0))


def data_acq_from_rtl_power_fftw_old():

    global data, sch_h, sch_m, sch_s, _sch_

    out = []
    
    if(_sch_ == True):
        sync_6.exec(sch_h , sch_m , sch_s)

    for n in range(0, int(check_devices)):

        out.append(open("log_test_" + str(n) + ".txt" , "w"))

        work = "rtl_power_fftw -f " + str(data["fc"] - 10**6) + ":" + str(data["fc"] + 10**6) + " -e " + str(data["time_for_obs"]) + " -t " + str(data["integration_time"]) + " -m " + "./" + str(data["project"]) + "/" + str(n) + " -g 0 -d " + str(n)  # , "rtl_power_fftw -f 92M:94M -e 10 -t 10 -m obs -g 0 -d 1"]
        log(work)
        p = subprocess.Popen(work, shell=True, stdout=out[n], stderr=out[n])

    log("Acq Starting")
    p.wait()

def data_acq_from_rtl_power_fftw():

    global data, sch_h, sch_m, sch_s, _sch_, scheduled_time

    out = []

    file_start_stop_n = open("./" + str(data["project"]) + "/StartStop_n.txt" , 'w')

    try:

        if(os.path.isdir("./" + str(data["project"]) + "/logs/") == False):
            os.system("mkdir ./" + str(data["project"]) + "/logs/")
        if(os.path.isdir("./" + str(data["project"]) + "/data/") == False):
            os.system("mkdir ./" + str(data["project"]) + "/data/")
        if(os.path.isdir("./" + str(data["project"]) + "/plots/") == False):
            os.system("mkdir ./" + str(data["project"]) + "/plots/")
    
    except:

        log("**Error Creating Dirs**")
    
    if(_sch_ == True and scheduled_time != "now"):
        sync_6.exec(sch_h , sch_m , sch_s)

    for n in range(0, int(check_devices)):

        out.append(open("log_test_" + str(n) + ".txt" , "w"))

        work = "rtl_power_fftw -f " + str(data["fc"] - 10**6) + ":" + str(data["fc"] + 10**6) + " -e " + str(data["time_for_obs"]) + " -t " + str(data["integration_time"]) + " -m " + "./" + str(data["project"]) + "/data/" + str(n) + " -g 4 -d " + str(n)  # , "rtl_power_fftw -f 92M:94M -e 10 -t 10 -m obs -g 0 -d 1"]
        log(work)
        p = subprocess.Popen(work, shell=True, stdout=out[n], stderr=out[n])

        file_start_stop_n.write(str(n))
        file_start_stop_n.write(" ")
        file_start_stop_n.write(str((data["fc"] - 10**6)/1e6))
        file_start_stop_n.write(" ")
        file_start_stop_n.write(str((data["fc"] + 10**6)/1e6))
        file_start_stop_n.write("\n")


    log("Acq Starting")
    p.wait()

    if(p.poll() != 0):

        p.kill()
        os.system("kill -9 " + str(p.pid + 1))
        log("\n Killed" , p.pid)

    file_start_stop_n.close()

    print("python3 new_subtract_noise_floor.py ./" + data["project"] + "/data/" + " -log")
    os.system("python3 new_subtract_noise_floor.py ./" + data["project"] + " -log")
    
def data_acq_from_rtl_sdr_old():

    global data, sch_h, sch_m, sch_s, scheduled_time

    out = []

    if(scheduled_time != "now"):

        sync_6.exec(sch_h , sch_m , sch_s)

    t2 = time.perf_counter()

    log("\n\n"  , " t2-t1 = " , t2 - t1 , "\n\n")
   
    for n in range(0, int(check_devices)):

        out.append(open("log_test_" + str(n) + ".txt" , "w"))

        work = "rtl_sdr -f " + str(data["fc"]) + " -g 0 -s " + str(data["fs"]) + " -n " + str(data["fs"]*data["time_for_obs"]) + " -d " + str(n) + " " +  "./" + str(data["project"]) + "/" + str(n) +".dat"+">junk"
        log(work)
        print(work)
        p = subprocess.Popen(work, shell=True, stdout=out[n], stderr=out[n])

    log("Acq Starting")
    p.wait()


def data_acq_from_rtl_sdr():

    global data, sch_h, sch_m, sch_s, scheduled_time

    out = []

    file_start_stop_n = open("./" + str(data["project"]) + "/StartStop_n.txt" , 'w')

    try:

        if(os.path.isdir("./" + str(data["project"]) + "/logs/") == False):
            os.system("mkdir ./" + str(data["project"]) + "/logs/")
        if(os.path.isdir("./" + str(data["project"]) + "/data/") == False):
            os.system("mkdir ./" + str(data["project"]) + "/data/")
        if(os.path.isdir("./" + str(data["project"]) + "/plots/") == False):
            os.system("mkdir ./" + str(data["project"]) + "/plots/")
    
    except:

        log("**Error Creating Dirs**")

    log("hello" , scheduled_time)

    if(scheduled_time != "now"):

        sync_6.exec(sch_h , sch_m , sch_s)

    t2 = time.perf_counter()

    log("\n\n"  , " t2-t1 = " , t2 - t1 , "\n\n")

    for n in range(0, int(check_devices)):
        
        for _times_ in range(0, data["time_for_obs"]):

            out.append(open("log_test_" + str(n) + ".txt" , "w"))

            work = "rtl_sdr -f " + str(data["fc"]) + " -g 0 -s " + str(data["fs"]) + " -n " + str(data["fs"]) + " -d " + str(n) + " " +  "./" + str(data["project"]) + "/data/" + str(_times_) +".dat"+">junk"
            log(work)
            # print(work)
            p = subprocess.Popen(work, shell=True, stdout=out[n], stderr=out[n])

            # time.sleep(2)

            p.wait()

            if(p.poll() != 0):

                p.kill()
                os.system("kill -9 " + str(p.pid + 1))
                log("\n Killed" , p.pid)

            file_start_stop_n.write(str(_times_))
            file_start_stop_n.write(" ")
            # file_start_stop_n.write(str(start/1e6))
            # file_start_stop_n.write(" ")
            # file_start_stop_n.write(str(stop_/1e6))
            file_start_stop_n.write("\n")


    log("Acq Starting")

    file_start_stop_n.close()
    
def data_acq():

    global data, _rfi_, _sch_, sch_h, sch_m, sch_s

    if(data["which_method"] == 0):

        data_acq_from_rtl_sdr()

    elif(data["which_method"] == 1):

        data_acq_from_rtl_power_fftw()

    if(_rfi_ == True):
        rfi.ACQ_RFI(data , check_devices , _rfi_ , _sch_ , sch_h , sch_m , sch_s)

def log(*args):

    global file_log

    out = ""

    for i in range(0, len(args)):
        file_log.write(str(args[i]))

        out += str(args[i])

    print(out)

    file_log.write("\n")


def check_sdr_devices():

    a_out = str(subprocess.check_output("lsusb", shell=True))
    a_out = a_out.split("\\")

    global check_devices
    check_devices = 0

    for i in a_out:

        if("DVB" in i):
            check_devices += 1

    return check_devices


def write_data():

    global file_data_name, data 

    save("data" , data , allow_pickle=True)

    log("Data Written to file")


def check_and_read_data():

    global file_data_name , data , flag

    if(os.path.isfile("data.npy") == True):

        _data_ = load("data.npy" , allow_pickle=True).item()
        
        if(_rfi_ == False):
            data = _data_
            
        else:
            data["project"] = _data_["project"]
            data["integration_time"] = _data_["integration_time"]
            data["time_for_obs"] = _data_["time_for_obs"]

        flag = 1

def data_enter():

    global data, no_of_sdr_devices, flag, flag2, scheduled_time, sch_h, sch_m, sch_s, _rfi_

    print("Enter Project Name")
    data["project"] = str(input())

    if(_rfi_ == False):
        print("Enter CF in MHz")
        data["fc"] = float(input())
        data["fc"] = data["fc"]*10**6
        print("Enter FS in MHz")
        data["fs"] = float(input())
        data["fs"] = data["fs"]*10**6

        if(data["fs"] > 2.56e6):
            log("**Not Valid**")
            log("**Setting fs to 2.4 MHz**")
            data["fs"] = 2.4e6

    print("Enter Integration Time ")
    data["integration_time"] = float(input())
    print("Enter Total Time")
    data["time_for_obs"] = int(input())

    if(data["integration_time"] > data["time_for_obs"]):
        log("**Integration Time and Total Time for obs NOT VALID**")
        log("**Setting Integration Time = ", data["time_for_obs"], "**")

    print("\n")
    
    if(_rfi_ == False):

        print("Data Acquiring Method 0 for rtl_sdr and 1 for rtl_power_fftw")
        data["which_method"] = int(input())

        if(data["which_method"] != 0 and data["which_method"] != 1):
            log("**Data Acquiring Method NOT VALID**")
            log("**Setting value to 0(default)**")
    
    
        print("\n")

    write_data()

    log("Project = ", str(data["project"]))
    if(os.path.isdir("./" + str(data["project"])) == False):
        os.system("mkdir " + data["project"])
    else:
        print("Project Folder Already Exists Overwrite..? y:n")
        over_write_data_project = input()
        log("Project Folder Already Exists Overwrite..? y:n " + str(over_write_data_project))

        if(over_write_data_project=="n" or over_write_data_project=="no"):
            print("Enter new Project Name")
            old_project = data["project"]
            data["project"] = input()
            log(old_project + " > " + data["project"] )
            try:
                os.system("mkdir " + data["project"])
            except:
                log("**Directory Already Exists**")
                log("**Even Then Using " + data["project"] + " as Project Name**")

        write_data()

    log("\nProject = " , str(data["project"]))
    
    if(_rfi_ == False):
            
        log("FC = ", str(data["fc"]/10**6) + " MHz ")
        log("FS = ", str(data["fs"]/10**6) + " MHz ")
    else:
        log("Start = " , str(data["start"]/10**6) + " MHz ")
        log("Stop = " , str(data["stop"]/10**6) + " MHz ")
        log("Step =  " , str(data["step"]/10**6) + " MHz ")
        
    log("Integration Time = ", data["integration_time"] , "**Currently Not Working**")
    log("Total Time for Obs = ", data["time_for_obs"])
    log("Data Acquiring Method = " , data["which_method"] , "\n")


def menu():

    global data, no_of_sdr_devices, flag, flag2, scheduled_time, sch_h, sch_m, sch_s, _sch_, _rfi_, y, m, d, x_term_pid

    check_and_read_data()
    
    if(flag == 0 or flag2 == 0):

        print("Enter Project Name")
        data["project"] = str(input())

        if(_rfi_ == False):             # If Not RFI Scan
                
            print("Enter CF in MHz")
            data["fc"] = float(input())
            data["fc"] = data["fc"]*10**6
            print("Enter FS in MHz")
            data["fs"] = float(input())
            data["fs"] = data["fs"]*10**6

            if(data["fs"] > 2.56e6):
                log("**Not Valid**")
                log("**Setting fs to 2.4 MHz**")
                data["fs"] = 2.4e6

        print("Enter Integration Time **Currently Not Working**")
        data["integration_time"] = float(input())
        print("Enter Total Time")
        data["time_for_obs"] = int(input())

        if(data["integration_time"] > data["time_for_obs"]):
            log("**Integration Time and Total Time for obs NOT VALID**")
            log("**Setting Integration Time = ", data["time_for_obs"], "**")

        print("\n")
        
        if(_rfi_ == False):

            print("Data Acquiring Method 0 for rtl_sdr and 1 for rtl_power_fftw")
            data["which_method"] = int(input())

            if(data["which_method"] != 0 and data["which_method"] != 1):
                log("**Data Acquiring Method NOT VALID**")
                log("**Setting value to 0(default)**")

        print("\n")

        write_data()

    log("Project = ", str(data["project"]))
    if(os.path.isdir("./" + str(data["project"])) == False):
        os.system("mkdir " + data["project"])
    else:
        print("Project Folder Already Exists Overwrite..? y:n")
        over_write_data_project = input()
        log("Project Folder Already Exists Overwrite..? y:n " + str(over_write_data_project))

        if(over_write_data_project=="n" or over_write_data_project=="no"):
            print("Enter new Project Name")
            old_project = data["project"]
            data["project"] = input()
            log(old_project + " > " + data["project"] )
            try:
                os.system("mkdir " + data["project"])
            except:
                log("**Directory Already Exists**")
                log("**Even Then Using " + data["project"] + " as Project Name**")

        write_data()
    
    log("\nProject = " , str(data["project"]))
        
    if(_rfi_ == False):
        
        log("FC = ", str(data["fc"]/10**6) + " MHz ")
        log("FS = ", str(data["fs"]/10**6) + " MHz ")
    else:
        log("Start = " , str(data["start"]/10**6) + " MHz ")
        log("Stop = " , str(data["stop"]/10**6) + " MHz ")
        log("Step =  " , str(data["step"]/10**6) + " MHz ")
        
    log("Integration Time = ", data["integration_time"] , "**Currently Not Working**")
    log("Total Time for Obs = ", data["time_for_obs"])
    log("Data Acquiring Method = " , data["which_method"] , "\n")

    print("\n", "Press 'y' to Continue")
    t = input()

    if(t == 'y'):
        pass

    elif(t == 'q'):
        exit(0)

    else:
        flag2 = 0
        data_enter()

    no_of_sdr_devices = check_sdr_devices()

    log("Found ", no_of_sdr_devices, " SDR Devices")
    
    if(_sch_ == True and _sch_cli == False):
            
        print("Enter the Scheduled Time for starting Acquisation in hh:mm:ss format \n Enter now for No Scheduled Time")
        scheduled_time = input()
        
        try:
            sch_h = int(scheduled_time[0:2])
            sch_m = int(scheduled_time[3:5])
            sch_s = int(scheduled_time[6:8])

        except:

            if(scheduled_time == "now"):
                _sch_ = False

    if(_sch_ == True):

        ## Checking for correct sch time ##

        now_ = datetime.datetime.now()
        
        # y = int(str(now_)[0:4])
        # m = int(str(now_)[5:7])
        # d = int(str(now_)[8:10])

        exec_time = datetime.datetime(y, m, d, sch_h, sch_m, sch_s, 0)

        print(exec_time)
                
        if(exec_time.timestamp() < now_.timestamp()):
            print("\n\n **Invalid Sch Time** \n\n")
            exit(0)

            ## Checking Completed ##
            
        log("Scheduled Acquisation Time is " , exec_time) #str(sch_h) + ":" + str(sch_m) + ":" + str(sch_s))

    _work_ = "xterm -hold -e python3 x_term_display.py " + str(y) + " " + str(m) + " " + str(d) + " " + str(sch_h) + " " + str(sch_m) + " " + str(sch_s) + " " + str(int(_rfi_))

    print(_work_)    

    # if(_rfi_ == True):

    #     _work_ = "xterm -hold -e python3 x_term_display.py " + str(y) + " " + str(m) + " " + str(d) + " " + str(sch_h) + " " + str(sch_m) + " " + str(sch_s) + " 1"

    q = subprocess.Popen(_work_, shell=True , stdout=None , stderr=None)

    x_term_pid = q.pid

    log("Current Time is ", str(datetime.datetime.now()))
    # log("Sleeping for 2s")

    # time.sleep(2)
    
print("Welcome to SAS")

menu()

if(check_devices >= 1):
        
    log("Current Time is " + str(datetime.datetime.now()))
    log("Starting Acquisation Timer")

    data_acq()

    log("Stopping Acquisation")
    log("Acquisation Completed at " , str(datetime.datetime.now()))

else:

    log("\nConnect SDR Device(s) ....")
    log("Exiting ........")

file_log.close()
os.system("cp -a " + "./logs/log" + str(time_of_creation) + ".txt" " ./" + data["project"] + "/")

print("kill -9 " + str(x_term_pid))

os.system("kill -9 " + str(x_term_pid+1))

