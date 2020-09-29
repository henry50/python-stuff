import tkinter as tk
import random
import base64
import pygame, winsound #For playing sounds
import time
initDir = dir()
pygame.init()
pygame.mixer.init()
class hiddenRoot(tk.Tk):
    """This is a hidden window that makes the window appear on the taskbar"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes("-alpha", 0.0) #Transparent window
        self.bind("<FocusIn>", self.tlFocus) #When selected from taskbar, opens pacman window
        self.tlSet = False
    def setTl(self, item):
        self.tlSet = True
        self.tl = item
    def tlFocus(self, event):
        if self.tlSet:
            self.tl.focus_force()
        
           
""" --- TODO ---
Add fruit
2. Ghost AI (currently random movement) -not-really-complete

Smaller things:
One ghost is always stuck in the middle and sometimes one is stuck just outside

COMPLETED:
1. Ghosts -done
3. Power ups -complete (ghosts cant't be eaten, but the power up animations work)
3.5 Sound for all of the above (and below) complete for: dying, power up -complete
4. Levels/varying difficulty -complete
5. Lives/game ending -complete
Change collision detection - very laggy at the moment -important -complete
Add a ghost appearance change function -important -complete 
Encode pac.dat -easy -complete
Turn left at start (after READY!) -complete
If level finished when using power up, two lots of ghosts spawn -complete
Make the taskbar icon work as expected -med -sometimes-works -fixed
When using two power ups in one go, the score multiplier is reset -fixed
Ghosts flash before turning back -important -complete
"""
class Pacman(tk.Toplevel):
    """Pacman game"""
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.version = "1.1.0"
        self.overrideredirect(True) #Removes default Windows title bar
        self.focus_force() #Focus window
        self.height = 810 #Window height
        self.width = 730 #Window width
        ws = self.winfo_screenwidth()      ##
        hs = self.winfo_screenheight()      # This code (roughly) calculates how to centre the window
        x = int((ws/2) - (self.width/2))    #
        y = int((hs/2) - (self.height/2))  ##
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, x, y)) #Centre the window and fix it's height/width
        self.resizable(False,False) #Non-resizable
        self.config(bg = "black")
        #self.bind("<Configure>", self.disp)
        self.navBar = tk.Frame(self, bg = "black") #Custom title bar
        self.navBar.pack(fill = "x", padx = 10, pady = 10)
        self.mouseX, self.mouseY = 0, 0 #Track where the mouse is when the title bar is clicked
        self.navBar.bind("<Button-1>", self.storePosition) #Binds clicking and dragging of the title bar
        self.navBar.bind("<B1-Motion>", self.dragWindow)
        self.topIcon = tk.Canvas(self.navBar, height = 20, width = 20, highlightthickness = 0, bg = "black") #Title bar pacman icon
        self.topIcon.create_oval(0,0,20,20, fill="yellow")
        self.topIcon.create_arc(0,0,20,20, start=315, extent=90, fill="black")
        self.topIcon.pack(side = "left", padx = 10)
        self.topName = tk.Label(self.navBar, text = "PAC-MAN", fg = "white", bg = "black", font = ("System",12))
        self.topName.pack(side = "left")
        self.closeBtn = tk.Label(self.navBar, text = "X", fg = "red", bg = "black", font = ("System",12))
        self.closeBtn.bind("<Button-1>",lambda event: self.saveAndQuit())
        self.closeBtn.pack(side = "right")
        self.alreadyAbout = False #Prevents multiple about windows from being created
        self.topAbout = tk.Label(self.navBar, text = "?", fg = "white", bg = "black", font = ("System",12))
        self.topAbout.pack(side = "right", padx = 20)
        self.topAbout.bind("<Button-1>", lambda event: self.about())
        self.hztlRule = tk.Frame(self, height = 2, bg = "white")
        self.hztlRule.pack(fill = "x")
        #Score bar UI:
        self.scoreBar = tk.Frame(self, bg = "black")
        self.scoreBar.pack(fill = "both", padx = 40, pady = (10,0))
        self.scoreLabT = tk.Label(self.scoreBar, text = "1UP", bg = "black", fg = "white", font = ("System",12))
        self.scoreLabV = tk.Label(self.scoreBar, text = "00", bg = "black", fg = "white", font = ("System",12))
        self.scoreSpacer = tk.Frame(self.scoreBar, width = 100, bg = "black")
        self.hscoreLabT = tk.Label(self.scoreBar, text = "HIGH SCORE", bg = "black", fg = "white", font = ("System",12))
        self.hscoreLabV = tk.Label(self.scoreBar, text = "00", bg = "black", fg = "white", font = ("System",12))
        self.scoreLabT.grid(row = 0, column = 0, sticky = "w")
        self.scoreLabV.grid(row = 1, column = 0, sticky = "e")
        self.scoreSpacer.grid(row = 0, column = 1, rowspan = 2)
        self.hscoreLabT.grid(row = 0, column = 2, sticky = "w")
        self.hscoreLabV.grid(row = 1, column = 2, sticky = "e")
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg = "black")
        self.canvas.pack(fill = "both", expand = True, padx = 10)
        self.startSound = pygame.mixer.Sound(r".\audio\game_start.wav") #Loads starting sound
        self.eatSnd1 = pygame.mixer.Sound(r".\audio\munch_1.wav") #Loads eating sound 1
        self.eatSnd2 = pygame.mixer.Sound(r".\audio\munch_2.wav") #Loads eating sound 2
        self.deathSound = pygame.mixer.Sound(r".\audio\death.wav") #Loads death sound
        self.altEat = 0 #Aleternates eating sound effect
        #Grid coords of walls
        self.wallCoords = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [8, 0], [7, 0], [9, 0], [11, 0], [12, 0], [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [19, 0], [18, 0], [20, 0], [21,0], [0, 2], [0, 1], [2, 2], [2, 3], [2, 4], [2, 6], [3, 6], [2, 7], [3, 7], [2, 8], [3, 8], [2, 9], [3, 9], [0, 3], [0, 5], [0, 4], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 13], [0, 12], [0, 15], [0, 14], [0, 17], [0, 16], [0, 18], [0, 19], [0, 20], [0, 22], [0, 21], [2, 22], [1, 22], [3, 22], [4, 22], [5, 22], [6, 22], [7, 22], [8, 22], [9, 22], [21, 22], [20, 22], [19, 22], [18, 22], [17, 22], [13, 22], [11, 22], [12, 22], [14, 22], [16, 22], [15, 22], [21, 21], [21, 19], [21, 20], [21, 18], [21, 17], [21, 16], [21, 14], [21, 15], [21, 12], [21, 13], [21, 11], [21, 10], [21, 9], [21, 5], [21, 8], [21, 6], [21, 7], [21, 4], [21, 3], [21, 1], [21, 2], [1, 11], [0, 11], [2, 11], [3, 11], [2, 13], [3, 13], [3, 14], [2, 14], [2, 15], [3, 15], [3, 16], [2, 16], [2, 18], [2, 19], [2, 20], [5, 2], [4, 3], [4, 4], [4, 2], [5, 3], [5, 4], [5, 6], [6, 6], [7, 6], [8, 6], [9, 6], [7, 7], [7, 8], [7, 9], [7, 11], [6, 11], [5, 11], [5, 10], [5, 9], [5, 8], [5, 12], [5, 13], [5, 14], [4, 18], [4, 19], [4, 20], [5, 20], [5, 18], [5, 19], [5, 16], [6, 16], [7, 16], [8, 16], [9, 16], [7, 15], [9, 10], [9, 12], [9, 13], [9, 14], [10, 14], [11, 14], [9, 8], [10, 8], [9, 9], [11, 8], [11, 9], [11, 10], [11, 13], [11, 12], [11, 11], [7, 2], [7, 1], [7, 3], [7, 4], [8, 4], [9, 3], [9, 4], [9, 2], [9, 1], [11, 1], [11, 3], [11, 2], [11, 4], [12, 4], [13, 4], [13, 3], [13, 2], [13, 1], [17, 1], [15, 2], [15, 3], [15, 4], [16, 3], [16, 4], [17, 4], [17, 3], [17, 6], [18, 6], [19, 6], [19, 5], [19, 4], [19, 3], [19, 2], [19, 7], [19, 8], [19, 9], [19, 11], [18, 11], [17, 11], [13, 8], [13, 10], [13, 9], [13, 11], [13, 12], [13, 14], [13, 13], [14, 11], [15, 11], [17, 10], [17, 8], [17, 9], [17, 12], [17, 13], [17, 14], [15, 6], [15, 7], [15, 8], [15, 9], [13, 6], [12, 6], [11, 6], [11, 16], [12, 16], [13, 16], [15, 13], [15, 14], [15, 15], [15, 16], [16, 18], [15, 18], [17, 18], [19, 13], [19, 14], [19, 15], [19, 16], [18, 16], [17, 16], [19, 17], [19, 18], [19, 19], [19, 20], [17, 21], [17, 19], [16, 19], [15, 19], [15, 20], [13, 21], [13, 20], [13, 18], [13, 19], [12, 18], [11, 18], [11, 19], [11, 20], [11, 21], [9, 21], [9, 19], [9, 18], [9, 20], [8, 18], [7, 18], [7, 19], [7, 21], [7, 20], [7, 14], [7, 13], [12, 19], [12, 20], [12, 21], [8, 21], [8, 20], [8, 19], [8, 1], [8, 2], [8, 3], [12, 1], [12, 2], [12, 3]]
        self.wallCoords = [[x[1],x[0]] for x in self.wallCoords] #The wall coords were recorded the wrong way round, so this fixes it
        self.usedCoords = list(self.wallCoords) #List that stores the coords in use
        self.bridges = [[0,10],[22,10]] #Coords of teleports
        self.foodCoords = [] #Stores coords of food
        self.eatenCoords = [] #Stores coords of eaten food and power ups
        self.powerUpCoords = [[1,2],[21,2],[1,16],[21,16]] #Coords of power ups
        self.powerUpState = "orange"
        self.powerUpActive = False
        #Coords of area around ghost area where food doesn't spawn
        self.excludeFood = [[7,8],[8,8],[9,8],[10,8],[11,8],[12,8],[13,8],[14,8],[15,8],[15,9],[15,10],[15,11],[15,12],[14,12],[13,12],[12,12],[11,12],[10,12],[9,12],[8,12],[7,12],[7,11],[7,10],[7,9]]
        self.ghostGate = [11,9] #Coords of ghost spawn area gate
        self.ghostArea = [[11,9],[9,10],[10,10],[11,10],[12,10],[13,10]] #Coords of ghost spawn area
        self.ghostSpawn = {"blinky":[11,8],"pinky":[11,10],"inky":[10,10],"clyde":[12,10]}
        self.ghostColour = {"blinky":"red","pinky":"pink","inky":"turquoise","clyde":"orange"}
        self.ghosts = ["blinky","pinky","inky","clyde"]
        self.ghostCount = 0
        self.ghostDirection = {"blinky":"left","pinky":"up","inky":"right","clyde":"left"}
        self.ghostEatenCoords = {"blinky":None,"pinky":None,"inky":None,"clyde":None}
        self.ghostCoords = dict(self.ghostSpawn)
        self.eatingGhost = False
        self.ghostFlashState = 0
        self.flashActivated = False
        #This loads the image files and stores them in such a way that they are not forgotten by the program
        root.gi1 = tk.PhotoImage(file = r".\images\ghost_blinky.gif")
        root.gi2 = tk.PhotoImage(file = r".\images\ghost_inky.gif")
        root.gi3 = tk.PhotoImage(file = r".\images\ghost_pinky.gif")
        root.gi4 = tk.PhotoImage(file = r".\images\ghost_clyde.gif")
        root.gi5 = tk.PhotoImage(file = r".\images\ghost_scared.gif")
        root.gi6 = tk.PhotoImage(file = r".\images\ghost_flash.gif")
        self.ghost_blinky = root.gi1
        self.ghost_inky = root.gi2
        self.ghost_pinky = root.gi3
        self.ghost_clyde = root.gi4
        self.ghost_scared = root.gi5
        self.ghost_flash = root.gi6
        #These are the coordinates on a 16x16 grid for the different parts of the ghost, which are then scaled (roughly) to 30x30 (grid box size)
        self.score = 0
        self.lives = 3
        self.moving = False
        self.started = False
        self.pacDying = False #So pacman can't die multiple times at once
        self.direction = "left"
        self.ignoreKey = True
        self.bind("<Key>", self.key) #WASD/arrow key binding
        self.protocol("WM_DELETE_WINDOW", self.saveAndQuit) #Saves and quits when window is closed
        self.highScore = 0                             ##
        self.loadHighScore()                            # Stores, loads and displays high score
        self.hscoreLabV.config(text = self.highScore)  ##
        self.draw() #Draws game
        self.createPac() #Draws pacman
        self.drawFood() #Draws food and power ups
        self.constantMotion() #Starts constant motion of pacman
        self.start()
        self.createGhosts()
        self.moveRandom()
    def start(self):
        self.update()
        #self.playStartSound()
        winsound.PlaySound(r".\audio\game_start.wav", winsound.SND_FILENAME) #Plays the intro sound
        self.canvas.itemconfig("text", text = "")
        self.ignoreKey = False
        pygame.mixer.music.load(r".\audio\siren_1.wav") #Loops the background siren
        pygame.mixer.music.play(-1) #Play it infinitely
        self.removeLife()
        self.moving = True
        self.started = True
    def playStartSound(self):
        self.startSound.play()
        while pygame.mixer.get_busy():
            continue
    def about(self):
        if not self.alreadyAbout:
            self.alreadyAbout = True
            self.aboutTl = tk.Toplevel(self)
            self.aboutTl.overrideredirect(True)
            self.aboutTl.config(bg = "black")
            self.aboutTl.bind("<FocusOut>", lambda event: self.aboutClose())
            self.aboutTl.focus_force()
            rootx = self.winfo_x() # X position of main window
            rooty = self.winfo_y() # Y position
            rootw = self.winfo_width() #Width
            rooth = self.winfo_height() #and height of main window
            #Centres the toplevel in the root window and subtracts half the size of the toplevel (100) to centre it
            x = int(rootx+(rootw/2)) - 250   # Calculates where to postion toplevel
            y = int(rooty + (rooth/2)) - 150
            self.aboutTl.geometry("500x300+{}+{}".format(x, y)) #Centre the window and fix it's height/width
            self.aboutFrm = tk.Frame(self.aboutTl, highlightthickness = 2, highlightbackground = "white", bg = "black")
            self.aboutFrm.pack(expand = True, fill = "both")
            self.aboutNav = tk.Frame(self.aboutFrm, bg = "black")
            self.aboutNav.pack(fill = "x", padx = 10, pady = 10)
            self.aboutIco = tk.Label(self.aboutNav, text = "?", fg = "white", bg = "black", font = ("System",12))
            self.aboutIco.pack(side = "left")
            self.aboutName = tk.Label(self.aboutNav, text = "About", fg = "white", bg = "black", font = ("System",12))
            self.aboutName.pack(side = "left", padx = 10)
            self.aboutCls = tk.Label(self.aboutNav, text = "X", fg = "red", bg = "black", font = ("System",12))
            self.aboutCls.bind("<Button-1>",lambda event: self.aboutClose())
            self.aboutCls.pack(side = "right")
            self.aboutRule = tk.Frame(self.aboutFrm, height = 2, bg = "white")
            self.aboutRule.pack(fill = "x")
            self.aboutTitle = tk.Label(self.aboutFrm, text = "PAC-MAN", fg = "white", bg = "black", font = ("System",24))
            self.aboutTitle.pack(pady = (5,0))
            self.aboutVersion = tk.Label(self.aboutFrm, text = "Version {}".format(self.version), fg = "white", bg = "black", font = ("System",12))
            self.aboutVersion.pack()
            cred = "Credits:\nCreated by Henry Lunn, ©2020\nPAC-MAN™ & ©1980 BANDAI NAMCO Entertainment Inc.\n\nSound files:\nNearly all: https://www.sounds-resource.com/arcade/pacman/sound/10603/\nDeath sound effect: http://www.orangefreesounds.com/pacman-death-sound/"
            self.aboutCredits = tk.Label(self.aboutFrm, text = cred, bg = "black", fg = "white", font = ("System",12), wrap = 450)
            self.aboutCredits.pack(pady = (20,0))
    def aboutClose(self):
        self.alreadyAbout = False
        self.aboutTl.destroy()
    def gridToXy(self, g):
        """Converts grid coordinates to tkinter x,y coordinates"""
        x,y = g
        x1,y1 = (x*30)+10,(y*30)+10
        x2,y2 = x1+30, y1+30
        return (x1,y1,x2,y2)
    def resizeXy(self, coords, size):
        """Resizes whole box cooridnates to smaller, scaled down boxes"""
        x1,y1,x2,y2 = coords
        if size == 0: #small
            scale = 12 #smaller by 12 on each side
        elif size == 1: #power up
            scale = 8
        elif size == 2: #lives indicator
            scale = 3
        x1,y1,x2,y2 = x1+scale,y1+scale,x2-scale,y2-scale
        return (x1,y1,x2,y2)
    def saveAndQuit(self):
        pygame.quit() #Stop all sounds
        with open("pac.dat","w") as f:
            f.write(base64.b64encode("high_score:{}".format(str(self.highScore)).encode()).decode()) #Saves obfuscated string
        self.master.destroy()
    def loadHighScore(self):
        try:
            open("pac.dat")
        except:
            new = True
        else:
            new = False
        if not new:
            f = open("pac.dat","r")
            if len(f.read()) == 0:
                new = True
        if new:
            f = open("pac.dat","w")
            f.write("aGlnaF9zY29yZTow")
            f.close()
        f = open("pac.dat","r")
        fd = base64.b64decode(f.read().encode()).decode().splitlines() #Decodes obfuscated string
        fdict = {y.split(":")[0]:y.split(":")[1] for y in fd}
        self.highScore = int(fdict["high_score"])
    def storePosition(self, e):
        #Collects info about mouse position when dragging the window
        x = self.winfo_x()
        y = self.winfo_y()
        sx = e.x_root
        sy = e.y_root
        self.mouseX = x - sx
        self.mouseY = y - sy
    def dragWindow(self, e):
        #Moves window when dragged
        self.geometry("+{}+{}".format(e.x_root+self.mouseX, e.y_root+self.mouseY))
    def key(self, event): #Handles the keypress events
        keyDict = {37:"left",38:"up",39:"right",40:"down",65:"left",87:"up",68:"right",83:"down"}
        if event.keycode in list(keyDict.keys()) and not self.ignoreKey:
            newDirection = keyDict[event.keycode]
            if self.canTurn(newDirection, "pac"):
                self.direction = newDirection
    def canTurn(self, ndir, what):
        """Checks to see if pacman can turn (if there is a wall/ghost area there or not"""
        gridDict = {"up":(0,-1),"down":(0,1),"left":(-1,0),"right":(1,0)}
        if what == "pac":
            newLoc = self.addCoords(self.pacLoc, gridDict[ndir])
            if newLoc in self.wallCoords + self.ghostArea:
                return False
            else:
                return True
        else:
            newLoc = self.addCoords(self.ghostCoords[what], gridDict[ndir])
            if newLoc in self.wallCoords:
                return False
            else:
                return True
            
    def move(self, d, what): #Controls the movement of pacman and ghosts
        if what == "pac":
            self.ignoreKey = False
        gridDict = {"up":(0,-1),"down":(0,1),"left":(-1,0),"right":(1,0)}
        xyDict = {"up":(0,-30),"down":(0,30),"left":(-30,0),"right":(30,0)}
        faceDict = {"up":"n","down":"s","left":"w","right":"e"}
        if what == "pac":
            self.canvas.tag_raise("pac") #Keep pacman on top of other items
            newLoc = self.addCoords(self.pacLoc, gridDict[d])
            self.facing = faceDict[d]
            self.moveMouth(False)
        else:
            oldLoc = self.ghostCoords[what]
            newLoc = self.addCoords(oldLoc, gridDict[d])
        if (newLoc == [0,10] and d == "left") or (newLoc == [22,10] and d == "right"):
            newLoc, pacXy = self.teleport(newLoc, d)
            self.ignoreKey = True
        else:
            pacXy = xyDict[d]
        if newLoc not in self.wallCoords:# and newLoc not in self.ghostArea: #Checks pacman can move to this square
            cont = True
            if what != "pac":
                if newLoc in list(self.ghostCoords.values()):
                    cont = False
                if newLoc in self.ghostArea:
                    if oldLoc in self.ghostArea:
                        cont = True
                    else:
                        cont = False
            if cont:
                self.canvas.move(what,*pacXy) #Visually moves pacman
                if what == "pac":
                    self.pacLoc = newLoc
                    self.checkCollisions(True)
                else:
                    self.ghostCoords[what] = newLoc
                    self.checkCollisions(False)
            
    def checkCollisions(self, isPac):
        """Checks for collision of pacman with food and ghosts"""
        if isPac and self.pacLoc in self.foodCoords + self.powerUpCoords:
            #These things only need to be done if it is pacman moving
            #This part visually removes items from the canvas
            items = self.canvas.find_overlapping(*self.gridToXy(self.pacLoc))
            for item in items:
                itemTag = self.canvas.gettags(item)[0]
                if itemTag == "food":
                    self.canvas.delete(item)
                    self.addScore(10)
                elif itemTag == "power":
                    self.canvas.delete(item)
                    self.addScore(50)
            #This part does the actions associated with the item
            if self.pacLoc not in self.eatenCoords:
                if self.pacLoc in self.foodCoords: #If the item if food
                    self.eatenCoords.append(self.pacLoc)
                    if not pygame.mixer.get_busy():
                        self.altEat = 1 if self.altEat == 0 else 0
                        if self.mouthState == 0:
                            self.eatSnd2.play()
                        else:
                            self.eatSnd1.play()
                elif self.pacLoc in self.powerUpCoords: #If the item is a power up
                    self.eatenCoords.append(self.pacLoc)
                    self.powerUp()
            if len(self.canvas.find_withtag("food")) == 0 and len(self.canvas.find_withtag("power")) == 0:
                self.levelCleared()
        if self.pacLoc in list(self.ghostCoords.values()):
            if self.powerUpActive:
                for i in self.canvas.find_overlapping(*self.gridToXy(self.pacLoc)):
                    tags = [x for x in self.canvas.gettags(i) if x in self.ghosts]
                    if len(tags) != 0:
                        ghost = [x for x in self.canvas.gettags(i) if x in self.ghosts][0]
                        if not self.eatingGhost:
                            self.eatingGhost = True
                            self.eatGhost(ghost)
            else:
                self.pacDied()
    def removeLife(self):
        oldLives = self.lives
        self.lives -= 1
        if self.lives == -1:
            self.gameOver()
            return False
        else:
            self.canvas.delete("life{}".format(str(oldLives)))
            return True
    def pacDied(self):
        if not self.pacDying:
            self.pacDying = True
            self.facing = "n"
            self.moveMouth(False)
            self.moving = False
            self.deleteGhosts()
            self.animationList = [(22.5, 135),(0,180),(337.5,225),(315,270),(0,359)]
            pygame.mixer.music.pause()
            channel = pygame.mixer.find_channel(True)
            channel.set_volume(0.3) #Makes death sound quieter, because it was louder than the other sounds
            channel.play(self.deathSound)
            self.deathAniCount = 0
            self.animationFinished = False
            self.deathAnimation()
    def pacDiedCont(self):
        self.canvas.delete("pac")
        self.update()
        if self.removeLife():
            self.after(1000, self.respawn)
    def delayedRespawn(self):
        self.canvas.itemconfig("text", text = "")
        self.createGhosts()
        pygame.mixer.music.unpause()
        self.pacDying = False
        self.moving = True
        self.facing = "w"
        self.moveMouth(False)
    def respawn(self):
        self.ghostCoords = dict(self.ghostSpawn)
        self.createPac()
        self.canvas.itemconfig("text", text = "READY!")
        root.after(2000, self.delayedRespawn)
    def deathAnimation(self):
        try:
            s, e = self.animationList[self.deathAniCount]
            self.canvas.itemconfig(self.pacMouth, start = s, extent = e, outline = "black")
            self.update()
            self.deathAniCount += 1
        except:
            self.pacDiedCont()
        else:
            root.after(200, self.deathAnimation)
    def flashWall(self):
        if self.flashWallCount <= 4:
            self.altFill = "#141483" if self.altFill == "white" else "white"            
            for i in self.canvas.find_withtag("wall"):
                    self.canvas.itemconfig(i, fill = self.altFill)
            self.flashWallCount += 1
            self.after(500, self.flashWall)
    def levelClearedDelayed(self):
        self.canvas.delete("pac")
        self.drawFood()
        self.canvas.tag_lower("food")
        self.respawn()
    def levelCleared(self):
        self.moving = False
        self.eatenCoords = []
        pygame.mixer.music.pause()
        self.deleteGhosts()
        self.canvas.itemconfig(self.pacMouth, start=360, extent=0, outline = "yellow") # Make full yellow circle
        self.altFill = "white"
        self.flashWallCount = 0
        self.flashWall()
        root.after(3000, self.levelClearedDelayed)                 
    def nextSquare(self, d, what):
        gridDict = {"up":(0,-1),"down":(0,1),"left":(-1,0),"right":(1,0)}
        oldLoc = self.ghostCoords[what]
        newLoc = self.addCoords(oldLoc, gridDict[d])
        if newLoc in self.wallCoords+list(self.ghostCoords.values()):
            return False
        else:
            return True
    def gameOver(self):
        pygame.mixer.music.stop()
        self.canvas.itemconfig("text", fill = "red", text = "GAME\tOVER")
    def addScore(self, n):
        self.score += n
        self.scoreLabV.config(text = str(self.score).zfill(2))
        if self.score > self.highScore:
            self.highScore = self.score
            self.hscoreLabV.config(text = str(self.score).zfill(2))
    def deleteGhosts(self):
        for i in self.canvas.find_withtag("ghost"):
            self.canvas.delete(i)
            self.ghostCount -= 4
    def endEat(self):
        self.eatingGhost = False
        self.moving = True
        self.canvas.delete("ghost_text")
        self.canvas.itemconfig("pac_body", fill = "yellow")
    def eatGhost(self, ghost):
        self.moving = False
        self.ghostsEaten += 1
        points = (2**self.ghostsEaten) * 100
        self.addScore(points)
        coords = [x + 15 for x in self.gridToXy(self.ghostCoords[ghost])[:2]]
        self.canvas.itemconfig("pac", fill = "black", outline = "black")
        self.canvas.create_text(*coords, text = str(points), fill = "teal", tag = "ghost_text", font = ("System",12))
        self.canvas.delete(ghost)
        self.ghostCount -= 1
        self.ghostEatenCoords[ghost] = self.ghostSpawn[ghost]
        self.after(500, self.endEat)
    def flashGhosts(self):
        self.ghostFlashState = 1 if self.ghostFlashState == 0 else 0
        img = [self.ghost_scared, self.ghost_flash]
        for i in self.ghosts:
            self.canvas.itemconfig("ghost", image = img[self.ghostFlashState])
    def powerUpEnd(self):
        timePassed = (time.time() - self.powerUpStart)
        if timePassed > 5.5:
            self.flashGhosts()
        if timePassed < 10:
            self.after(300, self.powerUpEnd)
        else:
            self.powerUpActive = False
            self.deleteGhosts()
            for k,v in self.ghostEatenCoords.items(): #Move dead ghosts to spawn
                if v != None:
                    self.ghostCoords[k] = v
            self.createGhosts()
            self.ghostEatenCoords = {"blinky":None,"pinky":None,"inky":None,"clyde":None}
            pygame.mixer.music.stop()
            pygame.mixer.music.load(r".\audio\siren_1.wav") #Loops the background siren again
            pygame.mixer.music.play(-1)
    def powerUp(self):
        if not self.powerUpActive:
            self.powerUpActive = True
            self.ghostsEaten = 0
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r".\audio\power_pellet.wav") #Loops the power up background sound
        pygame.mixer.music.play(-1)
        for i in self.ghosts:
            self.canvas.itemconfig("ghost", image = self.ghost_scared)
        self.powerUpStart = time.time()
        self.powerUpEnd()
    def teleport(self, coords, d): #Allows pac to travel from either side of the map to the other
        if coords == [22,10]:
            newLoc = [0,10]
            pacXy = (-630,0)
        elif coords == [0,10]:
            newLoc = [22,10]
            pacXy = (630, 0)
        return (newLoc, pacXy)
                
    def constantMotion(self): #The mainloop, which makes pacmna and the ghosts move
        if self.moving:
            self.move(self.direction, "pac")
            for i in self.ghosts:
                self.move(self.ghostDirection[i], i)
                self.moveRandom()
            self.flashPowerUp()
            self.canvas.tag_lower("food")
        self.after(150, self.constantMotion)
    def moveMouth(self, after):
        #Moves the mouth to make it look like pacman has changed direction
        if self.moving:
            self.mouthState = 0 if self.mouthState == 1 else 1
            #These are the start and extent values for the mouth.
            #These specify the start and size of the mouth angles, eg (330,60)
            #Starts at 330 degrees and draws and arc 60 degrees from there.
            #When they are rotated, the start values are changed by 90 degrees.
            mouthPositions = {"n":[(45,90),(90,0)], #Rotate arc north
                              "e":[(315,90),(360, 0)], #// east
                              "s":[(225,90),(270,0)], #// south
                              "w":[(135,90),(180,0)]} #//west
            s,e = mouthPositions[self.facing][self.mouthState]
            outline = "yellow" if e == 0 else "black"
            self.canvas.itemconfig(self.pacMouth, start = s, extent = e, outline = outline)
        if not self.started:
            self.after(10, lambda: self.moveMouth(True))
    def test_highlight_square(self,coords): #Test function to see where a coordinate is
        coords = self.gridToXy(coords)
        self.canvas.create_rectangle(*coords, fill = "red")
    def createPac(self): #Creates pacman
        spawnPos = [11, 16]
        self.pacLoc = spawnPos
        self.usedCoords.append(spawnPos)
        coord = self.gridToXy(spawnPos)
        self.canvas.create_oval(coord, fill="yellow", tags = ("pac","pac_body"))
        self.pacMouth = self.canvas.create_arc(coord, start=360, extent=0, fill="black", tags = ("pac","pac_mouth"), outline = "yellow")
        self.mouthState = 0
        self.facing = "e"
        self.moveMouth(True)
    def nextDirection(self, d): #Gets direction 90 degrees clockwise to current direction
        return {"left":"up","up":"right","right":"down","down":"left"}[d]
    def createGhosts(self): #Draws the ghosts
        imageDict = {"blinky":self.ghost_blinky,"pinky":self.ghost_pinky,"inky":self.ghost_inky,"clyde":self.ghost_clyde}
        if self.ghostCount <= 4:
            for i in self.ghosts:
                self.canvas.create_image(*[x+15 for x in self.gridToXy(self.ghostCoords[i])[:2]], image=imageDict[i], tags = ("ghost",i))
            self.ghostCount += 4
    def isOppositeDirection(self, old, new): #Checks if the new direction is opposite the old one
        oppDict = {"up":"down","left":"right","right":"left","down":"up"}
        if oppDict[old] == new:
            return True
        else:
            return False
    def moveRandom(self):
        if self.moving:
            for i in list(self.ghostSpawn.keys()):
                if not self.nextSquare(self.ghostDirection[i], i):
                    currentDir = self.ghostDirection[i]
                    choices = ["up","down","left","right"]
                    choices.remove(currentDir)
                    newDir = random.choice(choices)
                    if not self.isOppositeDirection(currentDir, newDir):
                        self.ghostDirection[i] = newDir
                    else:
                        self.ghostDirection[i] = self.nextDirection(newDir)
    def flashPowerUp(self):
        self.powerUpState = "orange" if self.powerUpState == "black" else "black"
        for i in self.canvas.find_withtag("power"):
            self.canvas.itemconfig(i, fill = self.powerUpState)
    def drawFood(self):
        for coord in self.powerUpCoords:
            xy = self.gridToXy(coord)
            rxy = self.resizeXy(xy, 1)
            self.canvas.create_oval(*rxy, fill = "orange", tag = "power")
        for row in range(22):
            for col in range(22):
                s = [col,row]
                if s not in [[11,16]] + self.wallCoords + self.bridges + self.powerUpCoords + self.ghostArea + self.excludeFood: #Food can't spawn in these coordinates
                    self.foodCoords.append(s)
                    xy = self.gridToXy(s)
                    rxy = self.resizeXy(xy,0)
                    self.canvas.create_oval(*rxy, fill = "orange", tag = "food")
    def border(self, coords, dirs, special=None, sType = None):
        """Creates a border for a box given coords and sides to border"""
        x1,y1,x2,y2 = coords
        x1,y1,x2,y2 = [x for x in coords]
        dirDict = {"b":[x1,y2,x2,y2],"l":[x1,y1,x1,y2],"r":[x2,y1,x2,y2],"t":[x1,y1,x2,y1]} #Calculates which coords need to be used to create border
        if not special:
            for d in dirs:
                self.canvas.create_line(*dirDict[d], fill = "#141483", width = 2, tag = "wall")
        elif sType == "gate":
            self.canvas.create_line(*dirDict[dirs], fill = "white", width = 3, tag = "gate")
    def addCoords(self, a, b):
        """Adds coords a and b and returns the result"""
        return [x + b[i%2] for i, x in enumerate(a)]
    def wallSurround(self, coords):
        """Returns the sides of a square that aren't adjacent to walls"""
        s = {(1, 0):"r", (-1, 0):"l", (0, 1):"b", (0, -1):"t"}
        match = [s[x] for x in list(s.keys()) if self.addCoords(coords,x) not in self.wallCoords]
        return match
    def disp(self, event = None):
        print("{}x{}".format(self.winfo_height(),self.winfo_width()))
    def draw(self): #Generates the walls
        boxHeight = 30
        boxWidth = 30
        for col in range(23):
            for row in range(22):
                coords = [col,row]
                xy = self.gridToXy(coords)
                if coords in self.wallCoords: #If the coord is a wall, draw it's borders
                    self.border(xy, self.wallSurround(coords))
        self.border(self.gridToXy(self.ghostGate),"t",True,"gate") #Ghost area gate
        txtCoords = [x + 15 for x in self.gridToXy([11,12])[:2]] #Below ghost area, centred
        self.canvas.create_text(txtCoords, text = "READY!", fill = "yellow", font = ("System",12), tag = "text")
        lifeCoords = [[0,22.2],[1.2,22.2],[2.4,22.2]]
        for x in range(1,4):
            i = x-1
            coord = self.resizeXy(self.gridToXy(lifeCoords[i]), 2)
            self.canvas.create_oval(coord, fill="yellow", tag = "life{}".format(str(x)))
            self.canvas.create_arc(coord, start=315, extent=90, fill="black", tag = "life{}".format(str(x)))
root = hiddenRoot() #This window is what appears on the taskbar
root.lower()    # The window is hidden from view
root.iconify()
root.title("Pacman") #Name to display on taskbar
root.iconbitmap(r"./images/pac.ico")
import ctypes
appid = "pacman.game" # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid) #This gives the game it's own icon
app = Pacman(root) #Actual pacman window created as child of hidden root
root.setTl(app) #Tells the hidden root what to show when it's taskbar icon is clicked
app.mainloop() #Starts the tkinter mainloop

endDir = dir()
varDict = {}
for x in [y for y in endDir if y not in initDir]:
	varDict[x] = type(x).__name__

print(varDict)
#print(endDir)

