import tkinter as tk
from functools import partial
from tkinter import messagebox
import server
import threading
from server2csg import *
import time

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Server")
        self.textbox = None
        self.isRunning = False
        self.serverThread = None
        self.server2csgThread = None
        self.match = None

    def showFrame(self):
        frame1 = tk.Frame(self)
        frame1.pack()
        frame2 = tk.Frame(self)
        frame2.pack()

        self.textbox = tk.Text(frame2,width=50,height=25)
        self.textbox.pack()
        self.textbox.insert(tk.END,"Hello!")
        # Khung nhập địa chỉ ip
        tk.Label(frame1, text="PORT:", pady=4).grid(row=0, column=1)
        label = tk.Label(frame1, text="Server stopped!", pady=4)
        label.grid(row=0, column=4)
        inputIp = tk.Entry(frame1, width=20)
        inputIp.grid(row=0, column=2, padx=5)
        inputIp.insert(0,"3456")
        connectBT = tk.Button(frame1, text="Start", width=10)
        connectBT.config(command=partial(self.runServer, label, connectBT, inputIp.get()))
        connectBT.grid(row=0, column=3, padx=3)

    def runServer(self, label, connectBT, port):
        if not self.isRunning:
            self.isRunning = True
            label.config(text="Server is running!")
            connectBT.config(text="Stop")
            if not self.serverThread :
                self.server2csgThread = threading.Thread(target=main_run)
                self.server2csgThread.start()
                self.serverThread = threading.Thread(target=self.createThreadServer, args=("127.0.0.1",PORT))
                self.serverThread.start()
        else:
            self.isRunning = False
            server.isRunning = False
            self.serverThread.join()
            self.serverThread = None
            self.textbox.insert(tk.END,"\nStopped!")
            label.config(text="Server stopped!")
            connectBT.config(text="Start")

    def createThreadServer(self, host, port):
        server.main(host,port,self.textbox)
        pass

if __name__ == "__main__":
    window = Window()
    window.showFrame()
    window.mainloop()