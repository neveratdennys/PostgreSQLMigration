import sys
import pip
import glob
import re


# Check for balanced brackets
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
        return before + "(" + B.lstrip() + ') :: ' + A + " " + after
    else:
        return before + B.lstrip() + '::' + A + after


# Modify cast syntax with convert(a,b). return line.
def convertCast(l):

    # Call helper for nested cases
    i = l.count('convert(')
    while i>0:
        i -= 1
        l = modifyConvert(l)

    return l



#input file
fin = open("testviews.sql", "rt")
#output file to write the result to
fout = open("testout.sql", "wt")

# marker for from
fromMarker = 0

# for each line in the input file
for line in fin:

    # replace non leading tabs with space
    while re.findall(r'[A-Za-z0-9]\t', line):
        line = re.sub(r'([A-Za-z0-9])\t', r'\1 ', line)

    # remove duplicate spaces
    space = 1
    while '  ' in line:
        space += 1
        if space > 3:
            line = line.replace('  ', '\t')
            space = 1
        else:
            line = line.replace('  ', ' ')

    # Next line if line is None
    if not line:
        continue


    # Replace convert(A, B) for B::A
    if ("convert(" in line):
        line = convertCast(line)


    # Add dbo. if line starts with FROM and add mark for next line
    matchFrom = ["from ", "FROM ", "From "]
    matchJoin = ["join ", "JOIN ", "Join "]
    matchWhere = ["where ", "WHERE ", "Where "]
    x = next((x for x in matchFrom if x in line), False)
    y = next((y for y in matchJoin if y in line), False)
    z = next((z for z in matchWhere if z in line), False)
    if x:
        if x+"(" not in line:
            #read replace the string and write to output file
            fout.write(re.sub(re.escape(x), 'FROM ' + 'dbo.', line))
            fromMarker = True
        else:
            fout.write(re.sub(re.escape(x), 'FROM ', line))
    # Find the join statements and add dbo.
    elif fromMarker and y:
        if y+"(" not in line:
            fout.write(re.sub(re.escape(y), 'JOIN ' + 'dbo.', line))
        else:
            fout.write(re.sub(re.escape(y), 'JOIN ', line))
    # Find where statements and capitalize and reset marker
    elif fromMarker and z:
        fout.write(re.sub(re.escape(z), "WHERE ", line))
        fromMarker = False
    else:
        fout.write(line)

#close input and output files
fin.close()
fout.close()
