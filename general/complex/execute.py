# execute.py 
# Fix dynamic execution in Postgres
# 1. fix EXECUTE var_sql USING var1 var2 structure
# 2. when var_sql is being built, replace var1 var2 ... with $1 $2 ... 
import re
import time


# Replace given variable names only in the quoted sections
def replaceQuoted(num, varName, count, line):

    quoted = line.split("'")

    # Find quoted sections
    if (count % 2) != 0:
        for x in range(1, len(quoted), 2):
            quoted[x] = re.sub(r'@'+varName+r'([^\w\d])', "$"+str(num)+r'\1', quoted[x], flags=re.IGNORECASE)
            quoted[x] = re.sub(r'[vp]ar_'+varName+r'([^\w\d])', "$"+str(num)+r'\1', quoted[x], flags=re.IGNORECASE)
    else:
        for x in range(0, len(quoted), 2):
            quoted[x] = re.sub(r'@'+varName+r'([^\w\d])', "$"+str(num)+r'\1', quoted[x], flags=re.IGNORECASE)
            quoted[x] = re.sub(r'[vp]ar_'+varName+r'([^\w\d])', "$"+str(num)+r'\1', quoted[x], flags=re.IGNORECASE)


    return "'".join(quoted), len(quoted) - 1


# Use variable name, find the related strings and replace using varlist with corresponding $n
def replaceVar(name, varStr, l, sp):

    # remove spaces and split the variables into an array
    varlist = varStr.replace(' ', '').split(",")
    execsp = []
    marker = False
    count = 1

    for line in sp:

        # escape lines
        if (not line) or ("--" in line) or ("*" in line):
            execsp.append(line)
            continue
        
        # dynamic sql build detected, replacement begins (marked by firstword)
        if ((name + " :=") in line) or marker:

            # detect end of assignement
            if (re.search(";\s*$", line) is not None):
                marker = False
            else:
                marker = True

            # replace each var
            for i, x in enumerate(varlist):
                line, length = replaceQuoted(i+1, x, count, line)

            count = count + length
            execsp.append(line)
        
        else:
            firstword = []
            execsp.append(line)

    # execute line reached, replacement finished
    return execsp


def complexExecute(l, sp):

    # find execute and group accordingly
    search = re.search(r"EXECUTE (\w+) USING ([^;\n]+)(;?)", l)
    if search:
        search = search.groups()
        if search[1] is not None:
            varlist = re.sub(r'.ar_', '', str(search[1]))
            varlist = re.sub(r'@', '', varlist)
            # call loop function with useful groups
            sp = replaceVar(search[0], varlist, l, sp)
    return sp
