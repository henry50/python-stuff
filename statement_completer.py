import tkinter as tk
from tkinter import ttk

class Statement(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Personal Statement Counter")
        self.titleLab = tk.Label(self, text = "Personal statement completion counter", font = ("Comic Sans MS", 16))
        self.titleLab.pack(padx = 10, pady = 5)
        self.textLab = tk.Label(self, text = "Paste personal statement here:")
        self.textLab.pack(pady = 10)
        self.valCmd = (self.register(self.setVal), "%P")
        self.mainText = tk.Text(self, height = 10, font = ("Comic Sans MS", 11))
        self.mainText.pack(fill = "x", padx = 10)
        self.mainText.bind_all("<Key>", self.setVal)
        self.mainText.bind_all("<<Paste>>", self.setVal)
        self.mainText.focus()
        self.div1 = tk.Frame(self, bg = "black", height = 2)
        self.div1.pack(fill = "x", pady = 10)
        self.charCount = tk.Label(self, text = "0 / 4000", font = ("Comic Sans MS", 24), fg = "red", bg = "white")
        self.charCount.pack(fill = "x")
        self.lineCount = tk.Label(self, text = "Character limit: 0% | Lines: 0", font = ("Comic Sans MS", 16))
        self.lineCount.pack(fill = "x")
        self.progBar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate", maximum = 4000)
        self.progBar.pack(pady = 10)
        self.resetBtn = tk.Button(self, text = "Clear all", command = self.reset, font = ("Comic Sans MS", 11))
        self.resetBtn.pack(pady = 5, ipadx = 16, ipady = 5)
    def reset(self):
        self.mainText.delete("1.0", "end")
        self.mainText.focus()
        self.charCount.config(text = "0 / 4000", fg = "red")
        self.lineCount.config(text = "Character limit: 0% | Lines: 0")
        self.progBar["value"] = 0
    def setVal(self, event):
        self.update_idletasks()
        newVal = len(self.mainText.get("1.0", "end-1c").replace("\n", ""))
        newLns = len(self.mainText.get("1.0", "end-1c").splitlines())
        self.lineCount.config(text = "Character limit: {}% | Lines: {}".format(int(newVal/4000*100), newLns))
        if newVal <= 4000:
            newFgRatio = (newVal/4000)
            rVal = int((1 - newFgRatio) * 255 * 2 if newFgRatio > 0.5 else 255)
            gVal = int(newFgRatio * 255 * 2 if newFgRatio < 0.5 else 255)
            newFgR = "{0:02x}".format(rVal)
            newFgG = "{0:02x}".format(gVal)
            newFg = "#" + newFgR + newFgG + "00"
        elif newVal == 4000:
            newFg = "#00FF00"
        else:
            newFg = "red"
        self.charCount.config(text = "{} / 4000".format(newVal), fg = newFg)
        self.progBar["value"] = newVal

app = Statement()
app.mainloop()
