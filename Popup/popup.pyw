###################################################################
#                                                                 #
#                           POPUP CREATOR                         #
#                             VERSION 2                           #
#                         Made by Henry Lunn                      #
#                                                                 #
###################################################################

import tkinter as tk
from tkinter.constants import *
import tkinter.messagebox
import tkinter.colorchooser
from tkinter.scrolledtext import ScrolledText
from tkinter import font
from tkinter import ttk

###################################################################

def verifyInput():
    verifTitle = titlEnt.get()
    verifText = entTxt.get("1.0", "end-1c")
    verifFont = fontCbb.get()
    verifSize = sizeEnt.get()
    verifFg = fontDetails[2]
    verifBg = fontDetails[3]
    #Int test
    try:
        int(verifSize)
    except:
        tk.messagebox.showerror("Invalid font", "Invalid font size")
        return False
    else:
        if infoLab.cget("text") != "Version 2.0\nMade by Henry Lunn":
            errormsg = "Error 0x0F59D4B069AC\nSomebody changed the version information...\nProbably you" + infoLab.cget("text").split("by",1)[1].title() + " :D"
            tk.messagebox.showerror("Error",errormsg)
            return False
        else:
            #Values given
            if len(verifTitle.strip()) == 0:
                retTitle = "Popup"
            else:
                retTitle = verifTitle
                
            if len(verifText.strip()) == 0:
                tk.messagebox.showerror("No text", "Enter some text for the popup")
                return False
            else:
                retText = verifText
            #Check font
            if verifFont not in font.families():
                tk.messagebox.showerror("Invalid font", "Invalid font")
                return False
            else:
                retFont = verifFont
            if int(verifSize) > 500:
                tk.messagebox.showerror("Large font", "Choose a size less than 500")
                return False
            else:
                retSize = verifSize
            retFg = verifFg
            retBg = verifBg
            
            pupVals = [retTitle, retText, retFont, retSize, retFg, retBg]
            return pupVals

def createPopup():
    verif = verifyInput()
    if verif != False:
        global pup
        if verif[4] != "Default" and verif[5] != "Default":
            pup = tk.Toplevel()
            pup.title(verif[0])
            pup.config(bg = verif[5])
            tk.Label(pup, text=verif[1], font = (verif[2], str(verif[3])), wraplength = 1000, fg = verif[4], bg = verif[5]).pack(padx=10,pady=10)
        elif verif[4] == "Default" and verif[5] != "Default":
            pup = tk.Toplevel()
            pup.title(verif[0])
            pup.config(bg = verif[5])
            tk.Label(pup, text=verif[1], font = (verif[2], str(verif[3])), wraplength = 1000, bg = verif[5]).pack(padx=10,pady=10)
        elif verif[5] == "Default" and verif[4] != "Default":
            pup = tk.Toplevel()
            pup.title(verif[0])
            tk.Label(pup, text=verif[1], font = (verif[2], str(verif[3])), wraplength = 1000, fg = verif[4]).pack(padx=10,pady=10)
        else:
            pup = tk.Toplevel()
            pup.title(verif[0])
            tk.Label(pup, text=verif[1], font = (verif[2], str(verif[3])), wraplength = 1000).pack(padx=10,pady=10)
    elif verif == False:
        False
    else:
        tk.messagebox.showerror("Error","Error displaying popup")

def spamPopup():
    for i in range(20):
        createPopup()
        
def chooseColour(typ):
    if typ == "fg":
        colChoice = tk.colorchooser.askcolor()
        fontDetails[2] = colChoice[1]
        sampleText("fg")
    elif typ == "bg":
        colChoice = tk.colorchooser.askcolor()
        fontDetails[3] = colChoice[1]
        sampleText("bg")

def selectAllEnt(event):
    sizeEnt.selection_range(0, END)

def selectAllCbb(event):
    fontCbb.selection_range(0, END)

def sampleText(typ):
    if typ == "size":
        fsize = sizeEnt.get()
        try:
            int(fsize)
        except:
            False
        else:
            if len(fsize) == 0:
                fontPrev.config(font = (None, 20))
                sizeEnt.delete(0, END)
                sizeEnt.insert(0, 20)
                fontDetails[1] = "20"
            elif int(fsize) > 100:
                fontDetails[1] = "100"
            else:
                ffont = fontCbb.get()
                fontPrev.config(font = (ffont, int(fsize)))
                fontDetails[0] = ffont
                fontDetails[1] = fsize
    elif typ == "font":
        fsize = sizeEnt.get()
        try:
            int(fsize)
        except:
            ffont = fontCbb.get()
            fontPrev.config(font = (ffont, 20))
            sizeEnt.delete(0, END)
            sizeEnt.insert(0, 20)
            fontDetails[1] = "20"
        else:
            if int(fsize) > 100:
                ffont = fontCbb.get()
                fontPrev.config(font = (ffont, 100))
                fontDetails[0] = ffont
                fontDetails[1] = fsize
            else:
                ffont = fontCbb.get()
                fontPrev.config(font = (ffont, int(fsize)))
                fontDetails[0] = ffont
                fontDetails[1] = fsize
    elif typ == "fg":
        fontPrev.config(fg = fontDetails[2])
        fgSamp.config(bg = fontDetails[2])
    elif typ == "bg":
        fontPrev.config(bg = fontDetails[3])
        bgSamp.config(bg = fontDetails[3])

###################################################################

root = tk.Tk()
root.title("Popup creator")
root.resizable(False, False)
##############[0 - Font     ,1-Size, 2 - Fg  , 3 - Bg   ]
fontDetails = ["Courier New", "20", "Default", "Default"]

###################################################################

mainFrm = tk.Frame(root)
mainFrm.pack(anchor = "w")

titl = tk.Label(mainFrm, text = "Create a popup", font = (None,"24"))
titl.pack(pady = (10,0))

infoLab = tk.Label(mainFrm, text = "Version 2.0\nMade by Henry Lunn")
infoLab.pack()

titlLab = tk.Label(mainFrm, text = "Enter title")
titlLab.pack(pady = (10,0), padx = 10, anchor = "w")

titlEnt = tk.Entry(mainFrm, width = 40)
titlEnt.pack(padx = 10, anchor = "w", pady = (0,10))

entLab = tk.Label(mainFrm, text = "Enter text:")
entLab.pack(padx = 10, anchor = "w")

entTxt = ScrolledText(mainFrm, height =7, width = 50)
entTxt.pack(padx = 10)
entTxt.config(font = titlEnt.cget("font"))

###################################################################

settingFrm = tk.Frame(root)
settingFrm.pack(anchor = "w", padx = 10, pady = 10)

fontLab = tk.Label(settingFrm, text = "Font:")
fontLab.grid(row = 0, column = 0, sticky = "w", pady = 10)

fontCbb  = ttk.Combobox(settingFrm, values=font.families())
fontCbb.set("Courier New")
fontCbb.grid(row = 0, column = 1, sticky = "w", padx = 10, columnspan = 2)

sizeLab = tk.Label(settingFrm, text = "Font size:")
sizeLab.grid(row = 1, column = 0, sticky = "w")

sizeEnt = tk.Entry(settingFrm, width = 10)
sizeEnt.grid(row = 1, column = 1, sticky = "w", padx = 10, columnspan = 2)
sizeEnt.insert(END, 20)

fgLab = tk.Label(settingFrm, text = "Text colour:")
fgLab.grid(row = 2, column = 0, sticky = "w", pady = 10)

fgSamp = tk.Frame(settingFrm, height = 20, width = 20, bg = "black", borderwidth = 1, relief = "solid")
fgSamp.grid(row = 2, column = 1)

fgBtn = tk.Button(settingFrm, text = "Choose...", command = lambda: chooseColour("fg"))
fgBtn.grid(row = 2, column = 2, sticky = "w")

bgLab = tk.Label(settingFrm, text = "Background colour:")
bgLab.grid(row = 3, column = 0, sticky = "w", pady = 10)

bgSamp = tk.Frame(settingFrm, height = 20, width = 20, borderwidth = 1, relief = "solid")
bgSamp.grid(row = 3, column = 1)

bgBtn = tk.Button(settingFrm, text = "Choose...", command = lambda: chooseColour("bg"))
bgBtn.grid(row = 3, column = 2, sticky = "w")

###################################################################

fprevFrm = tk.Frame(root)
fprevFrm.pack(anchor = "w", padx = 10)

fprevLab = tk.Label(fprevFrm, text = "Preview:")
fprevLab.pack(anchor = "w")

fontPrev = tk.Label(fprevFrm, text = "Sample text", font = ("Courier New", "20"))
fontPrev.pack()

###################################################################

buttonFrm = tk.Frame(root)
buttonFrm.pack(pady = 10, fill = "x")

crtBtn = tk.Button(buttonFrm, text = "Create", command = createPopup)
crtBtn.pack(padx = 10, anchor = "w")

spamBtn = tk.Button(buttonFrm, text = "Spam", command = spamPopup)
spamBtn.pack(padx = 10, anchor = "w")

###################################################################

sizeEnt.bind("<FocusIn>", selectAllEnt)
sizeEnt.bind("<KeyRelease>", lambda event: sampleText("size"))
sizeEnt.bind("<FocusOut>", lambda event: sampleText("size"))
fontCbb.bind("<<ComboboxSelected>>", lambda event: sampleText("font"))
fontCbb.bind("<Return>", lambda event: sampleText("font"))
fontCbb.bind("<FocusOut>", lambda event: sampleText("font"))
fontCbb.bind("<FocusIn>", selectAllCbb)

###################################################################

root.mainloop()

###################################################################
