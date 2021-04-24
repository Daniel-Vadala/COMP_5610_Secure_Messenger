import tkinter as tk
from tkinter import *
from tkinter import filedialog
from AESEncryption import encryptText, decryptText, encryptFile, decryptFile
from config import key, nonce

class MessageUI(tk.Frame):
    def __init__(self, userName = 'unknown', master=None):
        super().__init__(master)
        self.Window = master
        self.Window.geometry('1920x1080') 
        self.createWidgets()
        self.userName = userName
        
    def createWidgets(self):
        self.labelHead = Label(self.Window,
                             bg = "#2B0B4B", 
                              fg = "#EAECEE",
                              text = 'Secure Messages',
                               font = "Times 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Listbox(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#2B0B4B",
                             fg = "#EAECEE",
                             font = "Times 18")
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#A08BB5",
                              fg = "#EAECEE",
                              font = "Times 13")
          
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        self.uploadButton = Button(self.labelBottom,
                                text = "Upload",
                                font = "Times 10 bold",
                                height= 1, 
                                width = 20,
                                bg = "#ABB2B9",
                                command = self.uploadFile)
          
        self.uploadButton.place(relx = 0.77,
                             rely = 0.08,
                             relheight = 0.05, 
                             relwidth = 0.22)

        self.sendButton = Button(self.labelBottom,
                            text = "Send",
                            font = "Times 10 bold", 
                            width = 20,
                            height= 1,
                            bg = "#ABB2B9",
                            command = self.sendMessage)
          
        self.sendButton.place(relx = 0.77,
                             rely = 0.012,
                             relheight = 0.05, 
                             relwidth = 0.22)
          
        self.textCons.config(cursor = "arrow")
          
        scrollbar = Scrollbar(self.textCons)
          
        scrollbar.place(relheight = 1,
                        relx = 0.99)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)


    def sendMessage(self):
        self.textCons.configure(state=NORMAL)
        self.textCons.insert(END, self.userName + ": " + self.entryMsg.get())
        self.textCons.configure(state=DISABLED)
        self.entryMsg.delete(0, 'end')
    
    def recieveMessage(self, usernName, message):
        self.textCons.configure(state=NORMAL)
        self.textCons.insert(END, usernName + ": " + message)
        self.textCons.configure(state=DISABLED)

    def uploadFile(self, event=None):
        fileName = filedialog.askopenfilename()
        encryptFile(key, fileName)
        self.textCons.configure(state=NORMAL)
        self.textCons.insert(END, self.userName + ": Uploaded a file: " + fileName)
        self.textCons.configure(state=DISABLED)

    def recieveFile(self, fileName, userName):
        decryptFile(key, fileName)
        self.textCons.configure(state=NORMAL)
        self.textCons.insert(END, self.userName + ": Uploaded a file: " + fileName)
        self.textCons.configure(state=DISABLED)