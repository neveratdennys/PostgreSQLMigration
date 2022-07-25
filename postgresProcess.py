# postgresProcess.py

import glob
import config
import modify

def main():

    #input file
    fin = open("testviews.sql", "rt")
    #output file to write the result to
    fout = open("testout.sql", "wt")

    # global markers
    config.init()

    # for each line in the input file
    for line in fin:

        # Next line if line is None
        if not line:
            continue

        # Standardize spacing first
        line = modify.tabSpace(line)

        # Replace convert(A, B) for B::A
        if ("convert(" in line):
            line = modify.convertCast(line)

        # Add dbo. schema name as well as standardize capitalization
        line = modify.modifyLine(line)


        # Write modified line in output file
        fout.write(line)

    #close input and output files
    fin.close()
    fout.close()

# Run main()
if __name__ == "__main__":
    main()
