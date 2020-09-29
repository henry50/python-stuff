import tkinter as tk
import string
import itertools
import math
"""
-------------
tkinter Chess
-------------
(C) Henry Lunn
Version 1.1.0, 15/03/2020
-------------
Everything except stuff listed below works.
Now with working movement!

Improvements needed:
--LESS IMPORTANT
-No check detection, game ends when you end it
-Pawns can't be promoted
-No support for en passant and castling (I don't even know what they are)
-------------
"""
class Chess(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Chess")
        self.geometry("540x540")
        self.resizable(False,False)
        self.canvas = tk.Canvas(self, height = 540, width = 540)
        self.canvas.pack()
        self.playerStatus = tk.Frame(self)
        self.playerStatus.pack()
        self.playerStatusText = tk.Label(self.playerStatus, text = "Current turn:")
        self.playerStatusText.grid(row = 0, column = 0, sticky = "nesw", padx = 10)
        self.playerStatusColour = tk.Frame(self.playerStatus, bg = "white", height = 30, width = 30, highlightthickness = 1, highlightbackground = "black")
        self.playerStatusColour.grid(row = 0, column = 1, sticky = "nesw")
        menubar = tk.Menu(self)
        menubar.add_command(label = "New game", command=self.newGame)
        menubar.add_command(label = "About", command = self.about)
        menubar.add_command(label = "Switch colours", command = self.recolour)
        self.config(menu=menubar)
        self.unicodePieces = {"w":{"k":"\u2654","q":"\u2655","r":"\u2656","b":"\u2657","kn":"\u2658","p":"\u2659"},
                              "b":{"k":"\u265A","q":"\u265B","r":"\u265C","b":"\u265D","kn":"\u265E","p":"\u265F"}}
        #Initial positions of pieces
        self.positionDict = {"w":{"k": [["1", "e"]], "q": [["1", "d"]], "r": [["1", "a"], ["1", "h"]], "b": [["1", "c"], ["1", "f"]], "kn": [["1", "b"], ["1", "g"]], "p": [["2", "a"], ["2", "b"], ["2", "c"], ["2", "d"], ["2", "e"], ["2", "f"], ["2", "g"], ["2", "h"]]},
                             "b":{"k": [["8", "e"]], "q": [["8", "d"]], "r": [["8", "a"], ["8", "h"]], "b": [["8", "c"], ["8", "f"]], "kn": [["8", "b"], ["8", "g"]], "p": [["7", "a"], ["7", "b"], ["7", "c"], ["7", "d"], ["7", "e"], ["7", "f"], ["7", "g"], ["7", "h"]]}}
        self.initialPositions = [['1', 'e'], ['1', 'd'], ['1', 'a'], ['1', 'h'], ['1', 'c'], ['1', 'f'], ['1', 'b'], ['1', 'g'], ['2', 'a'], ['2', 'b'], ['2', 'c'], ['2', 'd'], ['2', 'e'], ['2', 'f'], ['2', 'g'], ['2', 'h'], ['8', 'e'], ['8', 'd'], ['8', 'a'], ['8', 'h'], ['8', 'c'], ['8', 'f'], ['8', 'b'], ['8', 'g'], ['7', 'a'], ['7', 'b'], ['7', 'c'], ['7', 'd'], ['7', 'e'], ['7', 'f'], ['7', 'g'], ['7', 'h']]
        self.currentPlayer = "w"
        self.positions = {}
        self.clickState = False
        self.clickedItem = None
        self.colourState = 0
        self.drawBoard()
        self.centreWindow()
        self.addPieces()
        self.canvas.bind("<Button-1>", self.clickHandle)
    def about(self): #About window
        self.aboutTl = tk.Toplevel(self)
        self.aboutTl.title("About")
        bp,wp = [" ".join([x for x in self.unicodePieces[c].values()]) for c in ["b","w"]]
        self.aboutPiecesB = tk.Label(self.aboutTl, text = bp, font = (None, "24"))
        self.aboutPiecesB.pack()
        self.aboutTitle = tk.Label(self.aboutTl, text = "Chess", font = (None, "32"))
        self.aboutTitle.pack(padx = 50)
        self.aboutVersion = tk.Label(self.aboutTl, text = "Version 1.1.0")
        self.aboutVersion.pack(pady = 5)
        self.aboutCredit = tk.Label(self.aboutTl, text = "©2020 Henry Lunn")
        self.aboutCredit.pack(pady = 10)
        self.aboutClose = tk.Button(self.aboutTl, text = "Close", command = self.aboutTl.destroy, width = 10)
        self.aboutClose.pack(pady = (5,10), ipadx = 5, ipady = 5)
        self.aboutPiecesW = tk.Label(self.aboutTl, text = wp[::-1], font = (None, "24"))
        self.aboutPiecesW.pack()
        self.aboutTl.update()
        sh, sw = self.winfo_screenheight(), self.winfo_screenwidth()
        wh, ww = self.aboutTl.winfo_height(), self.aboutTl.winfo_width()
        centre = ww, wh, int((sw/2)-ww/2), int((sh/2)-wh/2)
        self.aboutTl.geometry("{}x{}+{}+{}".format(*centre))
        self.aboutTl.focus_force()
    def centreWindow(self):
        sh, sw = self.winfo_screenheight(), self.winfo_screenwidth()
        wh, ww = 590, 540
        centre = ww, wh, int((sw/2)-ww/2), int((sh/2)-wh/2)
        self.geometry("{}x{}+{}+{}".format(*centre))
    def newGame(self):
        self.destroy()
        self.__init__()
        self.focus_force()
    def drawBoard(self):
        s, o = 60, 30 #size and offset of squares
        for col in range(8):
            for row in range(8):
                r,c = row, col
                if c == 0:
                    self.canvas.create_text(15, s*(row+1), text = str(9-(row+1)))
                fill = "white" if (r+c) % 2 == 0 else "grey"
                fno = "light" if (r+c) % 2 == 0 else "dark"
                self.canvas.create_rectangle((s*c)+o,(s*r)+o,(s*(c+1))+o,(s*(r+1))+o, fill = fill, tags = ("rect",fno))
                self.positions[(str(9-(row+1)),string.ascii_lowercase[col])] = "empty"
            self.canvas.create_text(s*(col+1), s*(row+2)-15, text = string.ascii_uppercase[col])
    def recolour(self):
        if self.colourState == 0:
            light = "#E2D0B2"
            dark = "#704022"
            self.colourState = 1
        elif self.colourState == 1:
            light = "white"
            dark = "grey"
            self.colourState = 0
        for i in self.canvas.find_withtag("light"):
            self.canvas.itemconfig(i, fill = light)
        for i in self.canvas.find_withtag("dark"):
            self.canvas.itemconfig(i, fill = dark)
    def addPieces(self):
        for i in list(self.positionDict.keys()):
            for k, v in list(self.positionDict[i].items()):
                for j in v:
                    coords = self.gridRefToXy(j)
                    coords = coords[0]+30 , coords[3]-30
                    t = self.canvas.create_text(*coords, text = self.unicodePieces[i][k], font = (None, 30), tags = ("piece",i,k))
                    self.positions[tuple(j)] = [i,k]
    def getItemFromCoords(self, x, y):
        gridRef = self.xyToGridRef((x,y))
        return gridRef
    def gridRefToXy(self, gridRef):
        row, col = gridRef
        row = 8-int(row)
        col = string.ascii_lowercase.index(col) #Convert from letter to number
        r,c,s,o = row, col, 60, 30
        coords = [(s*c)+o,(s*r)+o,(s*(c+1))+o,(s*(r+1))+o]
        return coords
    def xyToGridRef(self, xy):
        s,o = 60,30
        c,r = [(xy[0]-o)//s,(xy[1]-o)//s]
        r = 8 - r
        gridRef = [str(r),string.ascii_lowercase[c]]
        return gridRef
    def numToGridRef(self, num):
        num[0], num[1] = str(num[0]), string.ascii_lowercase[num[1]]
        return num
    def gridRefToNum(self, grid):
        grid[1] = string.ascii_lowercase.index(grid[1])
        return [int(x) for x in grid]
    def checkPath(self, vect, startPos):
        start = list(startPos)
        coord = self.gridRefToNum(start)
        vect = vect[::-1] #Because grid refs are in the form [y,x]
        iterLen = max([abs(i) for i in vect]) - 1 #-1 because the end coord is not needed
        addCoords = []
        for n, c in enumerate(coord):
            v = vect[n]
            p = 1 if v >=0 else -1
            v = abs(v)
            r = (1,v+1)
            a = list(range(min(r),max(r))) if v != 0 else [0 for i in range(iterLen)]
            a = [i*p for i in a]
            addCoords.append(a)
        x,y = coord
        pathCoords = [[x+addCoords[0][n], y+addCoords[1][n]] for n in range(iterLen)]
        pathRefs = [self.numToGridRef(x) for x in pathCoords]
        pathCheck = len([self.positions[tuple(x)] for x in pathRefs if self.positions[tuple(x)] != "empty"]) == 0
        return pathCheck
    def canMove(self, change, piece, isAttacking):
        """
        Description:
        Determines whether to allow a piece to move to a target square
        
        Parameters:
        change - the change in coordinates from the current location to the new one, eg [30.0, -60.0]
        piece - the tuple containg the tkinter item for the piece, the colour and type and the location
        in the format (tk, ["w","p"], ["8","e"])
        isAttacking - if the target tile has a piece on it, extra check need to happen (bool)
        
        Explanation:
        The change in coordinates is converted to a vector representing the change in square in x and y.
        The movement vectors are checked based on the piece's movement limits,
        which determines the value of canMove.
        After the validity of the move is calculated, checkPath is then called to
        check there are no peices on the path the piece will take, except if the piece is a knight,
        because knights can jump over other pieces.
        If everything is ok, this function returns True and the piece can move.
        
        In short:
        1. checks vector to see if it is valid for that piece
        2. uses the vector to get all squares on the path to check they're clear
        """
        vect = [int(x/60) for x in change]
        vect[1] *= -1 
        pieceId = piece[1][1] #The type of piece, eg "k", "r", "kn"
        x,y = vect #Change in x and y
        canMove = False
        currentSquare = piece[2]
        if pieceId == "k": #One square, any direction
            if (abs(x) == 1 and y == 0) or (abs(y) == 1 and x == 0) or abs(x) == abs(y):
                canMove = True
            else:
                canMove = False
        elif pieceId == "q": #Any direction, straight line
            if abs(x) == abs(y): #If diagonal
                canMove = True
            elif (x == 0 and y != 0) or (y == 0 and x != 0):
                canMove = True
            else:
                canMove = False
        elif pieceId == "r": #Up, down, left, right any amount
            if (x == 0 and y != 0) or (y == 0 and x != 0):
                canMove = True
            else:
                canMove = False
        elif pieceId == "b": #Any diagonal, any length
            if abs(x) == abs(y):
                canMove = True
            else:
                canMove = False
        elif pieceId == "kn": #Up/down/left/right 2, left/right 1
            if (abs(x) == 1 and abs(y)) == 2 or (abs(x) == 2 and abs(y) == 1):
                canMove = True
            else:
                canMove = False
        elif pieceId == "p": #1-2 forward, diagonal when attacking
            if isAttacking:
                if piece[1][0] == "w":
                    if vect in [[1,1],[-1,1]]: #The valid diagonal moves for white pawns
                        canMove = True
                    else:
                        canMove = False
                if piece[1][0] == "b":
                    if vect in [[1,-1],[-1,-1]]: #The valid diagonal moves for black pawns
                        canMove = True
                    else:
                        canMove = False

            else:
                validMoves = [[0,1],[0,2]]
                if piece[2] in self.initialPositions: #On the first move only the piece can move 2 squares
                    if piece[1][0] == "w":
                        if vect in [[0,1],[0,2]]:
                            canMove = True
                        else:
                            canMove = False
                    if piece[1][0] == "b":
                        if vect in [[0,-1],[0,-2]]:
                            canMove = True
                        else:
                            canMove = False

                else:
                    if piece[1][0] == "w":
                        if vect in [[0,1]]:
                            canMove = True
                        else:
                            canMove = False
                    if piece[1][0] == "b":
                        if vect in [[0,-1]]:
                            canMove = True
                        else:
                            canMove = False
        if canMove and pieceId != "kn":
            if self.checkPath(vect, currentSquare):
                canMove = True
            else:
                canMove = False
        return canMove
        
    def clickHandle(self, event):
        if 30 < event.x < 510 and 30 < event.y < 510: #Only react to clicks within the board
            gridClicked = self.getItemFromCoords(event.x,event.y)
            item = self.canvas.find_closest(event.x, event.y)
            tags = self.canvas.gettags(item)
            value = self.positions[tuple(gridClicked)]
            if self.clickState:
                if value == "empty" or value[0] != self.clickedItem[1][0]: #Try and move/attack
                    isAttacking = value != "empty"
                    newCoords = self.gridRefToXy(gridClicked)[:2]
                    oldCoords = self.canvas.coords(self.clickedItem[0])
                    changeCoords = [x - oldCoords[i] + 30  for i, x in enumerate(newCoords)]
                    # [ This part checks if the path is valid                   ]       [Check a king isn't]  [ Checks thata when attacking the piece moves to the    ]
                    # [                                                         ]       [being captured    ]  [ other peice not the rectangle around it               ]
                    if self.canMove(changeCoords, self.clickedItem, isAttacking) and not value[1] == "k" and ((isAttacking and "rect" not in tags) or (not isAttacking)):
                        if isAttacking:
                            self.canvas.delete(item)
                        self.currentPlayer = "b" if self.currentPlayer == "w" else "w"
                        self.playerStatusColour.config(bg = {"w":"white","b":"black"}[self.currentPlayer])
                        self.canvas.move(self.clickedItem[0], *changeCoords)
                        self.canvas.itemconfig(self.clickedItem[0], fill = "black")
                        self.positions[tuple(gridClicked)] = self.positions[tuple(self.clickedItem[2])] #Fill new square
                        self.positions[tuple(self.clickedItem[2])] = "empty" #Empty previous square
                        self.clickState = False
                        self.update()
                    else:
                        self.clickState = False
                        self.canvas.itemconfig(self.clickedItem[0], fill = "red")
                        self.after(500, lambda: self.canvas.itemconfig(self.clickedItem[0], fill = "black"))
                else: #Deselect
                    self.clickState = False
                    self.canvas.itemconfig(self.clickedItem[0], fill = "black")
                    self.clickedItem = None
            else:
                if value[0] == self.currentPlayer and "piece" in self.canvas.gettags(item): #If it is the current player's piece
                    self.clickState = True #Waiting for place to go or to deselect
                    self.canvas.itemconfig(item, fill = "green")
                    self.clickedItem = [item, value, gridClicked]
                    
        
                    
        


app = Chess()
app.mainloop()
