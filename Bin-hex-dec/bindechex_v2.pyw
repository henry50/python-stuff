from tkinter import *
import time
from tkinter import ttk
window = Tk()
window.title("Binary/Denary/Hex Converter")


def conv(opNo):
    resInpVal = fromInp.get()
    resType = cTo.get()
    
    if resType == "Binary":
        if opNo == 1:
            res = resInpVal
        elif opNo == 2:
            res = "{0:08b}".format(int(resInpVal))
        elif opNo == 3:
            ares = int(resInpVal, 16)
            res = "{0:08b}".format(ares)
                          
    elif resType == "Denary":
        if opNo == 1:
            res = int(resInpVal, 2)
        elif opNo == 2:
            res = resInpVal
        elif opNo == 3:
            res = int(resInpVal, 16)

    elif resType == "Hex":
        if opNo == 1:
            ares = int(resInpVal, 2)
            res = hex(int(ares))[2:]
        elif opNo == 2:
            res = hex(int(resInpVal))[2:]
        elif opNo == 3:
            res = resInpVal
    res = str(res).upper()
    toOutp.config(state = "normal")
    toOutp.delete(0, END)
    toOutp.insert(0, res)
    toOutp.config(state = "readonly")

def hideError():
    errMsg.pack_forget()

def showError():
    errMsg.pack()
    errMsg.config(text = "Invalid value")
    window.after(3000, hideError)
    
def calc():
    hideError()
    try:
        conFrom = cFrom.get()
        if conFrom == "Binary":
            conv(1)
        elif conFrom == "Denary":
            conv(2)
        elif conFrom == "Hex":
            conv(3)
    except:
        showError()

def cls():
    window.destroy()
    
title1 = Label(window, text="Binary/Denary/Hex Converter")
title1.pack(padx = 10, pady = 10)

fromToFrm = Frame(window)
fromToFrm.pack()

cLab1 = Label(fromToFrm, text="Convert")
cLab1.grid(column = 0, row = 0)

cFrom = ttk.Combobox(fromToFrm, values=["Binary","Denary","Hex"], width=7, state="readonly")
cFrom.set("Denary")
cFrom.grid(column=1, row=0)

cLab2 = Label(fromToFrm, text="to")
cLab2.grid(column=2, row=0)

cTo = ttk.Combobox(fromToFrm, values=["Binary","Denary","Hex"], width=7, state="readonly")
cTo.set("Binary")
cTo.grid(column=3, row=0)

inputsFrm = Frame(window)
inputsFrm.pack(pady = 10, padx = 10)

fromInp = Entry(inputsFrm)
fromInp.grid(column=0, row=0, padx = (0,10))

toOutp = Entry(inputsFrm, state = "readonly", readonlybackground = "white")
toOutp.grid(column = 1 , row = 0)

errMsg = Label(window, text = "", fg = "red")

btnFrm = Frame(window)
btnFrm.pack()

calc = Button(btnFrm, text="Convert", command=calc)
calc.grid(column=0,row=0, padx = (0,10), pady = (0,10))


cls = Button(btnFrm, text="Close", command=cls)
cls.grid(column=1, row=0, pady = (0,10))

window.mainloop()
