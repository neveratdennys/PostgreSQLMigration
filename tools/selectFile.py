# selectfiles.py
# Find target CREATE OR REPLACE PROCEDURE blocks and place them into files in the current folder
import sys
import os
import re

# write to output file
def selectFile(line, listed):
    found = False
    fout = None
    # find items and call writer
    for line in proceduredump:

        if ("CREATE OR REPLACE PROCEDURE" not in line) and not found:
            continue
        elif "CREATE OR REPLACE PROCEDURE" in line:
            for item in listed:
                stripped = item.strip()
                # If found, write to file
                if stripped in line:
                    fout = open(stripped.replace("CREATE OR REPLACE PROCEDURE ", "")+".sql", "wt")
                    listed.remove(item)
                    # Mark start of block
                    found = True
                    break
        if found: 
            fout.write(line)

        # Mark end of block
        if ("LANGUAGE plpgsql;" in line) and found:
            print("Modified " + os.path.basename(fout.name))
            fout.close()
            found = False

   

    return 0


# open dump file and target shortlist
proceduredump = open("pgsqlprocedurespg.sql", "rt")     # This is the AWS processed stored procedures dump
shortlist = open("procedurenames.txt", "rt")            # This is a formatted, wanted subset of procedure names. e.g. "CREATE OR REPLACE PROCEDURE dbo.procedurename"
listed = []
# put shortlist into a list type
for line in shortlist:
    listed.append(line)

selectFile(proceduredump, listed)


shortlist.close()
proceduredump.close()
