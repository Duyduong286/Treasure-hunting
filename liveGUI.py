import tkinter as tk
from functools import partial
from tkinter import messagebox
import server
import threading
from server2csg import *
from tkinter import *
import time

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Live")
        self.isRunning = False
        self.Buts = {}

    def showFrame(self):
        frame_top = tk.Frame(self)
        frame_top.pack()
        frame1 = tk.Frame(self)
        frame1.pack(side=LEFT)
        frame2 = tk.Frame(self)
        frame3 = tk.Frame(self)
        frame3.pack()
        frame2.pack(side=RIGHT)
        



        # frame = tk.Frame(self).grid(row=1, columnspan=3)
        # frame1 = tk.Frame(self).grid(column = 0, row = 1, rowspan = 2)
        # frame_mid = tk.Frame(self).grid(column = 1, row=1, rowspan=2)
        # frame2 = tk.Frame(self).grid(column = 2, row=1, rowspan=2)

        # btm_frame = tk.Frame(frame1).grid(row = 3, columnspan = 3)
        # btm_frame = tk.Frame(frame2).grid(row = 3, columnspan = 1)

        label_turn = tk.Label(frame_top, text="TURN", pady=4).grid(row=0, column=0)
        label_vs = tk.Entry(frame_top).grid(row=1, column=0)
        self.setMap(frame1, 15, 20)

        self.setMap(frame2, 15, 20)

        # # Khung nhập địa chỉ ip
        # tk.Label(frame1, text="PORT:", pady=4).grid(row=0, column=1)
        # label = tk.Label(frame1, text="Server stopped!", pady=4)
        # label.grid(row=0, column=4)
        # inputIp = tk.Entry(frame1, width=20)
        # inputIp.grid(row=0, column=2, padx=5)
        # inputIp.insert(0,"3456")

        

    def setMap(self, frame, width, height):
        for x in range(width):   # tạo ma trận button Ox * Oy
            for y in range(height):
                self.Buts[x, y] = tk.Button(frame, font=('arial', 15, 'bold'), height=1, width=2,
                                                    borderwidth=2)
                self.Buts[x, y].grid(row=x, column=y)
        

if __name__ == "__main__":
    window = Window()
    window.showFrame()
    window.mainloop()