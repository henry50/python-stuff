import sqlite3
import tkinter as tk
from tkinter import ttk
#Create example table
#c.execute("CREATE TABLE example (id integer PRIMARY KEY, item text NOT NULL, quantity integer NOT NULL)")
##fill with sample data
##stockList = [["table",34],
##             ["chair",29],
##             ["A4 lined book",563],
##             ["A4 Paper x500",403],
##             ["K toner",5],
##             ["Y toner", 6],
##             ["M toner", 2],
##             ["C toner", 8],
##             ["Staples x1000", 56]]
##for x in stockList:
##    sql = 'INSERT INTO example (item,quantity) VALUES ("{}", {})'.format(*x)
##    #print(sql)
##    c.execute(sql)
##conn.commit()
class stockManage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)
        self.title("Stock-o-matic™")
        self.mainFrm = tk.Frame(self)
        self.mainFrm.pack(fill = "both", expand = True)
        self.titleLab = tk.Label(self.mainFrm, text = "Data from 'example' table:", font = (None, 24))
        self.titleLab.pack()
        self.loadDatabase()
    def loadDatabase(self):
        conn = sqlite3.connect("stock.db")
        c = conn.cursor()
        c.execute("SELECT * FROM example")
        self.data = c.fetchall()
        self.dataFrm = tk.Frame(self.mainFrm)
        self.dataFrm.pack()
        self.dataTree = ttk.Treeview(self.dataFrm, columns = ("Item", "Quantity"), show = "headings")
        self.dataTree.heading("#0", text = "null")
        self.dataTree.heading("#1", text = "Item")
        self.dataTree.heading("#2", text = "Quantity")
        self.dataTree.column("#1", stretch=tk.YES)
        self.dataTree.column("#2", stretch=tk.YES)
        self.dataTree.pack()
        for i in self.data:
            self.dataTree.insert(parent = "", index = "end", text = "null", values = i[1:])

app = stockManage()
app.mainloop()
