# postgresProcess.py
import glob
import config
import modify
import ui
import replace
import complex.execute as execute

def main(name, act):
    #input file
    fin = open(name, "rt")
    #output file to write the result to
    fout = open(name[:-4]+"pg.sql", "wt")
    sp = []

    # for each line in the input file
    for line in fin:
        # Mark blocks to look at
        if "Severity CRITICAL" in line:
            config.action = True
            sp.append(line)
            continue
        elif config.action and ("*/" in line) and not act:
            config.action = False

        # Skip if None or no CRITICAL marked or commented
        if (not line) or (not config.action) or ("--" in line) or ("\*" in line) or ("/*" in line):
            sp.append(line)
            continue

        # Standardize spacing first
        #line = modify.tabSpace(line)
        # Find and replace
        line = replace.replaceAll(line)
        # Modify functions and keywords
        line = modify.modifyAll(line)
        
        # Complex modification
        if ("execute " in line.lower()):
            sp = execute.complexExecute(line, sp)
            sp.append(line)
            fout.write("".join(sp))
            sp = []
            continue


        # Mark and record each stored procedure
        if "LANGUAGE " in line:
            # write previous sp to output
            sp.append(line)
            fout.write("".join(sp))

            #sp stores each stored procedure up to current position
            sp = []
        else:
            sp.append(line)


    #close input and output files
    print("Modified " + fout.name)
    fin.close()
    fout.close()


# Run main() for each sql script selected
if __name__ == "__main__":
    # global markers
    config.init()
    act = input("Only act on Severity CRITICAL? (y/n)\n")
    # act on all content or select content
    if act.lower() == "y":
       act = False
    else:
       act = True
       config.action = True

    # call main
    for name in ui.selectFile():
        main(name, act)
