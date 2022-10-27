# combineFile.py
# This method combined all selected sql files to a single dump.sql
import sys
import os
import glob
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from os import listdir
from os.path import isfile, join

# Track time
import time

# Read file write to dump
def splitByCreate(name, dump):
    # input file
    fin = open(name, "rb")
    line = fin.read()

    # write block to dump
    dump.write(line)

    #close input and output files
    fin.close()

# Main function called on button press
def makeScript(directory, varlist, root):
    # Track time on button press
    start_time = time.time()
    selected = [directory[x] for x in range(len(directory)) if varlist[x].get()]
    # Get current dir
    current = os.getcwd()

    # Get all files under chosen folders
    files = []
    for d in selected:
        onlyfiles = glob.glob(current+"\\"+d+"\\*.sql")
        files = files + onlyfiles
        onlyfiles = glob.glob(current+"\\"+d+"\\**\\*.sql")
        files = files + onlyfiles

    # Create dump
    if files:
        dump = open("UpdateScript.sql", "wb") 
        # call main
        for name in files:
            splitByCreate(name, dump)

        dump.close()
        print("UpdateScript.sql" + " generated")
        tk.messagebox.showinfo(title="Notice", message="UpdateScript.sql generated in " + str(round(time.time() - start_time, 2)) + "seconds")
    else:
        print("No files selected")
        tk.messagebox.showinfo(title="Notice", message="No files selected")

    root.quit()


# Get current directories
directory = next(os.walk('.'))[1]

# GUI Selection
root = tk.Tk()
root.title('SQL updatescript tool')
root.geometry("600x800+120+120")

w = tk.Label(root, text ='Combine scripts from selected folders.', font = "50")
w.pack()

# Make checkbox
varlist = []
for x in range(len(directory)):
    varlist.append(tk.IntVar())
    l = tk.Checkbutton(root, text = directory[x],
            variable = varlist[x],
            onvalue = 1,
            offvalue = 0,
            height = 3,
            width = 20,
            anchor = "w")
    l.pack()

    # Select number prefix by default
    if directory[x][0].isdigit():
        l.select()

# Run button calls function
B = tk.Button(root, text = "Run", command = lambda: makeScript(directory, varlist, root), height = 1, width = 10)
B.pack(pady=10)

root.mainloop()


