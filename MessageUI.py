import tkinter as tk
import socket
import diffiehelman
import pickle
from tkinter import *
from tkinter import filedialog
from AESEncryption import encryptText, decryptText, encryptFile, decryptFile
from config import key
from threading import Thread


class MessageUI(tk.Frame):
    def __init__(self, userName = 'unknown', master=None):
        super().__init__(master)
        self.Window = master
        self.Window.geometry('1080x720')
        self.createWidgets()
        self.userName = userName

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get local machine name
        self.host = socket.gethostname()
        self.bob = diffiehelman.DiffieHellman()
        print(self.bob.publicKey)
        self.alice = 0
        self.port = 9999
        self.buffer = 1024
        self.s.connect((self.host, self.port))
        msg = pickle.dumps(self.bob.publicKey)
        self.s.send(msg)

        self.alice = self.s.recv(self.buffer)

        self.alice = pickle.loads(self.alice)

        self.bob.genKey(self.alice)
        self.key = self.bob.getKey()
        print(self.key)

        self.temp = pickle.dumps(self.key) #can't pickle and send in same line

        self.s.send(self.temp)

        self.key2 = self.s.recv(self.buffer)

        self.key2 = pickle.loads(self.key2)

        if (self.key != self.key2):
            print("system error")
            self.s.close()
            raise SystemExit(0)
        self.receiveThread = Thread(target=self.receiveMessage)
        self.receiveThread.start()


        
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

        message = self.entryMsg.get()
        encryptedMessage, nonce = encryptText(self.key, message)
        finalMessage = {"Message": encryptedMessage, "Nonce": nonce, "Username": self.userName}
        encodedMessage = pickle.dumps(finalMessage)
        self.s.send(encodedMessage)
        self.textCons.configure(state=NORMAL)
        self.textCons.insert(END, self.userName + ": " + message)
        self.textCons.configure(state=DISABLED)
        self.entryMsg.delete(0, 'end')
    
    def receiveMessage(self):
        while True:
            try:
                #message = client_socket.recv(BUFSIZ).decode("utf8")
                message = self.s.recv(self.buffer)
                print(message)
                message = pickle.loads(message)
                print(message)
                # self.textCons.configure(state=NORMAL)
                # self.textCons.insert(END, usernName + ": " + message)
                # self.textCons.configure(state=DISABLED)
            except OSError:  # Possibly client has left the chat.
                break


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