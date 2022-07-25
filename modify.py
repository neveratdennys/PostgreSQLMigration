# modify.py

import re
import config

# Standardize spacing
def tabSpace(l):
    # replace all non leading tabs with space
    while re.findall(r'(?<!\t)(?!^)\t+', l):
        l = re.sub(r'(?<!\t)(?!^)\t+', r' ', l)

    # remove duplicate spaces
    spaces = -((len(l) - len(l.lstrip(" "))) // -8)
    l = l.lstrip(" ")
    while spaces:
        spaces -= 1
        l = '\t' + l
    return l


# Helper: check for balanced brackets
def checkBracket(my_string):
    count = 0
    for c in my_string:
        if c == "(":
            count+=1
        elif c == ")":
            count-=1
    return count


# Modify the first convert in line
# Based on suggestions from stackoverflow.com/questions/73040953
def modifyConvert(l):
    # find the location of convert()
    count = l.index('convert(')

    # select the group before convert() call
    before = l[:count]

    group=""
    n1=0
    n2=0
    A=""
    B=""
    operate = False
    operators = ["|", "<", ">", "="]
    # look for A group before comma
    for n1, i in enumerate(l[count+8:], start=len(before)+8):
        # find current position in l
        checkIndex = checkBracket(l[count+8:][:n1-len(before)-8])
        if i == ',' and checkIndex == 0:
            A = group
            break
        group += i

    # look for B group after comma
    group = ""
    for n2, i in enumerate(l[n1+1:], start=n1+1):
        checkIndex = checkBracket(l[count+n1-len(before):][:n2-n1+1])
        if i == ',' and checkIndex == 0:
            return l
        elif checkIndex < 0:
            B = group
            break
        group += i
        
        # mark operators
        if i in operators:
            operate = True

    # select the group after convert() call
    after = l[n2+1:]

    # (B) if it contains operators
    if operate:
        return before + "(" + B.lstrip() + ') :: ' + A + after
    else:
        return before + B.lstrip() + '::' + A + after


# Modify cast syntax convert(a,b) to b::a. return line.
def convertCast(l):
    # Call helper for nested cases
    i = l.count('convert(')
    while i>0:
        i -= 1
        l = modifyConvert(l)

    return l


def modifyLine(l):
    # Add dbo. if line starts with FROM and add mark for next line
    matchFrom = ["from ", "FROM ", "From "]
    matchJoin = ["join ", "JOIN ", "Join "]
    matchWhere = ["where ", "WHERE ", "Where "]
    matchSelect = ["select ", "SELECT ", "Select "]
    matchWith = ["with ", "WITH ", "With "]
    # Mark WITH block to not add "dbo." and unmark it on ;
    if "WITH" in l:
        withMarker = False
    elif ";" in l:
        config.withMarker = True
        config.fromMarker = False
    x = next((x for x in matchFrom if x in l), False)
    y = next((y for y in matchJoin if y in l), False)
    z = next((z for z in matchWhere if z in l), False)
    s = next((s for s in matchSelect if s in l), False)
    # SELECT upper case
    if s:
        return(re.sub(re.escape(s), 'SELECT ', l))
    # FROM in line
    elif x:
        # mark FROM block regardless of FROM line
        config.fromMarker = True
        if (x+"(" not in l) and config.withMarker and ("dbo." not in l):
            #read replace the string and write to output file
            return(re.sub(re.escape(x), 'FROM ' + 'dbo.', l))
        else:
            return(re.sub(re.escape(x), 'FROM ', l))
    # FROM statement after FROM line
    elif config.fromMarker:
        # JOIN
        if y and (y+"(" not in l) and config.withMarker and ("dbo." not in l):
            return(re.sub(re.escape(y), 'JOIN ' + 'dbo.', l))
        elif y:
            return(re.sub(re.escape(y), 'JOIN ', l))
        # WHERE ending FROM statement
        elif z:
            config.fromMarker = False
            return(re.sub(re.escape(z), "WHERE ", l))
        else:
            return(l)
    else:
        return(l)



# Modify substring index syntax charindex(substring, string) to position(substring in string)
def convertCharindex(l):
    # Call helper for nested cases
    i = l.count('charindex(')
    while i>0:
        i -= 1
        l = modifyConvert(l)
    return l
