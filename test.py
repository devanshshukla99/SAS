
import os
import subprocess
import io
import sys
#import x_term_display

os.system("clear")

print(sys.argv)

_rfi_ = False


if(len(sys.argv) > 1 and "-rfi" in sys.argv):
    
    _rfi_ = True
    
    for _i_ in range(0, len(sys.argv)):

        _n_ = sys.argv[_i_].find("rfi")

        if(_n_ != -1):
            
            _freq_string = sys.argv[_i_ + 1]
            _freq_string = _freq_string.split(":")

            start = int(_freq_string[0]) * 10**6
            stop = int(_freq_string[1]) * 10**6
            step = int(_freq_string[2]) * 10**6

            print(start , stop , step)

        else:
            pass
                
else:
    _rfi_ = False
