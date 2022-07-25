# replace.py
import re
import config

def replaceAll(l):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, config.replaceList.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: config.replaceList[mo.group()], l) 
