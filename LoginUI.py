import tkinter as tk
import json
from tkinter import *
from functools import partial
from MessageUI import MessageUI
from AESEncryption import encryptText, decryptText, encryptFile, decryptFile
from base64 import b64encode, b64decode
from config import key

class LoginUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.Window = master
        self.createWidgets()

    def createWidgets(self):
        #window
        self.Window.geometry('400x150')  
        self.Window.title('Tkinter Login Form - pythonexamples.org')

        #username label and text entry box
        self.usernameLabel = Label(self.Window, text="User Name").grid(row=0, column=0)
        self.usernameEntry = Entry(self.Window)
        self.usernameEntry.grid(row=0, column=1) 

        #password label and password entry box
        self.passwordLabel = Label(self.Window,text="Password").grid(row=1, column=0)  
        self.passwordEntry = Entry(self.Window, show='*')
        self.passwordEntry.grid(row=1, column=1)  

        #login button
        loginButton = Button(self.Window, text="Login", command=self.validateLogin).grid(row=4, column=0)

                #username label and text entry box
        self.newUsernameLabel = Label(self.Window, text="User Name").grid(row=0, column=2)
        newUsername = StringVar()
        self.newUsernameEntry = Entry(self.Window, textvariable=newUsername)
        self.newUsernameEntry.grid(row=0, column=3)

        #password label and password entry box
        self.newPasswordLabel = Label(self.Window,text="Password").grid(row=1, column=2)  
        newPassword = StringVar()
        self.newPasswordEntry = Entry(self.Window, textvariable=newPassword, show='*')
        self.newPasswordEntry.grid(row=1, column=3)

        #validateLogin = partial(self.validateLogin, newUsername, newPassword)

        #login button
        newLoginButton = Button(self.Window, text="New Login", command=self.newLogIn).grid(row=4, column=2)

        self.serverAddressLabel = Label(self.Window, text="Server Address").grid(row=8, column=0)
        self.serverAddressEntry = Entry(self.Window)
        self.serverAddressEntry.grid(row=8, column=1)

    def validateLogin(self):
        with open('logins.json') as f:
            logins = json.load(f)
            userName = self.usernameEntry.get()
            password = self.passwordEntry.get()
            if(userName in logins.keys()):
                decodedPassword = b64decode(logins[userName]["Password"])
                decodedNonce = b64decode(logins[userName]["Nonce"])
                decrypted = decryptText(key, decodedPassword, decodedNonce, encode = True)
                if(decrypted == password):
                    self.usernameEntry.delete(0, 'end')
                    self.passwordEntry.delete(0, 'end')
                    self.login(userName)
                else:
                    print("Invalid log in")
            else:
                print("No Username Found")
        return
        
    def newLogIn(self):
        with open('logins.json') as f:
            userName = self.newUsernameEntry.get()
            password = self.newPasswordEntry.get()
            logins = json.load(f)
            if(self.usernameEntry.get() in logins.keys()):
                print("Username already used")
            else:
                encrypted, nonce = encryptText(key, password, encode = True)
                encodedPassword = b64encode(encrypted).decode()
                encodedNonce = b64encode(nonce).decode()
                logins[userName] = {"Password": encodedPassword, "Nonce": encodedNonce}
                self.updateLogIn(logins)
                self.newUsernameEntry.delete(0, 'end')
                self.newPasswordEntry.delete(0, 'end')
                self.login(userName)

    def login(self, userName):
        root2 = Toplevel()
        app2 = MessageUI(userName=userName, master=root2, serverAddress = self.serverAddressEntry.get())

    def updateLogIn(self, logins):
        with open('logins.json', 'w') as f:
            json.dump(logins, f)
