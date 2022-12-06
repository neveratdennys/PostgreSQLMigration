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
            "isnull(" : "coalesce(",
            "ISNULL(" : "coalesce(",
            "isnull (" : "coalesce(",
            "ISNULL (" : "coalesce(",
            "OUTER APPLY" : "LEFT JOIN LATERAL",
            "outer apply" : "LEFT JOIN LATERAL",
            "CROSS APPLY" : "INNER JOIN LATERAL",
            "cross apply" : "INNER JOIN LATERAL",
            "' +" : "' +",
            "+ '" : "+ '",
#            '[' : '"',              # may replace more than it should
#            ']' : '"',
#            " @" : " var_",        # par_ for parameter, var_ for variable 
#            "(@" : "(var_",        # par_ for parameter, var_ for variable 
            "nvarchar(max)" : "TEXT",
            "nvarchar(max)" : "TEXT",
            "NVARCHAR (max)" : "TEXT",
            "NVARCHAR (max)" : "TEXT",
            "nvarchar " : "VARCHAR ", 
            "NVARCHAR " : "VARCHAR ", 
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
