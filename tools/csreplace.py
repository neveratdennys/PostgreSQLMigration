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

    # input file
    fin = open(name, "rt")
    block = fin.read()

    #write block to dump
    block = block.replace("Aniki.SqlServer","Aniki.PostgresSQL")
    block = block.replace("Repo.MSSql","Repo.NpgSql")
    block = block.replace("[SqlServerRepo]","[PostgresRepo]")
    block = block.replace("ApiSqlServerDbContext", "ApiPostgresDbContext")
    block = block.replace("SqlDataReader", "NpgsqlDataReader")
    block = block.replace("SqlParameter", "NpgsqlParameter")
    block = block.replace("SqlException", "NpgsqlException")

    # variables
    block = block.replace('ParameterFactory.Create("@', 'ParameterFactory.Create("par_')
    block = block.replace("SqlDbType.", "NpgsqlDbType.")
    block = block.replace("NpgsqlDbType.NVarChar", "NpgsqlDbType.Varchar")
    block = block.replace("NpgsqlDbType.VarChar", "NpgsqlDbType.Varchar")
    block = block.replace("NpgsqlDbType.Int,", "NpgsqlDbType.Integer,")
    block = block.replace("NpgsqlDbType.Int)", "NpgsqlDbType.Integer)")
    block = block.replace("NpgsqlDbType.BigInt", "NpgsqlDbType.Bigint")
    block = block.replace("NpgsqlDbType.DateTime", "NpgsqlDbType.Timestamp")
    block = block.replace("NpgsqlDbType.UniqueIdentifier", "NpgsqlDbType.Uuid")
    block = block.replace("NpgsqlDbType.Bit", "NpgsqlDbType.Boolean")
    block = block.replace("NpgsqlDbType.VarBinary", "NpgsqlDbType.Bytea")

    # input file closed
    fin.close()

    # overwrite input file
    dump = open(name, "wt") 
    dump.write(block)
    dump.close()

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


