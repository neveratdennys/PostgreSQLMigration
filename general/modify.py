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


# Modify node
    '''
    from[ \t] A.nodes('B') C(D)[;]?  =>
    with C(D) AS (values(
        A
    ))
    select d.*
    from C
        cross join XMLTABLE ( 'B'
            PASSING D
            COLUMNS
                nodedata text path '.') d
    '''
def convertNode(l):
    # Find the location of from .nodes
    count = l.lower().index('from')
    # Select the group before .node
    before = l[:count]

    # Find by search groups      A             B               C        D
    search = re.search(r"from\s(.+)\.nodes\('(.+)'\) (\w+\s)?(\w+.?)\((\w+)\)", l.lower())

    result = ""
    result = result + before + "WITH " + search.group(4) + "(" + search.group(5) + ") AS (values(\n"
    result = result + before + "\t" + search.group(1) + "))\n"
    result = result + before + "SELECT d.* -- old .nodes REPLACE * BY HAND\n"
    result = result + before + "FROM " + search.group(4) + "\n"
    result = result + before + "\tCROSS JOIN XMLTABLE ('" + search.group(2) + "'\n"
    result = result + before + "\t\tPASSING " + search.group(5) + "\n"
    result = result + before + "\t\tCOLUMNS\n"
    result = result + before + "\t\t\tnodedata TEXT path '.') d\n"
    return result

# Modify text search contains
'''
Contains(A, B) 
=> to_tsvector(A) @@ to_tsquery(B)
'''
def convertContains(l):
    # Find location of contains
    count = l.lower().index('contains(')
    before = l[:count]
        
    group=""
    n1=0
    n2=0
    A=""
    B=""
    # Look for A group before comma
    for n1, i in enumerate(l[count+9:], start=len(before)+9):
        # find current position in l
        checkIndex = checkWrap(l[count+9:][:n1-len(before)-9])
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
        
    # select the group after contains() call
    after = l[n2+1:]
    return before + " to_tsvector("+ A + ") @@ to_tsquery(" + B + ") " + after

# Add ON true if not already in line
def lateralJoin(l):

    # No need to change if already in line
    if ("on true" in l.lower()) or ("left outer" in l.lower()):
        return l

    if ("inner join" in l.lower()):
        # Find the location of from .nodes
        count = l.lower().index('inner')
        # Select the group before .node
        before = l[:count]

        search = re.search(r"(INNER JOIN LATERAL .+ \w+)(\(\w+\))?(.+)?", l)

    elif ("left join" in l.lower()):
        # Find the location of from .nodes
        count = l.lower().index('left')
        # Select the group before .node
        before = l[:count]

        search = re.search(r"(LEFT JOIN LATERAL .+ \w+)(\(\w+\))?(.+)?", l)

    # Escape if regex cannot find (e.g. multi line lateral join)
    if search is None or checkWrap(l[count:])>1:
        return l

    result = ""
    if search.group(2) is None and search.group(3) is None:
        result = before + search.group(1) + " ON true\n"
    elif search.group(2) is None:
        result = before + search.group(1) + " ON true" + search.group(3) + '\n'
    elif search.group(3) is None:
        result = before + search.group(1) + search.group(2) + " ON true\n"
    else:
        result = before + search.group(1) + search.group(2) + " ON true" + search.group(3) + '\n'

    #print(l+"result:"+result)
    return result
     


def modifyAll(l):
    # Replace convert(A, B) for B::A
    if ("convert(" in l.lower()):
        l = convertCast(l)
    # Replace charindex(A, B) for position(A in B)
    if ("charindex(" in l.lower()):
        l = convertCharindex(l)
    # Replace SET syntax for assigning values
    if ("set " in l.lower()):
        l = convertSet(l)
    # Help with .node conversion and add block
    if (".nodes(" in l.lower()) and ("from" in l.lower()):
        l = convertNode(l);
    # Replace contains(A, B) for to_tsvector(A) @@ to_tsquery(B)
    if ("contains(" in l.lower()):
        l = convertContains(l);
    # Add ON true for lateral joins
    if ("inner join lateral" in l.lower()) or ("left join lateral" in l.lower()):
        if len([n for n in range(len(l)) if l.lower().find('join lateral', n) == n]) == 1:
            l= lateralJoin(l);
    # Add dbo. schema name as well as standardize capitalization
    l = modifyLine(l)
    return l
