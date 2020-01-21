#Function for rfi data collect

"""
Change Log

Simultaneous Graph Plot and Save

Adding 1/2 Step Overlap
Process Management

"""

"""
Devansh Shukla

"""

from numpy import *
import __main__
import subprocess
import os
import datetime
import sync_6

def data_acq_from_rtl_power_fftw_rfi(__n__ , start , stop_ , check_devices , data , _sch_ , sch_h , sch_m , sch_s , file_start_stop_n):

    out = []

    if(_sch_ == True and __n__ == 0):
        sync_6.exec(sch_h , sch_m , sch_s)

    # __main__.log("Starting Acquisition at " , datetime.datetime.now())

    for n in range(0, int(check_devices)):

        out.append(open("./" + str(data["project"]) + "/logs/log_rlt_" + str(__n__) + ".txt" , "w"))

        work = "rtl_power_fftw -f " + str(start) + ":" + str(stop_) + " -l -e " + str(data["time_for_obs"]) + " -t " + str(data["integration_time"]) + " -m " + "./" + str(data["project"]) + "/data/" + str(__n__) + " -g 4 -d " + str(n)  # , "rtl_power_fftw -f 92M:94M -e 10 -t 10 -m obs -g 0 -d 1"]
        __main__.log(work)
        p = subprocess.Popen(work, shell=True, stdout=out[n], stderr=out[n])
        
        work_plot = "xterm -e python3 survey_1_with_save.py " + "./" + str(data["project"]) + "/data/ " + str(int(__n__) - 1)
        print(work_plot)
        r = subprocess.Popen(work_plot, shell=True, stdout=None, stderr=None)

    __main__.log("Acq Starting ") # at ", datetime.datetime.now())

    __main__.log("Starting Acquisition at " , datetime.datetime.now())

    # file_process_gene.write(str(p.pid))
    # file_process_gene.write("\n")

    file_start_stop_n.write(str(__n__))
    file_start_stop_n.write(" ")
    file_start_stop_n.write(str(start/1e6))
    file_start_stop_n.write(" ")
    file_start_stop_n.write(str(stop_/1e6))
    file_start_stop_n.write("\n")
    
    p.wait()

    if(p.poll() != 0):

        p.kill()
        os.system("kill -9 " + str(p.pid + 1))
        log("\n Killed" , p.pid)
        

def ACQ_RFI(data , check_devices , _rfi_ , _sch_ , sch_h , sch_m , sch_s):

    file_start_stop_n = open("./" + str(data["project"]) + "/StartStop_n.txt" , 'w')
    # file_process_gene = open("./" + str(data["project"]) + "/process.txt" , 'w')
    
    start = data["start"]
    stop_ = data["start"] + data["step"]

    __n__ = 0

    try:

        if(os.path.isdir("./" + str(data["project"]) + "/logs/") == False):
            os.system("mkdir ./" + str(data["project"]) + "/logs/")
        if(os.path.isdir("./" + str(data["project"]) + "/data/") == False):
            os.system("mkdir ./" + str(data["project"]) + "/data/")
        if(os.path.isdir("./" + str(data["project"]) + "/plots/") == False):
            os.system("mkdir ./" + str(data["project"]) + "/plots/")
        
    except:

        log("**Error Creating Dirs**")

    while(stop_ <= data["stop"]):

        data_acq_from_rtl_power_fftw_rfi(__n__ , start , stop_ , check_devices , data , _sch_ , sch_h , sch_m , sch_s , file_start_stop_n)

        __n__ += 1
        
        start = start + (data["step"]/2)

        stop_ += (data["step"]/2)

    work_plot = "xterm -e python3 survey_1_with_save.py " + "./" + str(data["project"]) + "/data/ " + str(int(__n__) - 1)
    r = subprocess.Popen(work_plot, shell=True, stdout=None, stderr=None)

    r.wait()

    if(r.poll() != 0):

        r.kill()
        os.system("kill -9 " + str(r.pid + 1))
        log("\n Killed" , r.pid)
    

    work_merge = "python3 pdf_merger.py " + "./" + str(data["project"]) + "/plots/" + " " + str(__n__)
    s = os.system(work_merge)
    
    work_merge = "python3 pdf_merger_pvsf.py " + "./" + str(data["project"]) + "/plots/" + " " + str(__n__)
    s = os.system(work_merge)
    
    file_start_stop_n.close()
    # file_process_gene.close()


