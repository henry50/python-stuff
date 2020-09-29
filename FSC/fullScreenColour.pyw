import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.messagebox import askyesno
import random

bgr = ["#f0f0ed"]
randCols = [False]

def maxmin(event):
    setupFrmFrm.pack(expand = True)
    root.attributes("-fullscreen",False)
    root.state("zoomed")
    randCols[0] = False
    root.config(bg = "#f0f0ed", cursor = "arrow")

def randomColour():
    hexVals = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    hexCol = ["#"]
    for i in range(6):
        randIndx = random.randint(0,15)
        hexCol.append(hexVals[randIndx])
    returnStr = "".join(hexCol)
    return returnStr

def getColour():
    bgac = askcolor()
    bgr[0] = bgac[1]
    setupColLab.config(bg = bgr[0])

def randFScrn():
    randCols[0] = True
    setupFrmFrm.pack_forget()
    root.config(bg = randomColour(), cursor = "none")
    root.attributes("-fullscreen", True)
    changeBgColour()

def goFScrn():
    setupFrmFrm.pack_forget()
    root.config(bg = bgr[0], cursor = "none")
    root.attributes("-fullscreen", True)

def changeBgColour():
    if randCols[0]:
        fgcl = randomColour()
        root.config(bg = fgcl)
        root.after(1000, changeBgColour)

def changeBtnCol():
    fgcl = randomColour()
    setupCChange.config(fg = fgcl)
    root.after(500, changeBtnCol)  

randKeys = [0, True]
def helpMe(event):
    if randKeys[1] == True:
        randKeys[0] += 1
        if randKeys[0] % 10 == 0:
            if askyesno("Help","Do you want to exit?"):
                maxmin("a")
                randKeys[1] = True
            else:
                randKeys[1] = False

root = tk.Tk()
root.title("Full screen colour")
root.state("zoomed")
root.bind("<Escape>", maxmin)
root.bind("<Key>", helpMe)

setupFrmFrm = tk.Frame(root)
setupFrmFrm.pack(expand = True)
setupFrm = tk.Frame(setupFrmFrm, borderwidth = 3, relief = "solid")
setupFrm.pack(ipadx = 20, ipady = 20)
setupLab = tk.Label(setupFrm, text = "Select a colour:", font = ("TkDefaultFont", "30"))
setupLab.pack(pady = 10)
setupColour = tk.Button(setupFrm, text = "Select...", command = getColour, padx = 15, pady = 5)
setupColour.pack()
setupColLab = tk.Frame(setupFrm, height = 40, width = 40, borderwidth = 1, relief = "solid")
setupColLab.pack(pady = 20)
setupInfo = tk.Label(setupFrm, text = "Press ESC to exit fullscreen", fg = "red", font = ("TkDefaltFont", "16"))
setupInfo.pack()
setupConfirm = tk.Button(setupFrm, text = "Fullscreen", command = goFScrn, padx = 15, pady = 5)
setupConfirm.pack(pady = (10,0))
setupCChange = tk.Button(setupFrm, text = "Random colours", command = randFScrn, padx = 10, pady = 4)
setupCChange.pack(pady = (10,0))
changeBtnCol()
root.mainloop()
