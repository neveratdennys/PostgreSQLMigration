# postgresProcess.py

import glob
import config
import modify
import ui
import replace

def main(name):
    #input file
    fin = open(name, "rt")
    #output file to write the result to
    fout = open(name[:-4]+"pg.sql", "wt")

    # for each line in the input file
    for line in fin:
        # Next line if line is None
        if not line:
            continue

        # Standardize spacing first
        line = modify.tabSpace(line)

        # Find and replace
        line = replace.replaceAll(line)

        # Replace convert(A, B) for B::A
        if ("convert(" in line.lower()):
            line = modify.convertCast(line)
        # Replace charindex(A, B) for position(A in B)
        if ("charindex(" in line.lower()):
            line = modify.convertCharindex(line)
        # Add dbo. schema name as well as standardize capitalization
        line = modify.modifyLine(line)

        # Write modified line in output file
        fout.write(line)

    #close input and output files
    print("Modified " + fout.name)
    fin.close()
    fout.close()


# Run main() for each sql script selected
if __name__ == "__main__":
    # global markers
    config.init()
    for name in ui.selectFile():
        main(name)
