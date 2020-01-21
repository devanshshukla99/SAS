#Program to find peaks

from scipy.signal import *
from numpy import *
from pylab import *
import sys
import os
import pandas as pd

"""
Remove DC
Normalize Data
Noise Floor
Sys Argv
"""

noise_floor_file_name = "/home/devansh/Desktop/SAS/SAS_E/SAS_12_2/NF/data/0.bin"
h = 0

_liner_ = False

noise_floor = fromfile(noise_floor_file_name , dtype="float32")

path = sys.argv[1]

if(path[-1] == '/'):
    path = path[:-1]

path_split = path.split("/")
project = path_split[-1]

if(os.path.isdir(path + "/outcomes/") == False):

    os.system("mkdir " + path + "/../outcomes/")

if(os.path.isdir(path + "/outcomes/" + project) == False):

    os.system("mkdir " + path + "/../outcomes/" + project)
    

start_stop_n = loadtxt(path + "/StartStop_n.txt" , delimiter=" ")

peak_data = {"SFreq" : [] , "File_No" : [] , "Pos" : [] , "Height" : [] , "Freq" : []}

SFreq_ = []
File_No_ = []
Pos_ = []
Height_ = []
Freq_ = []


for i in range(0, 1):

    data = fromfile(path + "/data/" + str(i) + ".bin" , dtype="float32")

    data = data.reshape((int(len(data)/512) , 512))
    data = mean(data , axis=0)
    data -= noise_floor

    if(_liner_ == True):

        data *= 10**6

    h = max(data)

    peak, height = find_peaks(data , height=h , distance=20)
        
    print(peak)
    print(height)

    freq = (start_stop_n[1])

    freq_plot = []

    if(len(peak) != 0):

        n = 0

        for n in range(0 , len(peak)):
            
            freq = (start_stop_n[1]) 
           
            freq = freq*10**6 + peak[n]*(2*10**6/512)
           
            SFreq_.append(start_stop_n[1])
            File_No_.append(i)
            Pos_.append(peak[n])
            Height_.append((round(height["peak_heights"][n] , 4)))
            Freq_.append(round(freq/10**6 , 2))
            freq_plot.append(round(freq/10**6 , 2))

        
        fig = figure()
        plot(data)
        plot(peak , data[peak] , 'x')
        xlabel("Frequency Channels")
        if(_liner_ == True):
            ylabel("Power(Liner) (1e-6)")
        else:
            ylabel("Power(Log)")

        #ylim(-2 , 40)
        title(str(start_stop_n[1]) + " to " + str(start_stop_n[2]))
        
        for k in range(0, len(freq_plot)):
            annotate("    " + str(freq_plot[k]) + " MHz",
                xy=(peak[k], data[peak[k]]),  # theta, radius    # fraction, fraction
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='left',
                verticalalignment='top',
                )
        show()
        fig.savefig(path + "/../outcomes/" + str(project) + "/" + str(i) + ".pdf")
        close()


peak_data["SFreq"] = SFreq_
peak_data["File_No"] = File_No_
peak_data["Pos"] = Pos_
peak_data["Height"] = Height_
peak_data["Freq"] = Freq_

df = pd.DataFrame(peak_data)

columnsTitles = ['SFreq' , 'File_No' , "Pos" , "Height" , "Freq"]

df = df.reindex(columns=columnsTitles)

print("**" , path + "/../outcomes/peaks" + str(project) + ".txt" )

df.to_csv(path + "/../outcomes/peaks" + str(project) + ".txt" , index=None , sep="\t")

print("python3 pdf_merger_peak_finder.py " + path + "/../outcomes/"  + str(project))

a = os.popen("python3 pdf_merger_peak_finder.py " + path + "/../outcomes/"  + str(project)).read()

print(a)