####################################
#   Böggle™ Experimental edition   #
#             Henry Lunn           #
####################################
import tkinter as tk, urllib.request, random, string, webbrowser, datetime, tkinter.scrolledtext, tkinter.messagebox, re
root = tk.Tk()
root.title("Böggle™")
x = (root.winfo_screenwidth()//2) - 250
y = (root.winfo_screenheight()//2) - 250
root.geometry("500x500+{}+{}".format(x,y))
root.config(bg = "white")
dictLoaded = False
wordDict = None
inGame = False
correctWords = []
possibleWords = None
#The inverted scrabble scores of letters (used to determine probability of appearance)
invertedScrabbleScores = [['A', 10], ['B', 8], ['C', 8], ['D', 9], ['E', 10], ['F', 7], ['G', 9], ['H', 7], ['I', 10], ['J', 3], ['K', 6], ['L', 10], ['M', 8], ['N', 10], ['O', 10], ['P', 8], ['Q', 1], ['R', 10], ['S', 10], ['T', 10], ['U', 10], ['V', 7], ['W', 7], ['X', 3], ['Y', 7], ['Z', 1]]
randomLettersChoices = sum([list(y.lower()) for y in [x[0]*x[1] for x in invertedScrabbleScores]],[]) #Gets them all into one list
randLetter = lambda: random.choice(randomLettersChoices) #Chooses one
class boggle():
    def __init__(self, master):
        global possibleWords
        self.tiles = []
        self.tileFrame = tk.Frame(master)
        self.firstLetterSelected = False
        self.firstLetter = None
        self.validNext = None
        self.selectedObjects = []
        self.selectedLetters = []
        self.blockClick = False
        for r in range(4):
            self.tiles.append([])
            for c in range(4):
                f = tk.Frame(self.tileFrame, height = 50, width = 50, bg = "white", highlightbackground = "black", highlightthickness = 1)
                b = tk.Label(f, bg = "white", text = randLetter(), font = ("Comic Sans MS","20"))
                f.rowconfigure(0, weight =  1)
                f.columnconfigure(0, weight = 1)
                f.grid_propagate(0)
                b.bind("<Button-1>", lambda event, a = b: self.letterSelected(a))
                self.tiles[r].append(b)
                b.grid(sticky = "nesw")
                f.grid(row = r, column = c, sticky = "nesw", ipadx = 5, ipady = 2)
        possibleWords = self.possibleSolutions()
        updateList()
    def clearColours(self):
        for r in self.tiles:
            for i in r:
                i.config(bg = "white", fg = "black")
    def reset(self):
        self.selectedObjects = []
        self.selectedLetters = []
        self.firstLetter = None
        self.firstLetterSelected = False
        self.validNext = None
        self.blockClick = False
        self.clearColours()
    def checkIfWord(self):
        if "".join(self.selectedLetters) in loadDictionary() and len(self.selectedLetters) > 2:
            return (True, "".join(self.selectedLetters))
        else:
            return (False,None)
    def addToList(self, add):
        global correctWords
        correctWords.append(add)
        updateList()
    def waitReset(self):
        root.after(500,self.reset())
    def letterSelected(self, obj):
        if not self.blockClick:
            global correctWords
            if not self.firstLetterSelected: #First letter is selected
                self.firstLetter = obj
                self.firstLetterSelected = True
                self.validNext = self.getAdj(obj)
                self.selectedObjects.append(obj)
                self.selectedLetters.append(obj.cget("text"))
                obj.config(bg = "black", fg = "white")
            else:
                if obj in self.validNext and obj not in self.selectedObjects: #Valid letter is selected
                    self.selectedObjects.append(obj)
                    self.selectedLetters.append(obj.cget("text"))
                    self.validNext = self.getAdj(obj)
                    check = self.checkIfWord()
                    if check[0] and check[1] not in correctWords: #Check if word
                        self.blockClick = True
                        obj.config(bg = "black", fg = "white")
                        self.addToList(check[1])
                        for i in self.selectedObjects:
                            i.config(bg = "green")
                        root.update()
                        self.waitReset()
                    else:
                        obj.config(bg = "black", fg = "white")
                else:
                    pass
    def possibleSolutions(self):
        grid = ["".join([y.cget("text") for y in x]) for x in self.tiles]
        nrows, ncols = len(grid), len(grid[0])
        alphabet = ''.join(set(''.join(grid)))
        bogglable = re.compile('[' + alphabet + ']{3,}$', re.I).match
        words = set(word.rstrip('\n') for word in loadDictionary() if bogglable(word))
        prefixes = set(word[:i] for word in words
                       for i in range(2, len(word)+1))
        def solve():
            for y, row in enumerate(grid):
                for x, letter in enumerate(row):
                    for result in extending(letter, ((x, y),)):
                        yield result

        def extending(prefix, path):
            if prefix in words:
                yield (prefix, path)
            for (nx, ny) in neighbors(path[-1]):
                if (nx, ny) not in path:
                    prefix1 = prefix + grid[ny][nx]
                    if prefix1 in prefixes:
                        for result in extending(prefix1, path + ((nx, ny),)):
                            yield result

        def neighbors(t):
            x,y = t
            for nx in range(max(0, x-1), min(x+2, ncols)):
                for ny in range(max(0, y-1), min(y+2, nrows)):
                    yield (nx, ny)
        possibleWords = list(set([x[0] for x in set(solve())]))
        return (possibleWords, len(possibleWords))
    def returnObject(self, row, column):
        return self.tiles[row,column]
    def getAdj(self, tileObject):
        loc = None
        for rn, r in enumerate(self.tiles):
            for cn, c in enumerate(r):
                if tileObject == c:
                    loc = [rn,cn]
        if loc:
            r,c = loc
            validSquares = []
            surround = [[r-1,c-1],[r-1,c],[r-1,c+1],[r,c-1],[r,c+1],[r+1,c-1],[r+1,c],[r+1,c+1]]
            for i in surround:
                try:
                    self.tiles[i[0]][i[1]]
                except:
                    pass
                else:
                    validSquares.append(self.tiles[i[0]][i[1]])
            return validSquares
        else:
            raise AttributeError("tileObject is not valid")

def updateList():
    global correctWords, board, possibleWords
    wordList.config(state = "normal")
    wordList.delete(1.0,"end")
    wordList.insert(1.0,"\n".join(["{} possible words".format(possibleWords[1]),"Words found:"]+["{}. {}".format(str(i+1),x) for i,x in enumerate(correctWords)]))
    wordList.see("end")
    wordList.config(state = "disabled")

def resetBoard():
    global board
    board.reset()

def newGame():
    global board, correctWords, possibleWords
    missed = tk.Toplevel(root)
    missText = tk.scrolledtext.ScrolledText(missed, height = 10, width = 30, state = "disabled", font = ("Comic Sans MS","16"))
    misd = list(set(possibleWords[0]) - set(correctWords))
    txt = "\n".join(["Words missed:"]+["{}. {}".format(str(i+1),x) for i,x in enumerate(misd)])
    missText.config(state = "normal")
    missText.insert(1.0,txt)
    missText.config(state = "disabled")
    missText.pack()
    correctWords = []
    updateList()
    board.tileFrame.destroy()
    bottomButtonFrame.grid_forget()
    wordList.grid_forget()
    board = boggle(gameFrame)
    gameTitle.grid(row = 0, column = 0)
    board.tileFrame.grid(row = 1, column = 0)
    bottomButtonFrame.grid(row = 2, column = 0, sticky = "n")
    wordList.grid(row = 0, column = 1, rowspan = 3, padx = (20,0))
    

def loadDictionary():
    global dictLoaded, wordDict
    if not dictLoaded: #Only has to load the dictionary once
        try: #Catches error when trying to connect to website
            #From https://stackoverflow.com/a/49524775
            dictUrl = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
            urlResponse = urllib.request.urlopen(dictUrl)
            rawDict = urlResponse.read().decode()
            wordDict = rawDict.splitlines()
            dictLoaded = True
        except:
            tk.messagebox.showerror("Error", "Can't connect to the internet to download dictionary, please check your connection")
            root.destroy()
        else:
            return wordDict
    else:
        return wordDict

def startGame():
    global board, inGame
    credLab.place_forget()
    menuFrame.place_forget()
    gameFrame.pack(padx = 10)
    board = boggle(gameFrame)
    updateList()
    gameTitle.grid(row = 0, column = 0)
    board.tileFrame.grid(row = 1, column = 0)
    bottomButtonFrame.grid(row = 2, column = 0, sticky = "n")
    wordList.grid(row = 0, column = 1, rowspan = 3, padx = (20,0))
    gameFrame.grid_columnconfigure(0, weight = 1, uniform = "col")
    gameFrame.grid_columnconfigure(1, weight = 1, uniform = "col")
    gameFrame.grid_rowconfigure(0, weight = 1, uniform = "row")
    gameFrame.grid_rowconfigure(1, weight = 3, uniform = "row")
    gameFrame.grid_rowconfigure(2, weight = 2, uniform = "row")
    inGame = True

def init():
    root.update()
    loadDictionary()
    root.after(10, lambda:startFrame.pack_forget())
    menuFrame.place(relx = 0.5, rely = 0.5, anchor = "center")
    credLab.place(x = 10, y = root.winfo_height()-30)

startFrame = tk.Frame(root, bg = "white")
startFrame.pack(expand = True, fill = "both")
startNote = tk.Label(startFrame, text = "Loading...", font = ("Comic Sans MS","30"), bg = "white")
startNote.pack(expand = True, fill = "both")
menuFrame = tk.Frame(root, bg = "white")
titleLab = tk.Label(menuFrame, text = "Böggle™", font = ("Comic Sans MS","40"), bg = "white")
titleLab.grid(row = 0, column = 0, pady = (10,0), columnspan = 2)
sub1Lab = tk.Label(menuFrame, text = "Not to be confused with", bg = "white", font = (None,10,"italic"))
sub1Lab.grid(row=1,column = 0, sticky = "e")
sub2Lab = tk.Label(menuFrame, text = "Boggle", bg = "white", fg = "blue", font = (None,10,"underline italic"), cursor="hand2")
sub2Lab.bind("<Button-1>", lambda event: webbrowser.open("https://en.wikipedia.org/wiki/Boggle"))
sub2Lab.grid(row=1, column = 1, sticky = "w")
playBtn = tk.Button(menuFrame, text = "Play!", cursor="hand2", font = ("Comic Sans MS","30"), width = 10, relief = "solid", command = startGame, bg = "white")
playBtn.grid(row = 2, column = 0, pady = 40, columnspan = 2)
credLab = tk.Label(root, text = "Böggle™ 1.0.0 ©{} Henry Lunn".format(datetime.datetime.now().year), font = ("Comic Sans MS","10"), bg = "white")
gameFrame = tk.Frame(root, bg = "white")
gameTitle = tk.Label(gameFrame, text = "Böggle™", font = ("Comic Sans MS","20"), bg = "white")
bottomButtonFrame = tk.Frame(gameFrame, bg = "white")
gameClear = tk.Button(bottomButtonFrame, text = "Clear", command = resetBoard, bg = "white", relief = "solid", font = ("Comic Sans MS","16"))
gameClear.grid(row = 0, column = 0, pady = 10, columnspan = 2)
gameNew = tk.Button(bottomButtonFrame, text = "New game", command = newGame, bg = "white", relief = "solid", font = ("Comic Sans MS","16"))
gameNew.grid(row = 1, column = 0, padx = 5)
gameExit = tk.Button(bottomButtonFrame, text = "Exit", command = lambda: root.destroy(), bg = "white", relief = "solid", font = ("Comic Sans MS","16"))
gameExit.grid(row = 1, column = 1, padx = 5)
wordList = tk.scrolledtext.ScrolledText(gameFrame, state = "disabled", font = ("Comic Sans MS","16"))
root.bind("<Escape>", lambda event: resetBoard())
root.after(100, init)
root.mainloop()

