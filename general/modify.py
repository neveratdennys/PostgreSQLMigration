# modify.py
import re
import config

# Helper: check for balanced wraps
def checkWrap(my_string):
    count = 0
    left = ["(", "[", "{"]
    right = [")", "]", "}"]
    apos = 0
    quote = 0
    for c in my_string:
        # handle brackets
        if c in left:
            count+=1
        elif c in right:
            count-=1

        # handle '
        if (c == "'") and (apos == 0):
            apos = 1
        elif (c == "'") and (apos == 1):
            apos = 0
        # handle "
        if (c == '"') and (quote == 0):
            quote = 1
        elif (c == '"') and (quote == 1):
            quote = 0

    return count + apos + quote


# Standardize spacing
def tabSpace(l):
    # replace all non leading tabs with space
    while re.findall(r'(?<!\t)(?!^)\t+', l):
        l = re.sub(r'(?<!\t)(?!^)\t+', r' ', l)

    # strip extra spaces and account for leading spaces
    spaces = -((len(l) - len(l.lstrip(" "))) // -4)
    l = l.lstrip(" ")
    while spaces:
        spaces -= 1
        l = '\t' + l
    return l


# Enforce uppercase keywords and add dbo. schema name
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
        return(re.sub(re.escape(x), 'FROM ', l))
        if (x+"(" not in l) and config.withMarker and ("dbo." not in l):
            #read replace the string and write to output file
            return(re.sub(re.escape(x), 'FROM ' + 'dbo.', l))
        else:
            return(re.sub(re.escape(x), 'FROM ', l))
    # FROM statement after FROM line
    elif config.fromMarker:
        # JOIN
        if y and (y+"(" not in l) and config.withMarker and ("dbo." not in l):
            return(re.sub(re.escape(y), 'JOIN ', l))
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


# Modify the first convert in line
# Based on suggestions from stackoverflow.com/questions/73040953
def modifyConvert(l):
    # find the location of convert()
    count = l.lower().index('convert(')
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
        checkIndex = checkWrap(l[count+8:][:n1-len(before)-8])
        if i == ',' and checkIndex == 0:
            A = group
            break
        group += i

    # look for B group after comma
    group = ""
    for n2, i in enumerate(l[n1+1:], start=n1+1):
        checkIndex = checkWrap(l[count+n1-len(before):][:n2-n1+1])
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
    i = l.lower().count('convert(')
    while i>0:
        i -= 1
        l = modifyConvert(l)
    return l


# Modify the first charindex in line
# Bug: some unknown instance can break this function
def modifyIndex(l):
    # Find the location of charindex()
    count = l.lower().index('charindex(')
    # Select the group before charindex() call
    before = l[:count]

    group=""
    n1=0
    n2=0
    A=""
    B=""
    # Look for A group before comma
    for n1, i in enumerate(l[count+10:], start=len(before)+10):
        # find current position in l
        checkIndex = checkWrap(l[count+10:][:n1-len(before)-10])
        if i == ',' and checkIndex == 0:
            A = group
            break
        group += i

    # Look for B group after comma
    group = ""
    for n2, i in enumerate(l[n1+1:], start=n1+1):
        checkIndex = checkWrap(l[count+n1-len(before):][:n2-n1+1])
        if i == ',' and checkIndex == 0:
            return l
        elif checkIndex < 0:
            B = group
            break
        group += i
        
    # select the group after charindex() call
    after = l[n2+1:]
    return before + " position("+ A + " in " + B + ") " + after


# Modify substring index syntax charindex(substring, string) to position(substring in string)
def convertCharindex(l):
    # Call helper for nested cases
    i = l.lower().count('charindex(')
    while i>0:
        i -= 1
        l = modifyIndex(l)
    return l

# From SET pram_var = x
def convertSet(l):
    return l


def modifyAll(l):
    # Replace convert(A, B) for B::A
    if ("convert(" in l.lower()):
        l = convertCast(l)
    # Replace charindex(A, B) for position(A in B)
    if ("charindex(" in l.lower()):
        l = convertCharindex(l)
    # Replace SET syntax for assigning values
    if("set " in l.lower()):
        l = convertSet(l)
    # Add dbo. schema name as well as standardize capitalization
    l = modifyLine(l)
    return l
