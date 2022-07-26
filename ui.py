# ui.py
import tkinter as tk
import tkinter.filedialog as fd

def selectFile():
    root = tk.Tk()
    filez = fd.askopenfilenames(parent=root, title='Choose a file')
    # check for sql extension
    for name in filez:
        if name[-4:] == ".sql":
            continue
        else:
            print("Wrong filename extension in "+name)
            return 0
    return filez
