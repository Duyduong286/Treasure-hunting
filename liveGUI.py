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
        self.title("Live")
        self.isRunning = False
        self.Buts = {}

    def showFrame(self):
        frame1 = tk.Frame(self)
        frame1.pack()
        frame2 = tk.Frame(self)
        frame2.pack()

        # # Khung nhập địa chỉ ip
        # tk.Label(frame1, text="PORT:", pady=4).grid(row=0, column=1)
        # label = tk.Label(frame1, text="Server stopped!", pady=4)
        # label.grid(row=0, column=4)
        # inputIp = tk.Entry(frame1, width=20)
        # inputIp.grid(row=0, column=2, padx=5)
        # inputIp.insert(0,"3456")

        inputIp1 =tk.Entry(frame2, width=20)
        inputIp1.pack()
        for x in range(20):   # tạo ma trận button Ox * Oy
            for y in range(20):
                self.Buts[x, y] = tk.Button(frame1, font=('arial', 15, 'bold'), height=1, width=2,
                                            borderwidth=2)
                self.Buts[x, y].grid(row=x, column=y)

    def setMap(self):
        
        pass

if __name__ == "__main__":
    window = Window()
    window.showFrame()
    window.mainloop()