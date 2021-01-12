#################################################################
#   Timetable data file creator                                 #
#   Creates data files compatible with the timetable program    #
#   Version 1.0.0                                               #
#################################################################

import tkinter as tk, calendar, random, string, os
from datetime import datetime
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox
root = tk.Tk()
root.title("Timetable creator")
root.config(bg = "white")
root.state("zoomed")
#root.resizable(False,False)
timeData = """0,1,2,3,4,5,6,7,8,9,10
None,None,None,1,2,None,3,None,4,5,None
school ends,school starts,form,lesson 1,lesson 2,break,lesson 3,lunch,lesson 4,lesson 5,school ends
00:00,08:30,08:50,09:15,10:15,11:15,11:35,12:35,13:25,14:25,15:25
08:30,08:50,09:15,10:15,11:15,11:35,12:35,13:25,14:25,15:25,08:30
False,False,False,True,True,False,True,False,True,True,False
False,False,False,False,False,False,False,False,False,False,True
True,False,False,False,False,False,False,False,False,False,False"""
defaultVars = "False;#ADD8E6,#338DFF"
def newFile():
    menuFrame.pack_forget()
    centreFrame.pack_forget()
    e = editor()
def loadFile():
    menuFrame.pack_forget()
    loadPathFrame.pack()
    loadPathEnt.focus()
def loadFileBrowse():
    path = askopenfilename(defaultextension=".txt",filetypes = (("Text files","*.txt"),))
    if path:
        loadPathEnt.delete(0,"end")
        loadPathEnt.insert(0,path)
def load(path):
    loadPathFrame.pack_forget()
    with open(path, "r") as f:
        data = f.read()
        f.close()
    e = editor(data, path)
def validLoadPath():
    path = loadPathEnt.get()
    try:
        open(path,"r")
    except:
        tk.messagebox.showerror("Error","Invalid file path")
        loadPathEnt.delete(0,"end")
    else:
        load(path)
        
class editor():
    def __init__(self, data = None, path = None):
        self.frame = tk.Frame(root, bg = "white")
        self.frame.pack()
        self.saveBtn = tk.Button(self.frame, text = "Save timetable...", command = self.saveData, relief = "solid", bg = "white", font = (None,"16"))
        self.usedKeys = []
        self.overwritePath = None
        self.saveSelected = False
        if data and path:
            self.loadData(data)
            self.drawTable()
            self.insertData()
            self.overwritePath = path
        else:
            self.drawTable()
    def fmat(self, ldat):
        name, room, teacher = ldat
        if name in ["fr","dst"]:
            return [self.lessonDict[name]]
        else:
            return [self.lessonDict[name],room.upper(),self.teacherDict[teacher]]
    def unFmat(self, dat):
        if dat == "":
            return "None"
        elif dat in self.newTeachDict.values():
            return {v:k for k,v in self.newTeachDict.items()}[dat]
        elif dat in self.newLsnDict.values():
            return {v:k for k,v in self.newLsnDict.items()}[dat]
        else:
            return dat.lower()
        
    def genKey(self):
        key = "".join([random.choice(string.ascii_lowercase) for x in range(4)])
        if key not in self.usedKeys:
            self.usedKeys.append(key)
            return key
        else:
            self.genKey()
    def setSave(self, b):
        self.saveSelected = True
        self.saveOption = b
        self.saveAsTl.destroy()
        self.writeNew(self.saveasData)
    def getSaveAs(self):
        self.saveAsTl = tk.Toplevel()
        self.saveAsTl.config(bg = "white")
        saveLab = tk.Label(self.saveAsTl, font = (None,"24"), text = "Do you want to save as new or replace existing file?:", bg = "white")
        saveLab.grid(row = 0, column = 0, columnspan = 2, pady = (20,0), padx = 10)
        saveBtn1 = tk.Button(self.saveAsTl, text = "Save as new", font = (None,"16"), bg = "white", relief = "solid", command = lambda: self.setSave(True))
        saveBtn1.grid(row = 2, column = 0)
        saveBtn2 = tk.Button(self.saveAsTl, text = "Replace", font = (None,"16"), bg = "white", relief = "solid", command = lambda: self.setSave(False))
        saveBtn2.grid(row = 2, column = 1, padx = 10, pady = 10)
    def writeNew(self, newData):
        self.saveasData = newData
        if self.saveSelected or not self.overwritePath:
            if self.overwritePath:
                newPath = self.overwritePath
                if self.saveOption: #If save new
                    saveNew = True
                else:
                    saveNew = False
            else:
                saveNew = True
                newPath = "tabledata.txt"
            if os.path.isfile(newPath) and saveNew:
                base = "tabledata"
                num = 1
                while True:
                    altPath = base + str(num) + ".txt"
                    if os.path.isfile(altPath):
                        num += 1
                    else:
                        break
                if self.overwritePath:
                    baseDir = os.path.dirname(self.overwritePath)
                    newPath = os.path.join(baseDir, altPath)
                else:
                    newPath = altPath
            with open(newPath, "w") as f:
                f.write(newData)
                f.close()
            tk.messagebox.showinfo("Success","Timetable file successfully written")
        else:
            self.getSaveAs()
    def parseData(self,data, nl, nt):
        newTeach, newLsn = nt, nl
        self.newTeachDict = {self.genKey():x for x in newTeach}
        self.newLsnDict = {self.genKey():x for x in newLsn}
        fTeach = "\n".join(["{},{}".format(k,v) for k,v in self.newTeachDict.items()])
        fLsn = "\n".join(["{},{}".format(k,v) for k,v in self.newLsnDict.items()])
        fData = "\n".join(["\n".join(["\n".join([",".join([str(wn+1),str(dn),str(ln+1),",".join([self.unFmat(i) for i in l])]) for ln, l in enumerate(d)]) for dn, d in enumerate(w)]) for wn, w in enumerate(data)])
        newData = "/\n".join([fLsn,fTeach,fData,timeData,defaultVars])
        self.writeNew(newData)
    def loadData(self, data):
        rawData = [x.strip() for x in data.split("/")]
        try:
            lessonCode, teacherCode, tableCode = rawData[:3]
        except:
            tk.messagebox.showerror("Error","The selected file is not a timetable data file. The program will close now.")
            root.destroy()
            exit()
        else:
            self.lessonDict = {k:v for k,v in (x.split(",") for x in lessonCode.splitlines())}
            self.teacherDict = {k:v for k,v in (x.split(",") for x in teacherCode.splitlines())}
            self.tableData = [x.split(",") for x in tableCode.splitlines()]
            weekSplit = [[d[1:] for d in self.tableData if d[0] == str(w)] for w in range(1,3)]
            daySplit = [[[x[2:] for x in weekSplit[w] if x[0] == str(d)] for d in range(5)] for w in range(2)]
            self.textTable = [[[self.fmat(l) for l in d] for d in w] for w in daySplit]
    def insertData(self):
        for wn, week in enumerate(self.lessonBoxes):
            for dn, day in enumerate(week):
                for ln, lsn in enumerate(day):
                    for ni, i in enumerate(lsn.winfo_children()):
                        dayText = self.textTable[wn][dn][ln]
                        if dayText[0] in ["DST","Free"]:
                            if ni == 0:
                                i.insert(0,dayText[0])
                        else:
                            i.insert(0,dayText[ni])
    def saveData(self):
        newTextTable, newLsn, newTeach = [],[],[]
        if defaultVars.split(";")[0] == "False":
            self.getRefDate()
        else:
            for wn, week in enumerate(self.lessonBoxes):
                newTextTable.append([])
                for dn, day in enumerate(week):
                    newTextTable[wn].append([])
                    for ln, lsn in enumerate(day):
                        newTextTable[wn][dn].append([])
                        for ni, i in enumerate(lsn.winfo_children()):
                            cellValue = i.get()
                            if cellValue:
                                appendValue = cellValue
                            else:
                                appendValue = "None"
                            newTextTable[wn][dn][ln].append(appendValue)
                        newLsn.append(newTextTable[wn][dn][ln][0])
                        newTeach.append(newTextTable[wn][dn][ln][2])
            self.parseData(newTextTable, list(set(newLsn)), list(set(newTeach)))
    def setRefDate(self, num):
        global defaultVars
        rDate = datetime.strftime(datetime.now(),"%d.%m.%Y")
        rNo = str(num)
        rData = ",".join([rNo,rDate])
        sVars = defaultVars.split(";")
        sVars[0] = rData
        defaultVars = ";".join(sVars)
        self.refDateTl.destroy()
        self.saveData()
    def getRefDate(self):
        self.refDateTl = tk.Toplevel()
        self.refDateTl.config(bg = "white")
        refLab = tk.Label(self.refDateTl, font = (None,"24"), text = "Select current week number:", bg = "white")
        refLab.grid(row = 0, column = 0, columnspan = 2, pady = (20,0), padx = 10)
        refNote = tk.Label(self.refDateTl, text = "Note: If it is the weekend it is the week that just finished", bg = "white")
        refNote.grid(row = 1, column = 0, columnspan = 2, pady = (0,20))
        refBtn1 = tk.Button(self.refDateTl, text = "1", width = 5, font = (None,"16"), bg = "white", relief = "solid", command = lambda: self.setRefDate(1))
        refBtn1.grid(row = 2, column = 0)
        refBtn2 = tk.Button(self.refDateTl, text = "2", width = 5, font = (None,"16"), bg = "white", relief = "solid", command = lambda: self.setRefDate(2))
        refBtn2.grid(row = 2, column = 1, padx = 10, pady = 10)
    def drawTable(self):
        self.tableFrame = tk.Frame(self.frame, bg = "white")
        self.tableFrame.pack(side = "left")
        self.saveBtn.pack(side = "right", padx = 30)
        self.lessonBoxes = [[[[] for c in range(5)] for r in range(5)] for w in range(2)]
        wks = ["Week 1", "Week 2"]
        for w in range(2):
            weekHeader = tk.Label(self.tableFrame, text = wks[w], bg = "white")
            weekHeader.grid(row = w*7, column = 0, pady = 5, columnspan = 6)
            isTxt = False
            for row in range(6):
                for col in range(6):
                    if row == 0 and col == 0:
                        txt = ""
                        isTxt = True
                    elif row == 0:
                        txt = col
                        isTxt = True
                    elif col == 0:
                        txt = calendar.day_name[row-1] #row-1 to compensate for headers
                        isTxt = True
                    else:
                        r = row - 1 #To compensate for headers
                        c = col - 1
                        txt = ""
                        isTxt = False
                    if txt == "":
                        relf = "flat"
                    else:
                        relf = "solid"
                    if isTxt:
                        b = tk.Label(self.tableFrame, text= txt, bg = "white", relief = relf)
                        b.grid(row=row+1+(7*w), column=col, sticky = "nesw", ipadx = 3, ipady = 3)
                    else:
                        lessonEntry = tk.Frame(self.tableFrame, highlightbackground="black", highlightthickness=1)
                        lessonEntry.grid(row=row+1+(7*w), column=col, sticky = "nesw")
                        self.lessonBoxes[w][r][c] = lessonEntry
                        lsnEnt1 = tk.Entry(lessonEntry)
                        lsnEnt1.grid(row = 0, column = 0, sticky = "nesw")
                        lsnEnt2 = tk.Entry(lessonEntry)
                        lsnEnt2.grid(row = 1, column = 0, sticky = "nesw")
                        lsnEnt3 = tk.Entry(lessonEntry)
                        lsnEnt3.grid(row = 2, column = 0, sticky = "nesw")
                        self.tableFrame.grid_columnconfigure(col, weight=1, uniform="all")
centreFrame = tk.Frame(root, bg = "white")
centreFrame.place(relx = 0.5, rely = 0.5, anchor = "center")
menuFrame = tk.Frame(centreFrame, bg = "white")
menuFrame.pack()
menuTitle = tk.Label(menuFrame, bg = "white", text = "Timetable file creator", font = (None,"40"))
menuTitle.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 50)
menuNew = tk.Button(menuFrame, bg = "white", text = "New", relief = "solid", font = (None,"40"), command = newFile)
menuNew.grid(row = 1, column = 0, padx = 100, pady = 20)
menuLoad = tk.Button(menuFrame, bg = "white", text = "Load", relief = "solid", font = (None,"40"), command = loadFile)
menuLoad.grid(row = 1, column = 1, padx = 100, pady = 20)
#   Get path to load
loadPathFrame = tk.Frame(centreFrame, bg = "white")
loadPathLab = tk.Label(loadPathFrame, bg = "white", text = "Enter file path to load or browse:", font = (None,"32"))
loadPathLab.grid(row = 0, column = 0, columnspan = 2, pady = (0,50))
loadPathEnt = tk.Entry(loadPathFrame, width = 50, relief = "solid", font = (None,"20"))
loadPathEnt.grid(row = 1, column = 0, sticky = "nse", padx = 5)
loadPathBtn = tk.Button(loadPathFrame, bg = "white", text = "Browse...", command = loadFileBrowse, font = (None,"20"))
loadPathBtn.grid(row = 1, column = 1, sticky = "w", padx = 5)
loadPathEnd = tk.Button(loadPathFrame, bg = "white", text = "Load", relief = "solid", font = (None,"32"), command = validLoadPath)
loadPathEnd.grid(row = 2, column = 0, columnspan = 2, pady = 30)
