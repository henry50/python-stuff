import tkinter
from datetime import datetime
from datetime import date
import calendar
import time
window = tkinter.Tk()
window.title("Clock")
window.wm_iconbitmap('clockicon.ico')
window.geometry("200x50")
now = datetime.now()
yy = now.year
mm = now.month
dd = now.day
findday = date.today()
dow =calendar.day_name[findday.weekday()]
clock = tkinter.Label(window)
clock.pack()
def tick():
    time1 = time.strftime('%H:%M:%S')
    clock.configure(text = time1)
    clock.after(200, tick)
tick()
month = ['', 'January', 'February','March','April','May','June','July','August','September','October','November','December']
m = now.month
m = m
mon = month[m]
dateval = dow, dd , mon, yy
datelab = tkinter.Label(window, text=dateval)
datelab.pack()
window.mainloop()
