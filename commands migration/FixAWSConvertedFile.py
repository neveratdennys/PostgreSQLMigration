import sys
import os
import re
from itertools import groupby

def fixBoolean(st, variable):
    st = str.replace(st, variable + ' = 0', variable + ' = false')
    st = str.replace(st, variable + ' = 1', variable + ' = true')
    return st

def replaceText(st):
    st = str.replace(st, "aws_sqlserver_ext.tomsbit('0')", 'false')
    st = str.replace(st, "aws_sqlserver_ext.tomsbit('')", 'false')
    st = str.replace(st, "aws_sqlserver_ext.tomsbit('1')", 'true')
    st = str.replace(st, "aws_sqlserver_ext.tomsbit('False')", 'false')
    st = str.replace(st, "aws_sqlserver_ext.SYS_OBJECTS", 'sys_objects')
    st = str.replace(st, "aws_sqlserver_ext.object_id", 'object_id')
    st = str.replace(st, '$BODY$', '$$')
    st = str.replace(st, 'mainapp_dbo', 'dbo')
    st = str.replace(st, 'maincyber_dbo', 'dbo')
    st = str.replace(st, 'v140cyber_dbo', 'dbo')
    st = fixBoolean(st, 'issystem')
    st = fixBoolean(st, 'ishidden')
    st = fixBoolean(st, 'iscommandline')
    st = fixBoolean(st, 'istask')
    st = fixBoolean(st, 'istransformer')
    st = fixBoolean(st, 'iscondition')
    st = fixBoolean(st, 'isfilter')
    st = fixBoolean(st, 'skipinputvalidation')
    st = fixBoolean(st, 'enablebatchexecution')
    st = fixBoolean(st, 'enableskip')
    st = fixBoolean(st, 'issystemruntime')
    st = fixBoolean(st, 'isprovisioned')
    st = fixBoolean(st, 'ispython')
    st = fixBoolean(st, 'isrequired')
    st = fixBoolean(st, 'isintegration')
    st = fixBoolean(st, 'iscustom')
    st = fixBoolean(st, 'fetchincidents')
    st = fixBoolean(st, 'fetchevents')
    st = fixBoolean(st, 'checkurlreputation')
    st = fixBoolean(st, 'checkipreputation')
    st = fixBoolean(st, 'checkfilehashreputation')
    st = fixBoolean(st, 'enablerunonagent')
    st = fixBoolean(st, 'preventcontainerexecution')
    st = fixBoolean(st, 'hiddeninconnector')
    st = fixBoolean(st, 'allowinputvalue')
    st = str.replace(st, 'CALL dbo.sppb_generatecommandmodel', 'PERFORM dbo.fnsp_sppb_generatecommandmodel')
    st = str.replace(st, 'CALL dbo.sppb_config_updatecommandhash', 'PERFORM dbo.fnsp_sppb_config_updatecommandhash')
    st = str.replace(st, 'CALL dbo.sppb_updateeventfield', 'PERFORM dbo.fnsp_sppb_updateeventfield')
    st = str.replace(st, 'OldParamName', 'ParamName')
    st = str.replace(st, 'pa$$w0rd', 'pa\$\$w0rd')
    return st

if __name__ == '__main__':
    try:
        sys.argv = sys.argv[1:]
        path = ''
        if sys.argv:
            path = sys.argv[0]
        else:
            path = os.getcwd()

        # file = path + '/awsconverted/plpg_converted_utility.sql'
        # file = path + '/awsconverted/convertedfilter.sql'
        file = path + '/awsconverted/convertedintegration.sql'

        with open(file, encoding="utf8", errors="ignore") as f:
            fileLines = f.readlines()
            fileLines = list(map(replaceText, fileLines))
            
            splitFileLines = [['DO\n'] + list(g) for k, g in groupby(fileLines, lambda x: 'create procedure' not in x.lower() and x.lower().replace(" ", "") != 'as\n') if k]
            storedProcedureList = [list(g) for k, g in groupby(fileLines, lambda x: 'create procedure' in x.lower()) if k]
            storedProcedureName = [re.search('dbo."?_(.+?)(_[0-9]+)?"?\(.*\)', x[0]).groups() for x in storedProcedureList]

            returnFile = []
            # returnFile += splitFileLines[0]
            for procedure, oriName in zip(splitFileLines[1:], storedProcedureName):
                with open(path + '/convertedIntegration/_' + oriName[0] + '.sql', encoding="utf8", errors="ignore") as orif:
                    oriFileLines = orif.readlines()

                    if oriName[1]:
                        splitOriFileLines = [list(g) for _, g in groupby(oriFileLines, lambda x: 'create procedure' not in x.lower())]
                        procedureIndex = [i for i, x in enumerate(splitOriFileLines) if re.match('create procedure.*_' + oriName[0] + oriName[1], x[0], re.IGNORECASE)]
                        oriFileLines = splitOriFileLines[procedureIndex[0]+1]
                        
                    mergeIndices = [i for i, x in enumerate(procedure) if 'on conflict' in x.lower()]
                    oriMergeIndices = [i for i, x in enumerate(oriFileLines) if re.match('\s*merge\s', x, re.IGNORECASE)]

                    startPattern = 'using\s*\(\s*values\s*\('
                    endPattern = '\)\s*\)\s*$'
                    endPattern2 = '\)\s*\)\s*as src'
                    for mergeIndex, oriMergeIndex in zip(mergeIndices, oriMergeIndices):
                        valueIndex = oriMergeIndex+1

                        oriFileLines[valueIndex] = re.search(startPattern + '(.*)', oriFileLines[valueIndex], re.IGNORECASE).group(1)
                        mergeValue = ''
                        matchEnd = re.search(endPattern, oriFileLines[valueIndex], re.IGNORECASE) is None or re.search('^(\s*as src|\s*--)', oriFileLines[valueIndex+1], re.IGNORECASE) is None
                        matchEnd2 = re.search(endPattern2, oriFileLines[valueIndex], re.IGNORECASE) is None
                        while matchEnd and matchEnd2:
                            mergeValue += oriFileLines[valueIndex]
                            valueIndex += 1
                            matchEnd = re.search(endPattern, oriFileLines[valueIndex], re.IGNORECASE) is None or re.search('^(\s*as src|\s*--)', oriFileLines[valueIndex+1], re.IGNORECASE) is None
                            matchEnd2 = re.search(endPattern2, oriFileLines[valueIndex], re.IGNORECASE) is None
                            
                        mergeValue += re.search('(.*)' + '\)\s*\)\s*(?:$|as src)', oriFileLines[valueIndex], re.IGNORECASE).group(1)
                        
                        mergeValue = str.replace(mergeValue, '@', 'var_')
                        mergeValue = str.replace(mergeValue, '\\', '\\\\')

                        # mergeValue = re.sub('((?:^|,)\s*)([0-9]+)(\s*(?=,|$))', r'\1' + "'" + r'\2' + "'" + r'\3', mergeValue)

                        procedure[mergeIndex-1] = re.sub('(.*?values\s*\().*(\)\)*\s*$)', r'\1' + mergeValue + r'\2', procedure[mergeIndex-1], flags = re.IGNORECASE)
                        procedure[mergeIndex] = str.replace(procedure[mergeIndex], "var_", "")

                        if re.search('from\s*\(\s*values', procedure[mergeIndex-1], re.IGNORECASE) is not None:
                            procedure[mergeIndex-1] = re.sub('from\s*\((.*)', r'\1', procedure[mergeIndex-1], flags = re.IGNORECASE)
                            procedure[mergeIndex-3] = ''
                            procedure[mergeIndex-2] = ''

                    srcIndices = [i for i, x in enumerate(procedure) if 'as src' in x.lower() and '/*' not in x.lower()]
                    for srcIndex in srcIndices:
                        n = srcIndex
                        while (re.search('from\s*\(\s*values', procedure[n], re.IGNORECASE) is None):
                            n -= 1
                        procedure[n] = re.sub('from\s*\((.*)', r'\1', procedure[n], flags = re.IGNORECASE)
                        procedure[n-2] = ''
                        procedure[n-1] = ''

                        procedure[srcIndex] = re.sub('(.*)\)\s*as src\s*\(.*\)\)', r'\1', procedure[srcIndex], flags = re.IGNORECASE)

                    procedure = [x for x in procedure if x != '']
                    returnFile += procedure
                destFilename = path + '/integration/' + oriName[0] + '.sql'
                os.makedirs(os.path.dirname(destFilename), exist_ok=True)
                with open(destFilename, 'a+', encoding="utf8", errors="ignore") as newf:
                    newf.writelines(procedure)
            destFilename = path + '/awsconverted/convertedFixedIntegration.sql'
            with open(destFilename, 'w', encoding="utf8", errors="ignore") as newf:
                newf.writelines(returnFile)
    except Exception as e:
        print(e)