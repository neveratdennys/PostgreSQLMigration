# postgresProcess.py
import glob
import config
import modify
import ui
import replace

def main(name, act):
    #input file
    fin = open(name, "rt")
    #output file to write the result to
    fout = open(name[:-4]+"pg.sql", "wt")

    # for each line in the input file
    for line in fin:
        # Mark blocks to look at
        if "Severity CRITICAL" in line:
            config.action = True
            fout.write(line)
            continue
        elif config.action and ("*/" in line) and not act:
            config.action = False

        # Next line if line is None
        if (not line) or (not config.action):
            fout.write(line)
            continue

        # Standardize spacing first
        #line = modify.tabSpace(line)
        # Find and replace
        line = replace.replaceAll(line)
        # Modify functions and keywords
        line = modify.modifyAll(line)

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
    act = input("Only act on Severity CRITICAL? (y/n)\n")
    print(act)
    # act on all content or select content
    if act.lower() == "y":
       act = False
    else:
       act = True
       config.action = True

    # call main
    for name in ui.selectFile():
        main(name, act)
