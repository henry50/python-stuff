from tkinter import *
window = Tk()
window.title("Number Adder")

def check():
    ansent.config(state=NORMAL)
    ans = int(num1.get()) + int(num2.get())
    ansent.delete(0, 'end')
    ansent.insert(0, ans)
    ansent.config(state=DISABLED)

title1 = Label(window, text="Number Adder")
title1.grid(column=3, row=0)

num1 = Entry(window)
num1.grid(column=1, row=1)

addlab = Label(window, text="+")
addlab.grid(column=2, row=1)

num2 = Entry(window)
num2.grid(column=3, row=1)

equal = Label(window, text="=")
equal.grid(column=4, row=1)

ansent = Entry(window, disabledbackground="white", disabledforeground="black")
ansent.grid(column=5, row=1)

btn = Button(window, text="Add", command=check)
btn.grid(column=3, row=2)




window.mainloop()

