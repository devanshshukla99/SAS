#Program to plot dynamic spectrum

import numpy as np 
from pylab import *

"""
Devansh Shukla

"""

path = sys.argv[1]
# path_split = path.split("/")
# project = path_split[1]

# b = zeros((50,512) , dtype=float)

a1 = np.fromfile(str(path), dtype = 'float32')

b1 = a1.reshape(int(len(a1)/512) , 512)

b = b1

fig = figure()

ima = imshow(b , cmap="twilight" , aspect="auto" , interpolation="nearest")
# clim(-1e-6 , 1e-6)
colorbar()

# x_positions = np.arange(0,len(b),1) # pixel count at label position
# x_labels = range(int(80e6),int(100e6),1) # labels you want to see
# plt.xticks(x_positions, x_labels)

# fig.savefig(str(project) + "/plots/" + str(sys.argv[2])  + "_ds.pdf")

# show()

fig2 = figure()

c = np.transpose(b)

e = np.mean(c, axis=1) # average data values for each frequency bin

xlabel('Frequency in MHz')
ylabel('Relative Power in dB')

plot(e)

# fig2.savefig(str(project) + "/plots/" + str(sys.argv[2])  + "_pvsf.pdf")

# print("\n Saved 2 Figs\n")

show()
