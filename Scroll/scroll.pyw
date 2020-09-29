import tkinter as tk
import random
root = tk.Tk()
root.title("Scroll")
root.state("zoomed")
score = 0
col = lambda: random.randint(0,255)
def randCol():
    r,g,b = col(),col(),col()
    rcol = "#{:02X}{:02X}{:02X}".format(r,g,b)
    scoreLab.config(fg = rcol)
##    if (r*r*0.241 + g*g*0.691 + b*b*0.068)**0.5 >= 210:
##        scoreLab.config(bg = "#C0C0C0")
##    else:
##        scoreLab.config(bg = "#F0F0F0")
def scroll(event=None):
    global score
    score += 1
    if score % 20 == 0:
        randCol()
    scoreLab.config(text = str(score))
scoreLab = tk.Label(root, text = "0", font = (None,"36"))
scoreLab.place(relx = 0.5, rely = 0.5, anchor = "center")
root.bind("<MouseWheel>", scroll)
root.mainloop()
