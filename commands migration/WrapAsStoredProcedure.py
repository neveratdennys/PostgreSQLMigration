import sys
import os
import glob
import re
from itertools import groupby

if __name__ == '__main__':
    try:
        sys.argv = sys.argv[1:]
        path = ''
        if sys.argv:
            path = sys.argv[0]
        else:
            path = os.getcwd()

        listOfFiles = glob.glob(path + '/*.sql')

        for file in listOfFiles:
            with open(file, encoding="utf8", errors="ignore") as f:
                if len(sys.argv) >= 2:
                    basename = os.path.basename(file).rsplit('.')[0]
                    fileLines = f.readlines()
                    fileLines = [line for line in fileLines if not re.match('^\s*$', line, re.IGNORECASE)]
                    splitFileLines = [list(g) for k, g in groupby(fileLines, lambda x: not re.match('^\s*go\s*$', x, re.IGNORECASE)) if k]

                    returnFile = []
                    for idx, section in enumerate(splitFileLines):
                        startLines = []
                        startLines += ["IF EXISTS(SELECT 1 FROM sys.objects WHERE [type] = 'P' AND name = '_" + basename + "_" + str(idx) + "') DROP PROC [_" + basename + "_" + str(idx) + "]\n", 
                            "GO\n",
                            "CREATE procedure dbo.[_" + basename + "_" + str(idx) + "]\n", 
                            "as\n"]
                        returnFile += startLines + section + ["\nGO\n"]
                    
                    destFilename = path + '/converted/_' + basename + '.sql'
                    os.makedirs(os.path.dirname(destFilename), exist_ok=True)
                    with open(destFilename, "w", encoding="utf8", errors="ignore") as newf:
                        newf.writelines(returnFile)
                else:
                    basename = os.path.basename(file).rsplit('.')[0]
                    fileLines = f.readlines()
                    fileLines = [line for line in fileLines if not re.match('^\s*(go)?\s*$', line, re.IGNORECASE)]

                    startLines = []
                    startLines += ["IF EXISTS(SELECT 1 FROM sys.objects WHERE [type] = 'P' AND name = '_" + basename + "') DROP PROC [_" + basename + "]\n", 
                        "GO\n",
                        "CREATE procedure dbo.[_" + basename + "]\n", 
                        "as\n"]
                    fileLines = startLines + fileLines + ["\nGO\n"]
                    
                    destFilename = path + '/converted/_' + basename + '.sql'
                    os.makedirs(os.path.dirname(destFilename), exist_ok=True)
                    with open(destFilename, "w", encoding="utf8", errors="ignore") as newf:
                        newf.writelines(fileLines)
    except Exception as e:
        print(e)