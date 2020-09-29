import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import os
from tkinter.filedialog import askopenfilename

def selectAll(widgt):
    widgt.selection_range(0, tk.END)

def runCmd(event):
    cmdVal = ent.get()
    if len(cmdVal.strip()) > 0:
        os.chdir(r"C:\\Windows\\System32")
        if cmdVal[0] == '"' and cmdVal[-1:] == '"':
            commd = 'start "" ' + cmdVal
        else:
            commd = 'start "" "' + cmdVal + '"'
        os.system(commd)
        selectAll(ent)
        
def closeCmd(event):
    root.destroy()

def browseCmd(event):
    openLocc = askopenfilename(initialdir = "C:\\Windows\\System32", title = "Browse", filetypes = (("Programs", "*.exe;*.pif;*.com;*.bat;*.cmd"),("All files","*.*")))
    openLoc = '"' + openLocc + '"'
    ent.delete(0, tk.END)
    ent.insert(0, openLoc)

    
root = tk.Tk()
root.title("Run")
root.config(bg = "white")
sheight = root.winfo_screenheight() - 250
geoStr = "400x170+0+" + str(sheight)
root.geometry(geoStr)
root.config(bg = "#f0f0f0")




mainFrm = tk.Frame(root, bg = "white")
mainFrm.pack()

rnphoto = tk.PhotoImage(file="run.gif")
icon = tk.Label(mainFrm, image=rnphoto, bg = "white")
icon.grid(column = 0, row = 0, sticky = "w", padx = 10, pady = (20,0))

runLab = tk.Label(mainFrm, text = "Type the name of a program, folder, document or Internet\nresource, and Windows will open it for you.", justify = "left", bg = "white")
runLab.grid(column = 1, row = 0, padx = (10,20), pady = (20,0))

entLab = tk.Label(mainFrm, text = "Open:", bg = "white")
entLab.grid(column = 0, row = 1, pady = 20, sticky = "e")

ent = ttk.Combobox(mainFrm, width = 50)
ent.grid(row = 1, column = 1, pady = 20, sticky = "w", padx = 10)

btnFrm = tk.Frame(root)
btnFrm.pack(anchor = "e")

runBtn = tk.Label(btnFrm, relief = "groove", text = "OK", width = 10)
runBtn.grid(row = 0, column = 0, ipady = 2, ipadx = 5, padx = (10,0), pady = 15)

canBtn = tk.Label(btnFrm, relief = "groove", text = "Cancel", width = 10)
canBtn.grid(row = 0, column = 1, ipady = 2, ipadx = 5, padx = 10)

brwBtn = tk.Label(btnFrm, relief = "groove", text = "Browse...", width = 10)
brwBtn.grid(row = 0, column = 2, ipady = 2, ipadx = 5, padx = (0,10))

ent.focus()

runBtn.bind("<Button-1>", runCmd)
root.bind("<Return>", runCmd)
canBtn.bind("<Button-1>", closeCmd)
brwBtn.bind("<Button-1>", browseCmd)

root.mainloop()
