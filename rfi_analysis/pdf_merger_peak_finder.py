from PyPDF2 import PdfFileMerger
import sys
import numpy as np
import os

"""
Devansh Shukla

"""

pdfs = []

path = sys.argv[1]

if(path[-1] != "/"):
    path = path + "/"

files = os.popen("ls " + path).read()
files = files.split("\n")


pdfs_n = []

for i in range(0,len(files)):

    if(files[i].find(".pdf") != -1 and files[i].find("result") == -1):
        pdfs_n.append(files[i])

a = []

for i in range(0 , len(pdfs_n)):  
    a.append(int(pdfs_n[i][:-4])) 

a = np.array(a)
a = np.sort(a)

pdfs_n = [] 
    
for i in range(0 , len(a)): 
    pdfs_n.append(str(a[i]) + ".pdf") 

print(pdfs_n)

for i in range(0, len(pdfs_n)):

    pdfs.append(str(path) + str(pdfs_n[i]))

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write(str(path) + "result_peak_finder.pdf")
merger.close()