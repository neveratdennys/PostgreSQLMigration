# config.py

def init():
    # keyword markers
    global fromMarker
    global withMarker
    fromMarker = False
    withMarker = False

    # dictionary for replace functions
    global replaceList
    replaceList = {
            "isnull(" : "coalesce(",
            "ISNULL(" : "coalesce(",
            "isnull (" : "coalesce(",
            "ISNULL (" : "coalesce(",
            #" + " : " || ",        #too many false positives
            '[' : '"',
            ']' : '"',
            " @" : " pram_",
            "nvarchar" : "varchar",
            "varchar(max)" : "varchar"
            }
