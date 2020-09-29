from tkinter import *
from datetime import datetime
import os

window = Tk()
window.title("Binary Clock")
window.configure(background='black')
window.iconbitmap(os.getcwd()+"\\icon.ico")
title = Label(window, text="Binary Clock", fg="white", bg="black", font=("Courier", 30))

whrsl = Label(window, text="Hour:", fg="white", bg="black", font=("Courier", 30))
whrs = Label(window, text="00000000", fg="white", bg="black", font=("Courier", 30))

wminl = Label(window, text="Minute:", fg="white", bg="black", font=("Courier", 30))
wmin = Label(window, text="00000000", fg="white", bg="black", font=("Courier", 30))

wsecl = Label(window, text="Second:", fg="white", bg="black", font=("Courier", 30))
wsec = Label(window, text="00000000", fg="white", bg="black", font=("Courier", 30))
#binar = "{0:08b}".format(bina)
title.grid(column = 0, row = 0, columnspan = 2)

whrsl.grid(column = 0, row = 1)
whrs.grid(column = 1, row = 1)

wminl.grid(column = 0, row = 2)
wmin.grid(column = 1, row = 2)

wsecl.grid(column = 0, row = 3)
wsec.grid(column = 1, row = 3)


def uHrs():
    now = datetime.now()
    hrs = now.hour
    binh = "{0:08b}".format(hrs)
    whrs.configure(text=binh)
    whrs.after(200, uHrs)
def uMin():
    now = datetime.now()
    mins = now.minute
    binm = "{0:08b}".format(mins)
    wmin.configure(text=binm)
    wmin.after(200, uMin)
def uSec():
    now = datetime.now()
    sec = now.second
    bins = "{0:08b}".format(sec)
    wsec.configure(text=bins)
    wsec.after(200, uSec)
uHrs()
uMin()
uSec()
window.mainloop()
