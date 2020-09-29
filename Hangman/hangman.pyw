import tkinter as tk, urllib.request, random, tkinter.messagebox
root = tk.Tk()
WIN_HEIGHT = 300
WIN_WIDTH = 800
LEFT_WIDTH = 500
RIGHT_WIDTH = 300
alreadyLoaded = False
currentStickState = 0 #The current state of the stickman
letterDict = {} #Dictionary of letter postions
guessedLetterDict = {}
guessedLettersDict = {"y":[],"n":[]} #Guessed letters
alreadyGuessed = []
goodWords = []
guessWord = ""
gameStart = False
root.title("Hangman")
root.geometry("{}x{}".format(WIN_WIDTH,WIN_HEIGHT))
root.resizable(False, False)
def ext():
    root.destroy()
def newGame():
    global gameStart, guessWord, currentStickState, guessedLettersDict, guessedLetterDict, alreadyGuessed, letterDict
    currentStickState = 0 #The current state of the stickman
    letterDict = {} #Dictionary of letter postions
    guessedLetterDict = {}
    guessedLettersDict = {"y":[],"n":[]} #Guessed letters
    alreadyGuessed = []
    gameOverFrm.grid_remove()
    introFrm.grid()
    guessWord = ""
    guessLab.config(text = "")
    stickCnv.delete("all")
    tkEntError("")
    gameStart = False
    currentStickState = 0
    mainLab.config(text = "Guess a letter")
    
def gameOver(wl):
    global guessWord
    mainFrm.grid_remove()
    gameOverFrm.grid()
    if wl == "w":
        gameOverLabel.config(text = "Well done!")
    else:
        gameOverLabel.config(text = "Game over!")
    gameOverLab2.config(text = "The word was " + guessWord)

def returnHandle(event):
    global gameStart
    if gameStart:
        tryLetter()

def tryLetter():
    global guessedLetterDict, guessedLettersDict, letterDict, currentStickState, alreadyGuessed
    alreadyGuessed = [x for y in list(guessedLettersDict.values()) for x in y]
    userGuess = mainEnt.get()
    mainEnt.delete(0,"end")
    if userGuess.isalpha() != True or len(userGuess) != 1:
        mainLab.config(text = "Enter 1 letter")
    else:
        if userGuess in alreadyGuessed: #Checks if letter has been entered yet
            mainLab.config(text = "Letter already guessed")
        else:
            correctLetterList = [i for i, x in enumerate(letterDict.values()) if userGuess == x]
            #^Finds the indexes of the letters that match the user guess
            if len(correctLetterList) == 0: #If there are no matches, then the letter isn't in the word
                mainLab.config(text = userGuess + " is not in the word")
                currentStickState += 1 #Removes another part of the stickman
                if currentStickState == 9: #The final stickState means the game is over
                    drawStick(9)
                    gameOver("l")
                else:
                    guessedLettersDict["n"].append(userGuess) #Adds the guess to the list of incorrect guesses
                    drawStick(currentStickState)
            else:
                mainLab.config(text = "Correct letter!")
                for i in correctLetterList: #Iterates through the list of correct letter indexes
                    if letterDict[i] not in guessedLettersDict["y"]: #Checks if letter is already in the correct geuss list (for)
                        guessedLettersDict["y"].append(letterDict[i])
                    guessedLetterDict[i] = letterDict[i]
                        #^The letter at the position in the answer is added to the letters guessed
                if letterDict == guessedLetterDict: #If the letters guessed = the answer
                    wordLab.config(text = " ".join([v for v in guessedLetterDict.values()]))
                    mainLab.config(text = "You guessed the word!")
                    gameOver("w")
                else:
                    wordLab.config(text = " ".join([v for v in guessedLetterDict.values()]))
            gLabList = [x for y in list(guessedLettersDict.values()) for x in y]
            guessLab.config(text = ", ".join(gLabList))
            
def drawStick(stickNumber):
    root.update()
    cnvH = stickCnv.winfo_height()
    cnvW = stickCnv.winfo_width()
    if stickNumber == 0:
        stickCnv.create_line(cnvW-1, cnvH, cnvW-1, 0, fill = "black")
    if stickNumber == 1:
        stickCnv.create_line(50, cnvH - 50, 50, 50, fill = "black")
    if stickNumber == 2:
        stickCnv.create_line(50, 50, cnvW - 50, 50, fill = "black")
        stickCnv.create_line(50, 80, 80, 50, fill = "black")
    if stickNumber == 3:
        stickCnv.create_line(cnvW/2, 50, cnvW/2 ,90, fill = "black")
    if stickNumber == 4:
        stickCnv.create_oval(cnvW/2 - 15, 90, cnvW/2 + 15, 120, outline = "black")
    if stickNumber == 5:
        stickCnv.create_line(cnvW/2, 120, cnvW/2 ,170, fill = "black")
    if stickNumber == 6:
        stickCnv.create_line(cnvW/2, 130,cnvW/2-20,150, fill = "black")
    if stickNumber == 7:
        stickCnv.create_line(cnvW/2, 130,cnvW/2+20,150, fill = "black")
    if stickNumber == 8:
        stickCnv.create_line(cnvW/2, 170,cnvW/2-20,190, fill = "black")
    if stickNumber == 9:
        stickCnv.create_line(cnvW/2, 170,cnvW/2+20,190, fill = "black")
    
    
def startGame(gw):
    global gameStart, guessWord
    guessWord = gw
    for i, l in enumerate(guessWord): #Creates letterDict and guessedLetterDict from guessWord
        letterDict[i] = l
        guessedLetterDict[i] = "_"
    mainEnt.focus()
    gameStart = True
    drawStick(0)
    wordLab.config(text = " ".join([v for v in guessedLetterDict.values()]))

    
def getRandomWord():
    global alreadyLoaded, goodWords
    if alreadyLoaded == False: #Only has to load the website once
        try: #Catches error when trying to connect to website
            #From https://stackoverflow.com/a/49524775
            wordsUrl = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
            response = urllib.request.urlopen(wordsUrl)
            wordText = response.read().decode()
            wordList = wordText.splitlines()
            goodWords = [x for x in wordList if len(x) >= 4 and x[0].islower() and "'" not in x] #Only uses words 4 or more letters long which aren't proper nouns
        except:
            tk.messagebox.showerror("Error", "Can't connect to the internet, please check your connection")
            root.destroy()
        else:
            alreadyLoaded = True
            guessWord = random.choice(goodWords) #Randomly chooses a word from the refined list
    else:
        guessWord = random.choice(goodWords) #Randomly chooses a word from the refined list
    return guessWord     
def tkChoose():
    introFrm.grid_remove()
    enterFrm.grid()
    enterEnt.focus()
def tkRandom():
    introFrm.grid_remove()
    tkMainDisplay(getRandomWord())
def tkEntError(msg):
    enterErr.config(text = msg)
def tkGetWord():
    tkGw = enterEnt.get().lower()
    if tkGw.isalpha() != True:
        tkEntError("Enter only letters")
    else:
        if len(tkGw) > 26:
            tkEntError("Maximum word length is 26")
        else:
            enterFrm.grid_remove()
            enterEnt.delete(0, "end")
            tkMainDisplay(tkGw)
def tkMainDisplay(guessWord):
    mainFrm.grid()
    startGame(guessWord)
#START FRAME
introFrm = tk.Frame(root, height = WIN_HEIGHT, width = WIN_WIDTH, bg = "white")
introFrm.grid()
introMain = tk.Frame(introFrm, height = WIN_HEIGHT, width = WIN_WIDTH, bg = "white")
introMain.place(relx=0.5, rely = 0.4, anchor = "center")
introMainLab = tk.Label(introMain, text = "Hangman", font = ("Courier","24"), bg = "white")
introMainLab.grid(row = 0, column = 0, columnspan = 2, pady = 50)
introOpt1 = tk.Button(introMain, text = "Choose a word", bg = "white", relief = "solid", font = ("Courier","16"), command = tkChoose)
introOpt1.grid(row = 1, column = 0, padx = 10)
introOpt2 = tk.Button(introMain, text = "Random word", bg = "white", relief = "solid", font = ("Courier", "16"), command = tkRandom)
introOpt2.grid(row = 1, column = 1, padx = 10)
introOpt2pw = tk.Label(introMain, text = "Requires internet", bg = "white", font = ("Courier", "10"))
introOpt2pw.grid(row = 2, column = 1, padx = 5)
creditLab = tk.Label(introFrm, text = "Made by Henry Lunn", bg = "white", font = ("Courier","10"))
creditLab.place(x = 630, y = 270)
#ENTER WORD FRAME
enterFrm = tk.Frame(root, height = WIN_HEIGHT, width = WIN_WIDTH, bg = "white")
enterCenter = tk.Frame(enterFrm, bg = "white")
enterCenter.place(relx=0.5, rely = 0.4, anchor = "center")
enterLab = tk.Label(enterCenter, text = "Enter word:", bg = "white", font = ("Courier","16"))
enterLab.grid(row = 0, column = 0)
enterEnt = tk.Entry(enterCenter, font = ("Courier","16"))
enterEnt.grid(row = 1, column = 0, pady = 20)
enterBtn = tk.Button(enterCenter, text = "Play", command = tkGetWord, font = ("Courier","16"), bg = "white", relief = "solid")
enterBtn.grid(row = 2, column = 0)
enterErr = tk.Label(enterCenter, text = "", bg = "white", fg = "red", font = ("Courier","12"))
enterErr.grid(row = 3, column = 0)
#MAIN FRAME
mainFrm = tk.Frame(root, height = WIN_HEIGHT, width = WIN_WIDTH, bg = "white")
#LEFT HAND SIDE
leftFrm = tk.Frame(mainFrm, width = RIGHT_WIDTH, height = WIN_HEIGHT)
leftFrm.pack(side = "left")
stickCnv = tk.Canvas(leftFrm, width = RIGHT_WIDTH, height = WIN_HEIGHT, highlightthickness = 0, bg = "white")
stickCnv.pack()
#RIGHT HAND SIDE
rightFrm = tk.Frame(mainFrm, width = LEFT_WIDTH, height = WIN_HEIGHT, bg = "white")
rightFrm.pack(side = "left")
#WORD GUESS FRAME
wordFrm = tk.Frame(rightFrm, width = LEFT_WIDTH, height = 100, bg = "white")
wordFrm.pack()
wordLab = tk.Label(wordFrm, bg = "white", text = "_ _ _", font = ("Courier", "24"), wraplength = 500, justify = "left")
wordLab.place(relx = 0.5, rely = 0.5, anchor = "center")
#ENTRY/BUTTON FRAME
btnFrm = tk.Frame(rightFrm, width = LEFT_WIDTH, height = 100, bg = "white")
btnFrm.pack()
mainEnt = tk.Entry(btnFrm, font = ("Courier", "24"),width = 2)
mainEnt.grid(row = 0, column = 0, padx = 10)
mainBtn = tk.Button(btnFrm, text = "Enter", command = tryLetter, font = ("Courier", "16"), bg = "white", relief = "solid")
mainBtn.grid(row = 0, column = 1)
mainLab = tk.Label(btnFrm, text = "Guess a letter", bg = "white", font = ("Courier", "16"))
mainLab.grid(row = 1, column = 0, columnspan = 2)
#ALREADY GUESSED LETTERS
guessFrm = tk.Frame(rightFrm, width = LEFT_WIDTH, height = 100, bg = "white")
guessFrm.pack()
guessTtl = tk.Label(guessFrm, font = ("Courier", "18"), bg = "white", text = "Guessed letters:")
guessTtl.grid(row = 0, column = 0)
guessLab = tk.Label(guessFrm, font = ("Courier", "16"), wraplength = 500, justify = "left", bg = "white")
guessLab.grid(row = 1, column = 0)
#GAME OVER FRAME
gameOverFrm = tk.Frame(root, height = WIN_HEIGHT, width = WIN_WIDTH, bg = "white")
gameOverCenter = tk.Frame(gameOverFrm, bg = "white")
gameOverCenter.place(relx = 0.5, rely = 0.5, anchor = "center")
gameOverLabel = tk.Label(gameOverCenter, text = "", bg = "white", font = ("Courier", "24"))
gameOverLabel.grid(row = 0, column = 0, columnspan = 2)
gameOverLab2 = tk.Label(gameOverCenter, text = "", bg = "white", font = ("Courier", "16"))
gameOverLab2.grid(row = 1, column = 0, columnspan = 2, pady = 30)
gameOverOpt1 = tk.Button(gameOverCenter, text = "Play again", command = newGame, font = ("Courier", "16"), bg = "white", relief = "solid")
gameOverOpt1.grid(row = 2, column = 0,padx = 20)
gameOverOpt2 = tk.Button(gameOverCenter, text = "Exit", command = ext, font = ("Courier", "16"), bg = "white", relief = "solid")
gameOverOpt2.grid(row = 2, column = 1)

root.bind("<Return>", lambda event: tryLetter())
root.mainloop()
