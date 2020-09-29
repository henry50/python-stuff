from tkinter import *
import time
window = Tk()
#button functions
global key
    
def error():
    global err
    err = Tk()
    err.title("Error")
    err.geometry("500x50")
    errlab = Label(err, text="Calculator Error.")
    errlab.pack()
    errbtn = Button(err, text="Close", command=destroy)
    errbtn.pack()
    err.mainloop()

def destroy():
    err.destroy()
    window.destroy()

def operkey(key):
    global pre
    pre = disp.get()
    global prekey
    prekey = key
    disp.config(state=NORMAL)
    disp.delete(0, 'end')
    disp.insert(0, '0')
    disp.config(state='readonly')
    
def equalkey():
    post = disp.get()
    if prekey == "+":
        total = float(pre) + float(post)
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, total)
        disp.config(state = 'readonly')
    elif prekey == "-":
        total = float(pre) - float(post)
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, total)
        disp.config(state = 'readonly')

    elif prekey == "*":
        total = float(pre) * float(post)
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, total)
        disp.config(state = 'readonly')

    elif prekey == "/":
        total = float(pre) / float(post)
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, total)
        disp.config(state = 'readonly')
        
def deckey():
    val = disp.get()
    if val == '0':
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, '0.')
        disp.config(state='readonly')
    elif val != '0':
        ans = str(val)+"."
        print("dec:",ans)
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, str(ans))
        disp.config(state='readonly')

def clrkey():
    pre = 0
    prekey = 0
    key = 0
    disp.config(state=NORMAL)
    disp.delete(0, 'end')
    disp.insert(0, '0')
    disp.config(state='readonly')

def backey():
    val = disp.get()
    if len(val) == 1:
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, '0')
        disp.config(state='readonly')
    elif val == '0':
        donthng = 1
    elif len(val) > 1:
        cut = val[:-1]
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, cut)
        disp.config(state='readonly')

def pmkey():
    val = disp.get()
    val = int(val)
    if val+val == 0:
        pval = val+val+val
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, pval)
        disp.config(state='readonly')
    elif val-val == 0:
        nval = val-val-val
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, nval)
        disp.config(state='readonly')

def numkey(key):
    val = disp.get()
    if str(val) != '0':
        ans = (str(val) + key)
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, str(ans))
        disp.config(state='readonly')

    elif str(val) == '0':
        ans=key
        disp.config(state=NORMAL)
        disp.delete(0, 'end')
        disp.insert(0, str(ans))
        disp.config(state='readonly')

def setkey():
    setwin = Tk()
    setwin.title("Settings")
    setlab = Label(setwin, text="There are no settings, but here are some fun buttons")
    setlab.grid(column=0, row=0)
    sbtn2 = Button(setwin, text="Open error message", command=error)
    sbtn2.grid(column=0,row=1)

    setwin.mainloop()
    
    
def Zero():
    numkey(key="0")
def One():
    numkey(key="1")
def Two():
    numkey(key="2")
def Three():
    numkey(key="3")
def Four():
    numkey(key="4")
def Five():
    numkey(key="5")
def Six():
    numkey(key="6")
def Seven():
    numkey(key="7")
def Eight():
    numkey(key="8")
def Nine():
    numkey(key="9")
def Divide():
    operkey(key="/")
def Multiply():
    operkey(key="*")
def Minus():
    operkey(key="-")
def Add():
    operkey(key="+")
def Equal():
    equalkey()
def Dec():
    deckey()
def Clear():
    clrkey()
def Backspace():
    backey()
def PlusMinus():
    pmkey()
def Settings():
    setkey()
#display
disp = Entry(window, state='readonly', readonlybackground="white", )
disp.grid(column=0, row=0, columnspan=4, sticky=N+S+E+W)
disp.config(state=NORMAL)
disp.insert(0, 0)
disp.config(state='readonly')

#row 1
clear = Button(window, text="Clr", command=Clear)
clear.grid(column=0,row=1, sticky=N+S+E+W)

back = Button(window, text="<-", command=Backspace)
back.grid(column=1,row=1, sticky=N+S+E+W)

plusminus = Button(window, text="+/-", command=PlusMinus)
plusminus.grid(column=2,row=1, sticky=N+S+E+W)

settings = Button(window, text=u"\u2699", command=Settings)
settings.grid(column=3,row=1, sticky=N+S+E+W)

#row 2
seven = Button(window, text="7", command=Seven)
seven.grid(column=0,row=2, sticky=N+S+E+W)

eight = Button(window, text="8", command=Eight)
eight.grid(column=1,row=2, sticky=N+S+E+W)

nine = Button(window, text="9", command=Nine)
nine.grid(column=2,row=2, sticky=N+S+E+W)

divide = Button(window, text="÷", command=Divide)
divide.grid(column=3,row=2, sticky=N+S+E+W)

#row 3

four = Button(window, text="4", command=Four)
four.grid(column=0,row=3, sticky=N+S+E+W)

five = Button(window, text="5", command=Five)
five.grid(column=1,row=3, sticky=N+S+E+W)

six = Button(window, text="6", command=Six)
six.grid(column=2,row=3, sticky=N+S+E+W)

multiply = Button(window, text="×", command=Multiply)
multiply.grid(column=3,row=3, sticky=N+S+E+W)

#row 4

one = Button(window, text="1", command=One)
one.grid(column=0,row=4, sticky=N+S+E+W)

two = Button(window, text="2", command=Two)
two.grid(column=1,row=4, sticky=N+S+E+W)

three = Button(window, text="3", command=Three)
three.grid(column=2,row=4, sticky=N+S+E+W)

minus = Button(window, text="-", command=Minus)
minus.grid(column=3,row=4, sticky=N+S+E+W)

#row 5

zero = Button(window, text="0", command=Zero)
zero.grid(column=0,row=5, sticky=N+S+E+W)

dec = Button(window, text=".", command=Dec)
dec.grid(column=1,row=5, sticky=N+S+E+W)

equal = Button(window, text="=", command=Equal)
equal.grid(column=2,row=5, sticky=N+S+E+W)

add = Button(window, text="+", command=Add)
add.grid(column=3,row=5, sticky=N+S+E+W)

window.mainloop()
