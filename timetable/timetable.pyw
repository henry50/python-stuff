import tkinter.messagebox, tkinter.colorchooser, calendar
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import ctypes
appid = "timetable.app"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
VER_NO = "1.2.0"
"""
Version history:
1.0.0 - Initial timetable program
1.1.0 - Redesign with classes
1.2.0 - Addition of file creator and compatibility with it

"""


class timetable():
    def __init__(self, filePath):
        try:
            self.path = filePath
            self.testDelta = False
            # self.testDelta = True
            self.testDeltaHrs = 18
            self.colourPresets = {
                "Default": ["#ADD8E6", "#338DFF"],
                "Christmas": ["#3C8D0D", "#D42426"],
                "Springwood": ["#684398", "#25AE61"],
                "No highlight": ["#FFFFFF", "#FFFFFF"]}
            self.loadData()
            self.calculateWeek()
            self.createTimes()
            self.formatTable()
            self.displayTable()
        except Exception as e:
            if tk.messagebox.showerror("Error",
                                       "An error has occured: {}. Please make sure the timetable file is valid".format(
                                               e)):
                root.destroy()

        else:
            pass

    def loadData(self):
        try:
            open(self.path, "r")
        except:
            tk.messagebox.showerror("File not found", "Timetable file not found. It is required.")
        else:
            with open(self.path, "r") as f:
                rawData = [x.strip() for x in f.read().split("/")]
                f.close()
            self.rawData = rawData
            lessonCode, teacherCode, tableCode, timeCode, dataVars = rawData
            self.lessonDict = {k: v for k, v in (x.split(",") for x in lessonCode.splitlines())}
            self.teacherDict = {k: v for k, v in (x.split(",") for x in teacherCode.splitlines())}
            self.tableData = [x.split(",") for x in tableCode.splitlines()]
            timedata = [x.split(",") for x in timeCode.splitlines()]
            self.timeData = [[timedata[y][x] for y in range(len(timedata))] for x in
                             range(len(timedata[0]))]  # Swaps rows and columns
            self.dataVars = dataVars.split(";")
            self.weekData, self.colours = self.dataVars
            self.colours = self.colours.split(",")

    def calculateWeek(self):
        if self.testDelta:
            now = datetime.now() + timedelta(hours=self.testDeltaHrs)
        else:
            now = datetime.now()
        referenceWeek, referenceDateStr = self.weekData.split(",")
        try:
            referenceWeek = int(referenceWeek)
        except:
            tkinter.messagebox.showerror("Error", "Invalid reference week")
        else:
            referenceDate = datetime.date(datetime.strptime(referenceDateStr, "%d.%m.%Y"))
            currentDay = datetime.date(now)
            mon1 = (referenceDate - timedelta(days=referenceDate.weekday()))
            mon2 = (currentDay - timedelta(days=currentDay.weekday()))
            weekDifference = int(((mon2 - mon1).days / 7) % 2)
            if weekDifference == 0:
                self.currentWeekNumber = referenceWeek
            else:
                if referenceWeek == 2:
                    self.currentWeekNumber = 1
                else:
                    self.currentWeekNumber = 2

    def createTimes(self):
        self.lessonTimes = [lessonTime(*x + [self.testDelta, self.testDeltaHrs]) for x in self.timeData]

    def fmat(self, ldat):
        name, room, teacher = ldat
        if self.lessonDict[name] in ["Free", "DST"]:
            return self.lessonDict[name]
        else:
            return "{}\n{}\n{}".format(self.lessonDict[name], room.upper(), self.teacherDict[teacher])

    def formatTable(self):
        weekSplit = [[d[1:] for d in self.tableData if d[0] == str(w)] for w in range(1, 3)]
        daySplit = [[[x[2:] for x in weekSplit[w] if x[0] == str(d)] for d in range(5)] for w in range(2)]
        self.textTable = [[[self.fmat(l) for l in d] for d in w] for w in daySplit]

    def displayTable(self):
        self.boxWidgets = []
        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(side="left", fill="both", padx=20)
        wks = ["Week 1", "Week 2"]
        for w in range(2):
            self.boxWidgets.append([])
            weekHeader = tk.Label(self.frame, text=wks[w], bg="white")
            weekHeader.grid(row=w * 7, column=0, pady=5, columnspan=6)
            for row in range(6):
                self.boxWidgets[w].append([])
                for col in range(6):
                    if row == 0 and col == 0:
                        txt = ""
                    elif row == 0:
                        txt = col
                    elif col == 0:
                        txt = calendar.day_name[row - 1]  # row-1 to compensate for headers
                    else:
                        r = row - 1  # To compensate for headers
                        c = col - 1
                        txt = self.textTable[w][r][c]
                    if txt == "":
                        relf = "flat"
                    else:
                        relf = "solid"
                    b = tk.Label(self.frame, text=txt, bg="white", relief=relf)
                    self.boxWidgets[w][row].append(b)
                    b.grid(row=row + 1 + (7 * w), column=col, sticky="nesw", ipadx=3, ipady=3)
                    self.frame.grid_columnconfigure(col, weight=1, uniform="all")

    def updateTime(self):
        if self.testDelta:
            now = datetime.now() + timedelta(hours=self.testDeltaHrs)
        else:
            now = datetime.now()
        currentLesson = self.calculateLesson()
        nextLesson = self.lessonTimes[currentLesson.getNext()]
        day = datetime.weekday(now)
        # Display date/time
        if 4 <= now.day <= 20 or 24 <= now.day <= 30:
            sup = "th"
        else:
            sup = ["st", "nd", "rd"][now.day % 10 - 1]
        dateLab.config(text="{}, {}{} {} {}".format(now.strftime("%A"), now.day, sup, now.strftime("%B"), now.year))
        timeLab.config(text=now.strftime("%H:%M:%S"))
        if day not in [5, 6]:  # Not a weekend
            # Colourise
            for lnum, lsn in enumerate(
                    self.boxWidgets[self.currentWeekNumber - 1][day + 1]):  # Text boxes of current day
                lsn.config(bg=self.colours[0])  # Colours all boxes
                if currentLesson.isLesson and currentLesson.num == lnum:  # If it is the current lesson
                    lsn.config(bg=self.colours[1])  # Colours current lesson
            # Current lesson
            lessonText = self.getText(currentLesson, False, True, day)
            lsnLab.config(text=lessonText)
            addText = self.getText(nextLesson, True, True, day)
            if currentLesson.isLesson and len(addText) != 1:
                addLab.config(text="in {} with {}".format(*addText[1:]))
            else:
                addLab.config(text="")
            remText = self.getTime(currentLesson.getEnd() - now) + " until " + self.getText(nextLesson, False, False,
                                                                                            day)
            remLab.config(text=remText)
        else:
            lsnLab.config(text="Weekend")
            addLab.config(text="")
            remText = "School starts in " + self.getTime(
                datetime.combine((now + timedelta(days=((0 - day + 7) % 7))).date(),
                                 (self.lessonTimes[1].getStart()).time()) - now)
            remLab.config(text=remText)
        root.after(100, self.updateTime)

    def calculateLesson(self):
        if self.testDelta:
            now = datetime.now() + timedelta(hours=self.testDeltaHrs)
        else:
            now = datetime.now()
        current = [x for x in self.lessonTimes if x.getStart() <= now and x.getEnd() > now][0]
        return current

    def getTime(self, time):
        ts = time.total_seconds()
        h = int(ts // 3600)
        m = int((ts % 3600) // 60) + 1
        if h == 1:
            hs = ""
        else:
            hs = "s"
        if m == 1:
            ms = ""
        else:
            ms = "s"
        if h >= 1:
            if m == 60:
                return "{} hour{}".format(h + 1, hs)
            else:
                return "{} hour{} {} minute{}".format(h, hs, m, ms)
        else:
            return "{} minute{}".format(m, ms)

    def getText(self, lsn, returnAll, isNow, day):
        if lsn.isLesson:
            a = self.textTable[self.currentWeekNumber - 1][day][lsn.num - 1].split("\n")
            a[0] = a[0][0].upper() + a[0][1:]
            if returnAll:
                return a
            else:
                return a[0]
        else:
            if isNow:
                if returnAll:
                    return [lsn.present.title()]
                else:
                    return lsn.present.title()
            else:
                if returnAll:
                    return [lsn.present.title()]
                else:
                    return lsn.name

    def changeDataVars(self, index, value):
        try:
            self.rawData[-1].split(";")[index]
        except IndexError:
            tk.messagebox.showerror("IndexError", "IndexError in changeDataVars call: That is not a valid data index")
        else:
            dataLoc = self.rawData[-1].split(";")
            dataLoc[index] = value
            self.rawData[-1] = ";".join(dataLoc)
            newData = "/\n".join(self.rawData)
            with open(self.path, "w") as f:
                f.write(newData)
                f.close()
        self.loadData()

    def changeColours(self):
        # tk.messagebox.showinfo("Y E S", "(っ◔◡◔)っ ♥ colour ♥")
        self.top = tk.Toplevel(root)
        mainTitle = tk.Label(self.top, text="Select colours:", font=(None, "24"))
        mainTitle.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        title1 = tk.Label(self.top, text="Current day:")
        title1.grid(row=1, column=0)
        self.select1 = tk.Frame(self.top, bg=self.colours[0], highlightbackground="black", highlightthickness=2,
                                width=30, height=30)
        self.select1.grid(row=2, column=0, padx=10)
        self.select1.bind("<Button-1>", lambda event: self.colChange(0))
        title2 = tk.Label(self.top, text="Current lesson:")
        title2.grid(row=1, column=1)
        self.select2 = tk.Frame(self.top, bg=self.colours[1], highlightbackground="black", highlightthickness=2,
                                width=30, height=30)
        self.select2.grid(row=2, column=1, pady=10)
        self.select2.bind("<Button-1>", lambda event: self.colChange(1))
        title3 = tk.Label(self.top, text="Or use a preset:")
        title3.grid(row=3, column=0, columnspan=2, padx=10)
        self.select3 = ttk.Combobox(self.top, state="readonly", values=list(self.colourPresets.keys()))
        if self.colours in self.colourPresets.values():
            self.select3.set([k for k, v in self.colourPresets.items() if v == self.colours][0])
        else:
            self.select3.set("Custom")
        self.select3.bind('<<ComboboxSelected>>', lambda event: self.colChange(2))
        self.select3.grid(row=4, column=0, columnspan=2, pady=5)
        close = tk.Button(self.top, text="Close", command=lambda: self.top.destroy())
        close.grid(row=5, column=0, columnspan=2, sticky="ne", pady=5, padx=5)

    def colChange(self, option):
        if option == 2:
            getVal = self.select3.get()
            self.colours = self.colourPresets[getVal]
            self.select1.config(bg=self.colours[0])
            self.select2.config(bg=self.colours[1])
        else:
            newCol = tk.colorchooser.askcolor()[1]
            if newCol:
                self.colours[option] = newCol
                [self.select1, self.select2][option].config(bg=newCol)
                self.select3.set("Custom")
        if option == 2 or newCol:
            self.changeDataVars(1, ",".join(self.colours))
        self.top.lift()

    def weekSet(self):
        if self.currentWeekNumber == 1:
            newWeek = 2
        else:
            newWeek = 1
        change = tk.messagebox.askyesno("Change week", "Should it be week {}?".format(newWeek))
        if change:
            tk.messagebox.showinfo("Change week", "Week change will take effect when restarted")
            newText = ",".join([str(newWeek), datetime.now().strftime("%d.%m.%Y")])
            self.changeDataVars(0, newText)

    def getNew(self):
        return askopenfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"),))


class lessonTime():
    def __init__(self, *args):
        self.pos, self.num, self.name, self.start, self.end, self.isLesson, self.endTomorrow, self.startYesterday, self.tdelta, self.tdeltah = args
        self.pos, self.num, self.isLesson, self.endTomorrow = int(self.pos), self.tryNum(self.num), self.toBool(
            self.isLesson), self.toBool(self.endTomorrow)
        if "ends" in self.name:
            self.present = self.name.replace("ends", "ended")
        elif "starts" in self.name:
            self.present = self.name.replace("starts", "started")
        else:
            self.present = self.name

    def toBool(self, s):
        if s == "True":
            return True
        else:
            return False

    def tryNum(self, i):
        if i == "None":
            return i
        else:
            return int(i)

    def getStart(self):
        if self.tdelta:
            now = datetime.now() + timedelta(hours=self.tdeltah)
        else:
            now = datetime.now()
        if self.startYesterday:
            return datetime.combine(now + timedelta(days=-1), datetime.strptime(self.start, "%H:%M").time())
        else:
            return datetime.combine(now, datetime.strptime(self.start, "%H:%M").time())

    def getEnd(self):
        if self.tdelta:
            now = datetime.now() + timedelta(hours=self.tdeltah)
        else:
            now = datetime.now()
        if self.endTomorrow:
            return datetime.combine(now + timedelta(days=1), datetime.strptime(self.end, "%H:%M").time())
        else:
            return datetime.combine(now, datetime.strptime(self.end, "%H:%M").time())

    def getNext(self):
        if self.pos == 10:
            return 0
        else:
            return self.pos + 1


def newTable():
    global table
    newPath = table.getNew()
    table.frame.destroy()
    table.__init__(newPath)


def about():
    aboutTl = tk.Toplevel(root)
    aboutTl.title("About")
    aboutTl.config(bg="white")
    aboutTitle = tk.Label(aboutTl, text="Timetable", bg="white", font=(None, "32"))
    aboutTitle.pack(pady=(20, 0), padx=10)
    aboutVer = tk.Label(aboutTl, text="Version {}".format(VER_NO), bg="white")
    aboutVer.pack(pady=(0, 40))
    aboutCredit = tk.Label(aboutTl, text="©{} Henry Lunn".format(datetime.now().year), bg="white")
    aboutCredit.pack(pady=20)
    aboutClose = tk.Button(aboutTl, text="Close", command=aboutTl.destroy, bg="white", relief="solid")
    aboutClose.pack(pady=10)


def launchCreator():
    try:
        import creator
    except:
        tk.messagebox.showerror("ImportError", "Creator file not found.")
    else:
        pass


root = tk.Tk()
root.title("Timetable")
root.iconbitmap("time.ico")
root.state("zoomed")
root.config(bg="white")
table = timetable("tabledata.txt")
infoFrm = tk.Frame(root, bg="white")
infoFrm.pack(side="right", fill="both", expand=True)
divFrm = tk.Frame(root, bg="black", width=3)
divFrm.pack(fill="y", side="right")
dateLab = tk.Label(infoFrm, text="{DATE}", bg="white", font=(None, "40"), wraplength=400)
dateLab.pack(pady=10)
timeLab = tk.Label(infoFrm, text="{TIME}", bg="white", font=(None, "40"))
timeLab.pack(pady=10)
vDiv1 = tk.Frame(infoFrm, height=3, bg="black")
vDiv1.pack(fill="x", pady=20)
lsnLab = tk.Label(infoFrm, text="{LESSON}", bg="white", font=(None, "40"))
lsnLab.pack()
remLab = tk.Label(infoFrm, text="{REMAINING}", bg="white", font=(None, "24"))
remLab.pack()
addLab = tk.Label(infoFrm, text="{ADD. INFO}", bg="white", font=(None, "24"))
addLab.pack()
vDiv2 = tk.Frame(infoFrm, height=3, bg="black")
vDiv2.pack(fill="x", pady=20)
table.updateTime()
menubar = tk.Menu(root)
sMenu = tk.Menu(menubar, tearoff=0)
sMenu.add_command(label="Load another timetable", command=newTable)
sMenu.add_command(label="Change colours...", command=table.changeColours)
sMenu.add_command(label="Change week number...", command=table.weekSet)
menubar.add_cascade(label="Settings", menu=sMenu)
menubar.add_command(label="Launch timetable creator", command=launchCreator)
menubar.add_command(label="About", command=about)
menubar.add_command(label="Exit", command=root.destroy)
root.config(menu=menubar)
root.mainloop()
