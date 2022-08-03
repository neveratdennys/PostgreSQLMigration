# config.py

def init():
    # keyword markers
    global fromMarker
    global withMarker
    global action
    fromMarker = False
    withMarker = False
    action = False

    # dictionary for replace functions
    global replaceList
    replaceList = {
            "set transaction isolation level" : "SET TRANSACTION",
            "isnull(" : "coalesce(",
            "ISNULL(" : "coalesce(",
            "isnull (" : "coalesce(",
            "ISNULL (" : "coalesce(",
            "' +" : "' ||",
            "+ '" : "|| '",
            '[' : '"',
            ']' : '"',
            " @" : " @ar_",        # par_ for parameter, var_ for variable 
            "(@" : "(@ar_",        # par_ for parameter, var_ for variable 
            "nvarchar" : "varchar", # psql replace with text
            "varchar(max)" : "varchar",
            # the below may be missing some senarios
            "char(13)" : "chr(13)",     
            "char(11)" : "chr(11)",
            "char(10)" : "chr(10)",
            "char(9)" : "chr(9)",
            "TOP (100) percent" : "",
            "with(nolock)" : "",    
            "with(noexpand)" : "",
            " len(" : " length("    
            #"TOP " : "LIMIT ",     # change place 
            #"top " : "limit "
            }
