import tkinter as tk
import tkinter.messagebox
from hashlib import sha256
import sqlite3, os, hashlib, base64
class loginSystem(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Login-o-matic™")
        self.loadUI()
    def loadUI(self):
        self.mainFrm = tk.Frame(self)
        self.mainFrm.pack(expand = True, fill = "both", pady = (10,0))
        self.titleLab = tk.Label(self.mainFrm, text = "Login-o-matic™", font = (None, 32))
        self.titleLab.grid(row = 0, column = 0, columnspan = 2, padx = 10)
        self.userLab = tk.Label(self.mainFrm, text = "Username:")
        self.userLab.grid(row = 1, column = 0, sticky = "nesw")
        self.userEnt = tk.Entry(self.mainFrm)
        self.userEnt.grid(row = 1, column= 1, sticky = "nesw", pady = 10, padx = 10)
        self.passLab = tk.Label(self.mainFrm, text = "Password:")
        self.passLab.grid(row = 2, column = 0, sticky = "nesw")
        self.passEnt = tk.Entry(self.mainFrm, show = "*")
        self.passEnt.grid(row = 2, column= 1, sticky = "nesw", padx = 10)
        self.userEnt.focus()
        self.errLab = tk.Label(self.mainFrm, text = "", fg = "red")
        self.errLab.grid(row = 3, column = 0, sticky = "nesw", columnspan = 2, pady = 5)
        self.loginBtn = tk.Button(self.mainFrm, text = "Login™", font = (None, 24), relief = "solid", command = self.attemptLogin)
        self.loginBtn.grid(row = 4, column = 0, sticky = "nesw", columnspan = 2, pady = 10, padx = 10)
        self.div = tk.Frame(self.mainFrm, height = 2, bg = "black")
        self.div.grid(row = 5, column = 0, sticky = "ew", columnspan = 2, pady = 10)
        self.newUsrBtn = tk.Button(self.mainFrm, text = "Create new user", font = (None, 16), relief = "solid", command = self.newUser)
        self.newUsrBtn.grid(row = 6, column = 0, columnspan = 2, pady = (10,20))
    def nuserFormError(self, text):
        self.errLab.config(text = text)
        self.after(3000, lambda: self.errLab.config(text = ""))
    def registerNew(self):
        newUser = self.nuser.userEnt.get()
        newPass = self.nuser.passEnt.get()
        data = self.dbQuery("SELECT id, username FROM login").fetchall()[0]
        if newUser in data:
            self.nuserFormError("Username in use")
        else:
            if len(newPass) >= 8:
                salt = base64.b64encode(os.urandom(16)).decode()
                saltedPass = hashlib.sha256((newPass + salt).encode()).hexdigest()
                self.dbQuery("INSERT INTO login (username, password, salt) VALUES ('{}','{}','{}')".format(newUser,saltedPass, salt), commit = True)
                self.nuser.errLab.config(text = "Registered successfully", fg = "green")
                self.after(1000, self.nuser.destroy)
            else:
                self.nuserFormError("Password must be at least 8 characters")
    def newUser(self):
        self.nuser = tk.Toplevel(self)
        self.nuser.title("Register new user")
        self.nuser.mainFrm = tk.Frame(self.nuser)
        self.nuser.mainFrm.pack(expand = True, fill = "both", pady = (10,0))
        self.nuser.titleLab = tk.Label(self.nuser.mainFrm, text = "Create new user:", font = (None, 32))
        self.nuser.titleLab.grid(row = 0, column = 0, columnspan = 2, padx = 10)
        self.nuser.userLab = tk.Label(self.nuser.mainFrm, text = "Username:")
        self.nuser.userLab.grid(row = 1, column = 0, sticky = "nesw")
        self.nuser.userEnt = tk.Entry(self.nuser.mainFrm)
        self.nuser.userEnt.grid(row = 1, column= 1, sticky = "nesw", pady = 10, padx = 10)
        self.nuser.passLab = tk.Label(self.nuser.mainFrm, text = "Password:")
        self.nuser.passLab.grid(row = 2, column = 0, sticky = "nesw")
        self.nuser.passEnt = tk.Entry(self.nuser.mainFrm)
        self.nuser.passEnt.grid(row = 2, column= 1, sticky = "nesw", padx = 10)
        self.nuser.userEnt.focus()
        self.nuser.errLab = tk.Label(self.nuser.mainFrm, text = "", fg = "red")
        self.nuser.errLab.grid(row = 3, column = 0, sticky = "nesw", columnspan = 2, pady = 5)
        self.nuser.loginBtn = tk.Button(self.nuser.mainFrm, text = "Register™", font = (None, 24), relief = "solid", command = self.registerNew)
        self.nuser.loginBtn.grid(row = 4, column = 0, sticky = "nesw", columnspan = 2, pady = 10, padx = 10)
    def formError(self, text):
        self.errLab.config(text = text)
        self.after(3000, lambda: self.errLab.config(text = ""))
    def linError(self, text):
        self.lin.errLab.config(text = text)
        self.after(3000, lambda: self.errLab.config(text = "", fg = "red"))
    def changePass(self, uid):
        newPass = self.lin.newPassEnt.get()
        if len(newPass) < 8:
            self.linError("Password must be at least 8 characters")
        else:
            salt = base64.b64encode(os.urandom(16)).decode()
            saltedPass = hashlib.sha256((newPass + salt).encode()).hexdigest()
            self.dbQuery("UPDATE login SET password = '{}', salt = '{}' WHERE id = {}".format(saltedPass, salt, uid), commit = True)#
            self.lin.errLab.config(text = "Password changed successfully!", fg = "green")
            self.lin.newPassEnt.delete(0, "end")
    def loggedIn(self, uid):
        self.lin = tk.Toplevel(self)
        self.lin.id = uid
        self.lin.data = self.dbQuery("SELECT * FROM login WHERE id = {}".format(self.lin.id)).fetchone()
        self.lin.titleLab = tk.Label(self.lin, text = "Welcome, {}".format(self.lin.data[1]), font = (None, 32))
        self.lin.titleLab.grid(row = 0, column = 0, columnspan = 2, pady = 10)
        self.lin.newPassLab = tk.Label(self.lin, text = "New password:")
        self.lin.newPassLab.grid(row = 1, column = 0)
        self.lin.newPassEnt = tk.Entry(self.lin)
        self.lin.newPassEnt.grid(row = 1, column = 1)
        self.lin.errLab = tk.Label(self.lin, text = "", fg = "red")
        self.lin.errLab.grid(row = 2, column = 0, columnspan = 2)
        self.lin.subPass = tk.Button(self.lin, text = "Change password", font = (None, 16), relief = "solid", command = lambda: self.changePass(self.lin.id))
        self.lin.subPass.grid(row = 3, column = 0, columnspan = 2, pady = 10)
    def attemptLogin(self):
        attUser = self.userEnt.get()
        attPass = self.passEnt.get()
        data = self.dbQuery("SELECT id, username FROM login").fetchall()
        usernames = [data[n][1] for n, x in enumerate(data)]
        if attUser not in usernames:
            self.formError("Username not found")
        else:
            userId = data[usernames.index(attUser)][0]
            userPass, userSalt = self.dbQuery("SELECT password, salt FROM login WHERE id = {}".format(userId)).fetchone()
            if userPass == sha256((attPass + userSalt).encode()).hexdigest():
                #tk.messagebox.showinfo("Success", "Successfully logged in")
                self.loggedIn(userId)
                self.db.close()
                self.userEnt.delete(0, "end")
                self.passEnt.delete(0, "end")
                self.userEnt.focus()
            else:
                self.formError("Incorrect password")
    def dbQuery(self, sql, commit = False, debug = False):
        if debug:
            print(sql)
        self.db = sqlite3.connect("login™.db")
        c = self.db.cursor()
        c.execute(sql)
        if commit:
            self.db.commit()
        return c
        self.db.close()
app = loginSystem()
app.mainloop()

"""
user = "shs14166"
ps = "qwertyuiop"
salt = base64.b64encode(os.urandom(16)).decode()
salted_pass = hashlib.sha256((ps + salt).encode()).hexdigest()
c.execute("INSERT INTO login (username, password, salt) VALUES ('{}','{}','{}')".format(u,salted_pass, salt))
"""
