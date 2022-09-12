# fastCombine.py
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
start_time = time.time()

# Read file write to dump
def splitByCreate(name):

    #input file
    fin = open(name, "rt")

    # put lines in string file
    file = ""
    for line in fin:
        file = file + line

    fin.close()
    return file


# Main function called on button press
def makeScript(directory, varlist, root):
    selected = [directory[x] for x in range(len(directory)) if varlist[x].get()]
    # Get current dir
    current = os.getcwd()

    # Get all files under chosen folders
    files = []
    for d in selected:
        onlyfiles = glob.glob(current+"\\"+d+"\\*.sql")
        files = files + onlyfiles

    text = ""
    # Create dump
    if files:
        # compile text
        for name in files:
            text = text + splitByCreate(name) + "\n"

        # write file at once
        dump = open("UpdateScript.sql", "w") 
        dump.write(text)
        dump.close()
        print("UpdateScript.sql" + " generated")
        tk.messagebox.showinfo(title="Notice", message="UpdateScript.sql generated in " + str(time.time() - start_time) + "seconds")
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


