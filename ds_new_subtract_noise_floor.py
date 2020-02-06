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


def find_in_array(__A__ , s):

    for _i_ in range(0, len(__A__)):

        _n_ = __A__[_i_].find(s)

        if(_n_ != -1):
            return _i_, _n_

    if(_n_ == -1):
        return -1, -1
    
_pos_, _n_ = find_in_array(sys.argv , "-log")

_liner_ = False

if(_n_ != -1):

    noise_floor_file_name = "./NF/data/0.bin"
    h = 5

    _liner_ = False

else:

    #noise_floor_file_name = "/home/devansh/Desktop/SAS/NoiseFloorLinear/data/0.bin"
    noise_floor_file_name = "./NFLiner/data/0.bin"
    h = 0.1

noise_floor = fromfile(noise_floor_file_name , dtype="float32")

if(len(sys.argv) < 2):
    print("\n Path Not Found")
    print("\n Useage -----")
    print("\n python3 ds_new_subtract_noise_floor.py path_to_project_folder")
    
path = sys.argv[1]

if(path[-1] == '/'):
    path = path[:-1]

if(os.path.isdir(path + "/snoisefloor/") == False):

    os.system("mkdir " + path + "/snoisefloor/")

start_stop_n = loadtxt(path + "/StartStop_n.txt" , delimiter=" ")

for i in range(0, 1):

    data = fromfile(path + "/data/" + str(i) + ".bin" , dtype="float32")

    print(i)
    
    data = data.reshape((int(len(data)/512) , 512))
    # data = mean(data , axis=0)
    data -= noise_floor
    
    # if(_liner_ == True):
    #     data *= 10**6

    freq = (start_stop_n[1])

    fig = figure()
    data_mean = mean(data , axis=0)
    plot(data_mean)
    # ylim(-2 , 40)
    title(str(start_stop_n[1]) + " to " + str(start_stop_n[2]))

    # b1 = data.reshape(int(len(data)/512) , 512)

    b = data

    fig = figure()

    ima = imshow(b , cmap="twilight" , aspect="auto" , interpolation="nearest")
    # clim(-1e-6 , 1e-6)
    colorbar()


    show()
    fig.savefig(path + "/snoisefloor/" + str(i) + ".pdf")
    close()

# print("python3 pdf_merger_peak_finder.py " + path + "/snoisefloor/")

# a = os.popen("python3 pdf_merger_peak_finder.py " + path + "/snoisefloor/").read()

# print(a)