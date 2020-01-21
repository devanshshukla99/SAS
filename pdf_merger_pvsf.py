from PyPDF2 import PdfFileMerger
import sys

"""
Devansh Shukla

"""

pdfs = []

path = sys.argv[1]
n = int(sys.argv[2])

for i in range(0, n):

    pdfs.append(str(path) + str(i) + "_pvsf.pdf")

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write(str(path) + "result_pvsf.pdf")
merger.close()