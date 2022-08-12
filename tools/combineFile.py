# combineFile.py
# This method combined all selected sql files to a single dump.sql
import sys
import os
import glob
import re
from pathlib import Path
sys.path.insert(1, '../')
import ui


def splitByCreate(name):
    #input file
    fin = open(name, "rt")

    # for each line in the input file
    for line in fin:
        dump.write(line)

    dump.write("\n")

    #close input and output files
    fin.close()


files = ui.selectFile()
parentpath = Path(os.path.dirname(os.path.abspath(files[0]))).resolve().parent
dump =  open(str(parentpath) + "/"  + "dump.sql", "w") 
# call main
for name in files:
    splitByCreate(name)

print("dump.sql generated")
dump.close()

