# csreplace.py
# This method treats all the .cs files under selected folders containing NpgSql
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

# Read, replace then write to new file
def processCS(name):

    dump = open(name[:-3]+"pg.cs", "wt") 
    # input file
    fin = open(name, "rt")
    block = fin.readlines()

    # write block to dump
    for line in block:
        line = line.replace("Aniki.SqlServer","Aniki.Postgres")
        line = line.replace("Repo.MSSql","Repo.NpgSql")
        line = line.replace("[SqlServerRepo]","[PostgresRepo]")
        line = line.replace("AppSqlServerDbContext", "AppPostgresDbContext")

        # variables
        line = line.replace('ParameterFactory.Create("@', 'ParameterFactory.Create("par_')
        line = line.replace("SqlDbType.", "NpgsqlDbType.")
        line = line.replace(".NVarChar", ".Varchar")
        line = line.replace(".VarChar", ".Varchar")
        line = line.replace(".Int", ".Integer")
        line = line.replace(".DateTime", ".Timestamp")
        line = line.replace(".UniqueIdentifier", ".Uuid")
        line = line.replace(".Bit", ".Boolean")
        line = line.replace(".VarBinary", ".Bytea")

        dump.write(line)


    #close input and output files
    dump.close()
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
        onlyfiles = sorted(glob.glob(current+"\\"+d+"\\**\\*.cs"))
        files = files + onlyfiles
        onlyfiles = sorted(glob.glob(current+"\\"+d+"\\*.cs"))
        files = files + onlyfiles

    if files:
        # Replace content for each file
        for name in files:
            processCS(name)

        print("cs processed")
        tk.messagebox.showinfo(title="Notice", message="Processed in " + str(round(time.time() - start_time, 2)) + "seconds")
    else:
        print("No files selected")
        tk.messagebox.showinfo(title="Notice", message="No files selected")

    root.quit()


# Get current directories
directory = next(os.walk('.'))[1]

# GUI Selection
root = tk.Tk()
root.title('Npgsql .cs replace tool')
root.geometry("600x800+120+120")

w = tk.Label(root, text ='Process .cs files from selected folders.', font = "50")
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


