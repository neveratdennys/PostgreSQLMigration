# cleanattribute.py
# Remove excessive quotations and standardize capitalization
import sys
import os
import re
sys.path.insert(1, '../')
import ui

def cleanattribute(name):
    #input file
    fin = open(name, "rt")
    #output file to write the first lines
    fout = open(name[:-4]+"pg.sql", "wt")

    quote = False
    key = ''
    remove = False

    for line in fin:
        # " in line
        if ('"' in line):
            # loop over characters in the line
            for c in line:
                # mark start of quote
                if c == '"' and not quote:
                    quote = True
                # no space detected
                elif c == '"' and quote:
                    quote = False
                    remove = True
                    break
                # space detected in quotes
                if quote and c.isspace():
                    quote = False
                    break

            # remove quotes on true
            if remove:
                fout.write(line.replace('"', ''))
                remove = False
            else:
                fout.write(line)

        # write non affected lines
        else:
            fout.write(line)

    #close input and output files
    print("Modified " + fout.name)
    fin.close()
    fout.close()

# pass in file
for name in ui.selectFile():
    cleanattribute(name)

