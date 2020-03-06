#Program to find peaks

from scipy.signal import *
from numpy import *
from pylab import *
import sys
import os

"""
Remove DC
Normalize Data
Noise Floor
Sys Argv
"""

noise_floor = fromfile("/home/devansh/Desktop/SAS/11RXTSSPMO/NoiseFloorLinear/data/0.bin" , dtype="float32")

path = sys.argv[1]

if(path[-1] == '/'):
    path = path[:-1]

no_of_files = os.system("ls -l " + path + "/data/" + " | grep .bin | wc -l")

if(os.path.isdir(path + "/outcomes/") == False):

    os.system("mkdir " + path + "/outcomes/")

start_stop_n = loadtxt(path + "/StartStop_n.txt" , delimiter=" ")

peak_file = open(path + "/outcomes/peaks.txt" , "w")

peak_file.write("SFreq")
peak_file.write("  ")
peak_file.write("File No.")
peak_file.write("  ")
peak_file.write("Pos")
peak_file.write("\t")
peak_file.write("Height")
peak_file.write("\t\t\t\t\b\b\b\b")
peak_file.write("Freq")
peak_file.write("\n")

for i in range(0, no_of_files):

    data = fromfile(path + "/data/" + str(i) + ".bin" , dtype="float32")

    data = data.reshape((int(len(data)/512) , 512))
    data = mean(data , axis=0)
    data -= noise_floor

    data *= 10**6

    peak, height = find_peaks(data , height=1 , distance=20)
        
    print(peak)
    print(height)

    freq = (start_stop_n[i][1])

    for n in range(0 , len(peak)):
        
        freq = (start_stop_n[i][1]) 
        peak_file.write(str(freq))
        peak_file.write("\t")

        freq = freq*10**6 + peak[n]*(2*10**6/512)
        
        peak_file.write(str(i))
        peak_file.write("\t")
        
        peak_file.write(str(peak[n]))
        peak_file.write("\t")
        
        peak_file.write(str(round(height["peak_heights"][n] , 6)))
        peak_file.write("\t\t")
        
        peak_file.write(str(freq/10**6))
        
        peak_file.write("\n")

    if(len(peak) != 0):
        
        fig = figure()
        plot(data)
        plot(peak , data[peak] , 'x')
        # ylim(-2 , 40)
        title(str(start_stop_n[i][1]) + " to " + str(start_stop_n[i][2]))
        #show()
        fig.savefig(path + "/outcomes/" + str(i) + ".pdf")

peak_file.close()

print("python3 pdf_merger_peak_finder.py " + path + "/outcomes/")

a = os.popen("python3 pdf_merger_peak_finder.py " + path + "/outcomes/").read()

print(a)