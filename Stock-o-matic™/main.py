import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.scrolledtext
from datetime import datetime
"""
CHANGELOG:
Version 1.0 - Original program, displayed data in ttk Treeview
Version 2.0 - Created custom data table class (stockTable)
Version 2.1 - Added editing
Version 2.2 - Added deletion
Version 2.3 - Added record addition
Version 3.0 - Fixed problems with database IDs (there were quite a few)
Version 3.1 - Added new UI with separate sections
Version 3.2 - Added database changelog, change checker
Version 3.3 - Added scrollable data table
Version 3.3.1 - Added constants for file name and table name and added version info
Version 3.3.2 - Fixed probelem where creating new row and committing multiple times made lots of new rows
"""
DATA_FILE = "stock.db"
TABLE_NAME = "example"
VERSION = "3.3.2"
class stockTable(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.row = 0
        self.highestId = 1
        self.editIcon = tk.PhotoImage(file = "edit_icon_16x16.png")
        self.delIcon = tk.PhotoImage(file = "delete_icon_16x16.png")
        self.rows = {}
        self.edits = {}
        self.deletes = {}
        self.editStatus = {}
        self.deletedRows = []
        self.addedRows = {}
        self.editedRows = {}
        self.changeMade = False
    def insert(self, values = [], header = False, edit = False, num = False, delete = False, added = False):
        r = []
        if not header:
            rowId = values[0]
            if rowId > self.highestId:
                self.highestId = rowId
        else:
            rowId = "head"
        for n, i in enumerate(values):
            if header:
                bg = "lightgrey"
            else:
                bg = "white"
            f = tk.Frame(self, highlightthickness = 1, highlightbackground = "black", bg = bg)
            f.grid(row = self.row, column = n, sticky = "nesw")
            self.grid_columnconfigure(n, weight = 1)
            l = tk.Entry(f, bg = bg, relief = "flat", disabledbackground = bg, disabledforeground = "black")
            l.insert("end", i)
            l.config(state = "disabled")
            if num and num == n:
                l.config(validate = "key", validatecommand = (l.register(self.checkInput), "%P", "%d"))
            l.pack(padx = 3, pady = 3, fill = "both", expand = True)
            r.append([f,l])
        if edit:
            editFrm = tk.Frame(self, highlightthickness = 1, highlightbackground = "black", bg = bg)
            editFrm.grid(row = self.row, column = n+1, sticky = "nesw")
            editIco = tk.Label(editFrm, image = self.editIcon, bg = bg)
            editIco.pack(expand = True, fill = "both")
            editIco.bind("<Button-1>", lambda event, a = rowId: self.toggleEdit(a))
            editFrm.bind("<Button-1>", lambda event, a = rowId: self.toggleEdit(a))
            self.edits[rowId] = [editFrm, editIco]
            self.editStatus[rowId] = False
        if delete:
            delFrm = tk.Frame(self, highlightthickness = 1, highlightbackground = "black", bg = bg)
            colNo = n+2 if edit else n+1
            delFrm.grid(row = self.row, column = colNo, sticky = "nesw")
            delIco = tk.Label(delFrm, image = self.delIcon, bg = bg)
            delIco.pack(expand = True, fill = "both")
            delIco.bind("<Button-1>", lambda event, a = rowId: self.confirmDelete(a))
            delFrm.bind("<Button-1>", lambda event, a = rowId: self.confirmDelete(a))
            self.deletes[rowId] = [delFrm, delIco]
        if added:
            self.addedRows[rowId] = values
        self.rows[rowId] = r
        self.row += 1
    def checkInput(self, text, event):
        if event == "1":
            if not text.isdigit():
                return False
            else:
                return True
    def debug(self, printTkRows = False):
        if printTkRows:
            print(self.rows)
    def get(self):
        result = []
        for i, x in self.rows.items():
            if i != "head":
                result.append([i, x[1][1].get(), int(x[2][1].get())])
        return result
    def resetData(self):
        self.deletedRows = []
        self.addedRows = {}
        self.editedRows = {}
    def confirmDelete(self, row):
        if tk.messagebox.askokcancel("Delete?","Are you sure you want to delete row with id {}?".format(row)):
            for x in self.rows[row]:
                for y in x:
                    y.destroy()
            for x in self.edits[row]:
                x.destroy()
            for x in self.deletes[row]:
                x.destroy()
            del self.rows[row]
            del self.edits[row]
            del self.deletes[row]
            self.deletedRows.append(row)
    def toggleEdit(self, row):
        if self.editStatus[row]:
            newState = "disabled"
            newBg = "white"
            newStatus = False
            self.editedRows[row] = [x[1].get() for x in self.rows[row]]
        else:
            newState = "normal"
            newBg = "lightgrey"
            newStatus = True
        for x in self.rows[row][1:]:
            x[0].config(bg = newBg)
            x[1].config(state = newState, bg = newBg)
        for x in self.edits[row]:
            x.config(bg = newBg)
        self.rows[row][2][1].focus()
        self.editStatus[row] = newStatus
        
class stockManage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Stock-o-matic™")
        self.state("zoomed")
        self.resizable(False,False)
        self.mainFrm = tk.Frame(self)
        self.mainFrm.pack(fill = "both", expand = True)
        self.titleFrm = tk.Frame(self.mainFrm)
        self.titleFrm.grid(row = 0, column = 0, columnspan = 3, pady = 5)
        self.titleLab = tk.Label(self.titleFrm, text = "Stock-o-matic™", font = (None, 24))
        self.titleLab.pack()
        self.titleVer = tk.Label(self.titleFrm, text = "Version {}".format(VERSION), font = (None, 16))
        self.titleVer.pack()
        self.div1 = tk.Frame(self.mainFrm, bg = "black", height = 2)
        self.div1.grid(row = 1, column = 0, columnspan = 3, sticky = "ew")
        self.loadDatabase()
        self.loadUI()
        self.initChecker()
        #self.dataTable.debug(printTkRows = True)
    def loadDatabase(self):
        conn = sqlite3.connect(DATA_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM {}".format(TABLE_NAME))
        self.data = c.fetchall()
        conn.close()
    def canvasConfig(self, event):
        self.update_idletasks()
        self.dataCnv.config(scrollregion = self.dataCnv.bbox("all"))
        self.dataCnv.itemconfig(self.dataFrmWin, width = self.dataCnv.winfo_width())
    def canvasScroll(self, event):
        self.dataCnv.yview_scroll(int(-1*(event.delta/120)), "units")
    def loadUI(self):
        self.dataWrap = tk.Frame(self.mainFrm)
        self.dataWrap.grid(row = 2, column = 0, sticky = "nesw")
        self.dataCnv = tk.Canvas(self.dataWrap, highlightthickness = 0)
        self.dataCnv.pack(side = "left", expand = True, fill = "both")
        self.dataFrmWrap = tk.Frame(self.dataCnv, bg = "red")
        self.dataFrmWrap.bind("<Configure>", self.canvasConfig)
        self.dataFrmWin = self.dataCnv.create_window((0,0), window= self.dataFrmWrap, anchor = "nw")
        self.dataScr = tk.Scrollbar(self.dataWrap, orient = "vertical", command = self.dataCnv.yview)
        self.dataScr.pack(side = "right", fill = "y")
        self.dataCnv.configure(yscrollcommand = self.dataScr.set)
        self.bind("<MouseWheel>", self.canvasScroll)
        self.canvasConfig(event = None)
        self.dataFrm = tk.Frame(self.dataFrmWrap)
        self.dataFrm.pack(fill = "both", expand = True)
        self.div2 = tk.Frame(self.mainFrm, bg = "black", width = 2)
        self.div2.grid(row = 2, column = 1, sticky = "ns")
        self.mainFrm.grid_columnconfigure(0, weight = 100)
        self.mainFrm.grid_columnconfigure(1, weight = 0)
        self.mainFrm.grid_columnconfigure(2, weight = 100)
        self.mainFrm.grid_rowconfigure(0, weight = 1)
        self.mainFrm.grid_rowconfigure(1, weight = 0)
        self.mainFrm.grid_rowconfigure(2, weight = 100)
        self.dataTitle = tk.Label(self.dataFrm, text = "Data from '{}' table '{}':".format(DATA_FILE, TABLE_NAME), font = (None, 18))
        self.dataTitle.pack(pady = 10)
        self.dataTable = stockTable(self.dataFrm)
        self.dataTable.pack(padx = 20, fill = "y", side = "left")
        self.dataTable.insert(("ID","Item", "Quantity"), header = True)
        for i in self.data:
            self.dataTable.insert(i, edit = True, num = 2, delete = True)
        self.rightFrm = tk.Frame(self.mainFrm)
        self.rightFrm.grid(row = 2, column = 2, sticky = "nesw")
        self.addWrap = tk.Frame(self.rightFrm)
        self.addWrap.pack(fill = "both", pady = 5)
        self.addFrm = tk.Frame(self.addWrap)
        self.addFrm.pack()
        self.addLab = tk.Label(self.addFrm, text = "Add record:", font = (None, 16))
        self.addLab.grid(row = 0, column = 0, columnspan = 2, pady = 10)
        self.addEnt1Frm = tk.Frame(self.addFrm, highlightthickness = 1, highlightbackground = "black", bg = "white")
        self.addEnt1Frm.grid(row = 1, column = 0, sticky = "nesw")
        self.addEnt1 = tk.Entry(self.addEnt1Frm, relief = "flat")
        self.addEnt1.focus()
        self.addEnt1.pack(padx = 3, pady = 3)
        self.addEnt2Frm = tk.Frame(self.addFrm, highlightthickness = 1, highlightbackground = "black", bg = "white")
        self.addEnt2Frm.grid(row = 1, column = 1, sticky = "nesw")
        self.addEnt2 = tk.Entry(self.addEnt2Frm, relief = "flat")
        self.addEnt2.config(validate = "key", validatecommand = (self.addEnt2.register(self.dataTable.checkInput), "%P", "%d"))
        self.addEnt2.pack(padx = 3, pady = 3)
        self.addFrm3 = tk.Frame(self.addFrm, highlightthickness = 1, highlightbackground = "black", bg = "white")
        self.addFrm3.grid(row = 1, column = 2, sticky = "nesw")
        self.addImg1 = tk.PhotoImage(file = "add_icon_16x16.png")
        self.addLab1 = tk.Label(self.addFrm3, image = self.addImg1, bg = "white")
        self.addLab1.pack(fill = "both", expand = True)
        self.addFrm4 = tk.Frame(self.addFrm, highlightthickness = 1, highlightbackground = "black", bg = "white")
        self.addFrm4.grid(row = 1, column = 3, sticky = "nesw")
        self.addImg2 = tk.PhotoImage(file = "delete_icon_16x16.png")
        self.addLab2 = tk.Label(self.addFrm4, image = self.addImg2, bg = "white")
        self.addLab2.pack(fill = "both", expand = True)
        self.addFrm3.bind("<Button-1>", self.addRecord)
        self.addLab1.bind("<Button-1>", self.addRecord)
        self.addFrm4.bind("<Button-1>", self.clearInputs)
        self.addLab2.bind("<Button-1>", self.clearInputs)
        self.div3 = tk.Frame(self.rightFrm, height = 2, bg = "black")
        self.div3.pack(fill = "x", pady = 10)
        self.saveChangesTxt = tk.scrolledtext.ScrolledText(self.rightFrm, state = "disabled")
        self.saveChangesTxt.pack(padx = 5)
        self.saveChanges = tk.Button(self.rightFrm, text = "Commit changes", command = self.updateDatabase, bg = "white", relief = "solid", font = (None, 24))
        self.saveChanges.pack(pady = 10)
    def clearInputs(self, event = None):
        self.addEnt1.delete(0, "end")
        self.addEnt2.delete(0, "end")
        self.addEnt2.delete(0, "end")
        self.addEnt1.focus()
    def addRecord(self, event):
        self.dataTable.insert([self.dataTable.highestId + 1, self.addEnt1.get(), self.addEnt2.get()], edit = True, delete = True, num = 2, added = True)
        self.clearInputs()
    def initChecker(self):
        self.prevRemoved = list(self.dataTable.deletedRows)
        self.prevNew = list(self.dataTable.addedRows.values())
        self.prevEdit = list(self.dataTable.editedRows.keys())
        self.modifyText("Stock-o-matic™ version {} database changes log:".format(VERSION))
        self.modifyText("{} - Database loaded".format(datetime.strftime(datetime.now(), "%H:%M:%S")))
        self.changeChecker()
    def modifyText(self, text):
        self.saveChangesTxt.config(state = "normal")
        self.saveChangesTxt.insert("end", text + "\n")
        self.saveChangesTxt.config(state = "disabled")
    def changeChecker(self):
        self.newRemoved = [x for x in self.dataTable.deletedRows if x not in self.prevRemoved]
        self.newNew = [x for x in self.dataTable.addedRows.values() if x not in self.prevNew]
        self.newEdit = [x for x in self.dataTable.editedRows.keys() if x not in self.prevEdit]
        timestamp = datetime.strftime(datetime.now(), "%H:%M:%S")
        if self.newRemoved:
            for x in self.newRemoved:
                self.modifyText("{} - Removed row with ID {}".format(timestamp,x))
                self.prevRemoved.append(x)
        if self.newNew:
            for x in self.newNew:
                self.modifyText("{} - Created new row, item: '{}', quantity: '{}'".format(timestamp, x[1],x[2]))
                self.prevNew.append(x)
        if self.newEdit:
            for x in self.newEdit:
                self.modifyText("{} - Edited row with ID {}".format(timestamp, x))
                self.prevEdit.append(x)
        self.after(100, self.changeChecker)
        
    def updateDatabase(self):
        try:
            conn = sqlite3.connect(DATA_FILE)
            c = conn.cursor()
            removedIds = self.dataTable.deletedRows
            newIds = self.dataTable.addedRows
            changes = self.dataTable.editedRows
            if newIds: #Data added:
                for x in newIds.values():
                    c.execute("INSERT INTO {} (item, quantity) VALUES ('{}', {})".format(TABLE_NAME, x[1], int(x[2])))
            if changes:
                for n, x in changes.items():
                    c.execute("UPDATE {} SET item = '{}', quantity = {} WHERE id = {}".format(TABLE_NAME, x[1],x[2],n))
            if removedIds: #Data removed
                for x in removedIds:
                    c.execute("DELETE FROM {} WHERE id = {}".format(TABLE_NAME, x))
            
            conn.commit()
            conn.close()
        except Exception as e:
            self.modifyText("{} - An error occured: {}".format(datetime.strftime(datetime.now(), "%H:%M:%S"), e))
        else:
            self.modifyText("{} - Changes committed successfully".format(datetime.strftime(datetime.now(), "%H:%M:%S")))
            self.dataTable.resetData()
app = stockManage()
app.mainloop()
