import tkinter as tk
import winsound
msg = """A problem has been detected and Windows has been shut down to prevent damage to your computer.


ERROR_CRITICAL_PROCESS_DIED

If this is the first you've seen this Stop error screen restart your computer, If this screen appears again, follow these steps:

Check to make sure any new hardware or software is properly installed. If this is a new installation, ask your hardware or software manufacturer for any Windows updates you might need.

If problems continue, disable or remove any newly installed hardware or software. Disable BIOS memory options such as caching or shadowing. If you need to use Safe Mode to remove or disable components, restart your computer, press F8 to select Advanced Startup Options and then select Safe Mode.

Technical information:

*** STOP 0x00000001 (0x0000000C, 0x00000002, 0x00000000)
  ***	sys32.exe - Critical process died

Beginning dump of physical memory

Physical memory dump complete.

Contact your system administrator or technical support group for further assistance"""
def snd():
    root.after(100, lambda: winsound.PlaySound("SystemHand", winsound.SND_ALIAS))
def close(event = None):
    root.attributes("-fullscreen",False)
    root.state("zoomed")
    root.config(cursor = "arrow")
root = tk.Tk()
root.attributes("-fullscreen",True)
root.config(bg = "blue")
main = tk.Frame(root, bg = "blue")
main.place(relx = 0, rely = 0)
mainLab = tk.Label(main, text = msg, bg = "blue", fg = "white", justify = "left", wraplength = 1000, font = ("Consolas","16"))
mainLab.pack(ipadx = 75, ipady = 75, fill = "y")
root.config(cursor = "none")
root.bind("<Escape>", close)
snd()
root.mainloop()
