# execute.py 
# Fix dynamic execution in Postgres
# 1. fix EXECUTE var_sql USING var1 var2 structure
# 2. when var_sql is being built, replace var1 var2 ... with $1 $2 ... 
import re

# Use variable name, find the related strings and replace using varlist with corresponding $n
def replaceVar(name, varStr, l, sp):

    # remove spaces and split the variables into an array
    varlist = varStr.replace(' ', '').split(",")
    execsp = []
    marker = False

    for line in sp:

        # escape lines
        if (not line) or ("--" in line) or ("*" in line):
            execsp.append(line)
            continue
        
        # dynamic sql build detected, replacement begins (marked by firstword)
        if ((name + " :=") in line) or marker:

            # detect end of assignement
            if (";" in line):
                marker = False
            else:
                marker = True


            # replacement
            for i, x in enumerate(varlist):

                # detect edge cases and skip them
                if (re.search(r"(\'.+||.+)"+x+r"(.+||)?(.+\')?", line) is not None):
                    continue

                line = re.sub(r"(\'.+)\@"+x+r"(.+\')", r"\1$"+str(i+1)+r"\2", line)
                line = re.sub(r"(\'.+).ar_"+x+r"(.+\')", r"\1$"+str(i+1)+r"\2", line)

            execsp.append(line)
        
        else:
            firstword = []
            execsp.append(line)

    # execute line reached, replacement finished
    return sp
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
