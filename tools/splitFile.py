# splitFile.py
# This method splits a SQL Dump file into each individual file
import sys
import os
import glob
import re
sys.path.insert(1, '../')
import ui

def splitByCreate(name):
    #input file
    fin = open(name, "rt")
    #output file to write the first lines
    fout = open(name[:-4]+"pg.sql", "wt")
    newfile = False
    #make new directory
    path = os.path.dirname(os.path.abspath(name)) + "/" + os.path.splitext(os.path.basename(name))[0] + "/"
    if not os.path.exists(path):
        os.mkdir(path)

    # for each line in the input file
    for line in fin:
        # Mark key lines to divide files
        namere = re.search('(CREATE OR ?\w+? ? \w+ +?)(\w+\.\w+)( ?\(?)',line)
        if namere:
            name = namere.group(2)
            newfile = True
            fout.close()
            fout = open(path+name+".sql", "wt")
        else:
            newfile = False
        # Write modified line in output file
        fout.write(line)

    #close input and output files
    print("Modified " + fout.name)
    fin.close()
    fout.close()


# call main
for name in ui.selectFile():
    splitByCreate(name)

