import tkinter as tk
import random

BACKGROUND_COLOUR = "white"
BORDER_COLOUR = "black"
TEXT_COLOUR = "black"
SNAKE_COLOURS = ["#ffd343","#2b5b84"] #The 2 colours for the snake
SNAKE_SPEED = 100 #How often it moves in ms
ADD_LENGTH = 3 #How much length is added
ADD_SCORE = 3 #How much is added to the score

"""
Default options:

BACKGROUND_COLOUR = "white"
BORDER_COLOUR = "black"
TEXT_COLOUR = "black"
SNAKE_COLOURS = ["#ffd343","#2b5b84"]
SNAKE_SPEED = 100
ADD_LENGTH = 3
ADD_SCORE = 3
"""

root = tk.Tk()
root.title("Python")
root.config(bg = BACKGROUND_COLOUR)
root.state("zoomed")
root.resizable(False,False)

pythonColour = SNAKE_COLOURS
scores = [0,4] #Score and length
isGameOver = False
firstKeyPressed = False
constantDirection = "right"

def checkCrash():
    checkFood()
    headCoords = mainCnv.coords("snake_head")
    overCoords = [-20,-20,w + 20,h + 20]
    matches = [x for x, y in enumerate(headCoords) if y == overCoords[x]]
    if len(matches) > 0:
        gameOver("edge")
    else:
        snakeParts = [mainCnv.coords(z) for z in [x[0] for x in turnData[1:]]]
        if headCoords in snakeParts:
            gameOver("self")

def gameOver(reason):
    global isGameOver
    isGameOver = True
    xPos = mainCnv.winfo_width() / 2
    yPos = mainCnv.winfo_height() / 2
    goHeight = yPos / 1.2
    goWidth = xPos / 1.2
    mainCnv.create_window((xPos, yPos), height = goHeight, width = goWidth, anchor = "s", window = goFrm, tag = "gameOver")
    scoreStr = "Score: " + str(scores[0])
    gosLab.config(text = scoreStr)
    lenStr = "Length: " + str(scores[1])
    golLab.config(text = lenStr)

def restartAll():
    global isGameOver, scores, firstKeyPressed, constantAfter
    mainCnv.delete("gameOver")
    isGameOver = False
    firstKeyPressed = False
    scores = [0,4]
    root.after_cancel(constantAfter)
    delSnake = [z for z in [x[0] for x in turnData]]
    for i in delSnake:
        mainCnv.delete(i)
    mainCnv.delete("food")
    scoreLab.config(text = "Score: 0")
    lenLab.config(text = "Length: 4")
    createSnake()
    spawnFruit()

def updateTurnData():
    global turnData
    turnData[0][1] = turnData[0][2]
    for i, j in enumerate(turnData):
        #Change previous to current
        turnData[i][1] = turnData[i][2]
        #Change current to previous item previous
        turnData[i][2] = turnData[i-1][1]

def updateScore(points):
    global scores
    scores[0] += points
    scoreLab.config(text = "Score: {}".format(scores[0]))

def updateLength(amount):
    global scores
    scores[1] += amount
    lenLab.config(text = "Length: {}".format(scores[1]))

def spawnFruit():
    global w, h
    snakeParts = [mainCnv.coords(z) for z in [x[0] for x in turnData]]
    xmax = (w - 20) / 20
    ymax = (h - 20) / 20
    randX = random.randint(0, xmax) * 20
    randY = random.randint(0, ymax) * 20
    rx2 = randX + 20
    ry2 = randY + 20
    match = len([x for x in snakeParts if x == [randX, randY, rx2, ry2]])
    if match > 0:
        spawnFruit()
    else:
        mainCnv.create_rectangle(randX, randY, rx2, ry2, fill = "red", tag = "food")

def constantMove():
    global constantAfter
    keyPress(constantDirection, False)
    constantAfter = root.after(SNAKE_SPEED,constantMove)

def checkFood():
    snakeArea = mainCnv.coords("snake_head")
    foodArea = mainCnv.coords("food")
    if snakeArea == foodArea:
        mainCnv.delete("food")
        addMass(ADD_LENGTH)
        updateLength(ADD_LENGTH)
        updateScore(ADD_SCORE)
        spawnFruit()

def keyPress(direction, user, event = None):
    oppositeDirections = {"up":"down","down":"up","left":"right","right":"left"}
    global isGameOver, turnData, firstKeyPressed, constantDirection
    if firstKeyPressed == False:
        constantDirection = direction
        firstKeyPressed = True
        constantMove()
    if isGameOver != True and turnData[0][1] != oppositeDirections[direction] and user == False:
        turnData[0][2] = direction
        constantDirection = direction
        for i in turnData:
            itemId = i[0]
            direction = i[2]
            if direction == "up":
                mainCnv.move(itemId, 0, -20)
            elif direction == "down":
                mainCnv.move(itemId, 0, 20)
            elif direction == "left":
                mainCnv.move(itemId, -20, 0)
            elif direction == "right":
                mainCnv.move(itemId, 20, 0)
        checkCrash()
        updateTurnData()
    elif user == True and turnData[0][1] != oppositeDirections[direction]:
        constantDirection = direction
    
def getRounded(dimen,num):
    if dimen % num == 0:
        return dimen
    else:
        diff = dimen % num
        half = int(num / 2)
        maxmn = int(num - 1)
        if diff < 10:
            return dimen - diff
        else:
            diff = num - diff
            return dimen + diff

def drawGrid():
    global w, h
    w = getRounded(mainCnv.winfo_width(),20) - 20
    h = getRounded(mainCnv.winfo_height(),20) - 20
    """
    for i in range(0, w + 1, 20):
        mainCnv.create_line([(i, 0), (i, h)], tag='grid_line')

    for i in range(0, h + 1, 20):
        mainCnv.create_line([(0, i), (w, i)], tag='grid_line')
    """
    #Top red line
    mainCnv.create_line([(0,0), (w, 0)], tag = "out_line", fill = "red", width = 3)
    #Bottom red line
    mainCnv.create_line([(0,h), (w, h)], tag = "out_line", fill = "red", width = 3)
    #Left red line
    mainCnv.create_line([(0,0), (0, h)], tag = "out_line", fill = "red", width = 3)
    #Right red line
    mainCnv.create_line([(w, 0),(w, h)], tag = "out_line", fill = "red", width = 3)

def addMass(amount):
    for i in range(amount):
        if bodyCount[1] == 0:
            bgCol = pythonColour[0]
            bodyCount[1] = 1
        elif bodyCount[1] == 1:
            bgCol = pythonColour[1]
            bodyCount[1] = 0
        prevBodyRect = "body_" + str(bodyCount[0])
        previousCoords = mainCnv.coords(prevBodyRect)
        previousDirection = turnData[bodyCount[0]][2]
        bodyCount[0] += 1
        newBodyRect = "body_" + str(bodyCount[0])
        turnData.append([newBodyRect,"right",turnData[bodyCount[0] - 1][2]])
        if previousDirection == "up":
            snakeX1 = previousCoords[0]
            snakeY1 = previousCoords[1] + 20
            snakeX2 = previousCoords[2]
            snakeY2 = previousCoords[3] + 20
        elif previousDirection == "down":
            snakeX1 = previousCoords[0]
            snakeY1 = previousCoords[1] - 20
            snakeX2 = previousCoords[2]
            snakeY2 = previousCoords[3] - 20
        elif previousDirection == "left":
            snakeX1 = previousCoords[0] + 20
            snakeY1 = previousCoords[1]
            snakeX2 = previousCoords[2] + 20
            snakeY2 = previousCoords[3]
        elif previousDirection == "right":
            snakeX1 = previousCoords[0] - 20
            snakeY1 = previousCoords[1]
            snakeX2 = previousCoords[2] - 20
            snakeY2 = previousCoords[3]
        mainCnv.create_rectangle(snakeX1,snakeY1,snakeX2,snakeY2, fill = bgCol, tag = (newBodyRect,"snake_body","snake"))
          
def createSnake():
    global snake, bodyCount, turnData
    bodyCount = [] #bodyCount[0] = number of snake parts, [1] = yellow or blue
    #Turn data is in the format [previous,current] and the next part's current is the last part's previous
    turnData = [["snake_head","right",None],["body_1","right","right"],["body_2","right","right"],["body_3","right","right"]]
    snakeHead = mainCnv.create_rectangle(120,120,140,100, fill = pythonColour[0], tag = ("snake_head", "snake"))
    body1 = mainCnv.create_rectangle(100,120,120,100, fill = pythonColour[1], tag = ("body_1","snake_body", "snake"))
    body2 = mainCnv.create_rectangle(80,120,100,100, fill = pythonColour[0], tag = ("body_2","snake_body", "snake"))
    body3 = mainCnv.create_rectangle(60,120,80,100, fill = pythonColour[1], tag = ("body_3","snake_body", "snake"))
    bodyCount.append(3)
    bodyCount.append(0)


#GUI

opsFrm = tk.Frame(root, bg = BACKGROUND_COLOUR)
opsFrm.pack(pady = 10, fill = "x", padx = 10)

dividerFrm = tk.Frame(root, bg = BORDER_COLOUR, height = 2)
dividerFrm.pack(fill = "x")

titleFrm = tk.Frame(opsFrm)
titleFrm.pack(side = "left")
word = ["P","y","t","h","o","n"]
for letter, i in enumerate(word):
    textCol = pythonColour[letter%2]
    tk.Label(titleFrm, text = i, bg = BACKGROUND_COLOUR, fg = textCol, font = ("Courier New", "20")).grid(row = 0, column = letter)
   

scoreLab = tk.Label(opsFrm, text = "Score: 0", bg = BACKGROUND_COLOUR, fg = TEXT_COLOUR, font = ("Courier New", "16"))
scoreLab.pack(padx = 10, side = "left")

lenLab = tk.Label(opsFrm, text = "Length: 4", bg = BACKGROUND_COLOUR, fg = TEXT_COLOUR, font = ("Courier New", "16"))
lenLab.pack(padx = 10, side = "left")

exitBtn = tk.Button(opsFrm, text = "Exit", bg = BACKGROUND_COLOUR, relief = "solid", borderwidth = 2, command = root.destroy, font = ("Courier New", "12"))
exitBtn.pack(ipadx = 10, side = "right")

mainCnv = tk.Canvas(root, bg = BACKGROUND_COLOUR, highlightthickness = 0)
mainCnv.pack(fill = "both", expand = True, padx = 20, pady = 20)
mainCnv.update()
#Game over window
goFrm = tk.Frame(mainCnv, bg = BACKGROUND_COLOUR, relief = "solid", borderwidth = 3)
goInrFrm = tk.Frame(goFrm, bg = BACKGROUND_COLOUR)
goInrFrm.pack(expand = True)
goLab = tk.Label(goInrFrm, text = "Game Over!", fg = TEXT_COLOUR, font = ("Courier New", "28"), bg = BACKGROUND_COLOUR)
goLab.pack(pady = (0,20))
gosLab = tk.Label(goInrFrm, text = "Error", fg = TEXT_COLOUR, bg = BACKGROUND_COLOUR, font = ("Courier New", "20"))
gosLab.pack()
golLab = tk.Label(goInrFrm, text = "Error", fg = TEXT_COLOUR, bg = BACKGROUND_COLOUR, font = ("Courier New", "20"))
golLab.pack()
playBtn = tk.Button(goInrFrm, text = "Play again", fg = TEXT_COLOUR, command = restartAll, bg = BACKGROUND_COLOUR, relief = "solid", font = ("Courier New", "12"))
playBtn.pack(pady = 20, ipadx = 10)

#Key bindings

root.bind("<Up>", lambda event: keyPress("up",True))
root.bind("<Down>", lambda event: keyPress("down",True))
root.bind("<Left>", lambda event: keyPress("left",True)) 
root.bind("<Right>", lambda event: keyPress("right",True))
root.bind("<w>", lambda event: keyPress("up",True))
root.bind("<a>", lambda event: keyPress("left",True))
root.bind("<s>", lambda event: keyPress("down",True))
root.bind("<d>", lambda event: keyPress("right",True))

drawGrid()
createSnake()
spawnFruit()
root.mainloop()
