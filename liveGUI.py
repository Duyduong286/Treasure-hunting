import tkinter as tk
from functools import partial
from tkinter import messagebox
import server
import threading
from server2csg import *
from tkinter import *
import time

SIDE_LEFT = 0
SIDE_RIGHT = 1

class Window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Live")
        self.isRunning = False
        self.Buts_left = {}
        self.Buts_right = {}
        self.memory_1 = [[0,0],[0,0]]
        self.memory_2 = [[0,0],[0,0]]
        self.light_tor_1 = []
        self.light_tor_2 = []
        self.en_tor_1 = []
        self.en_tor_2 = []
        self.photo_battle = tk.PhotoImage(file = "image/Battle.png")
        self.photo = tk.PhotoImage(file = "image/ship3.png")
        self.photo_en = tk.PhotoImage(file = "image/ship.png")
        self.photo_tor_en = tk.PhotoImage(file = "image/torch1.png")
        self.photo_tor = tk.PhotoImage(file = "image/torch2.png")
        self.photo_neo = tk.PhotoImage(file = "image/neo.png")
        self.photo_fog = tk.PhotoImage(file = "image/fog.png")
        self.photo_fog_trea = tk.PhotoImage(file = "image/fog_trea.png")
        self.photo_sea = tk.PhotoImage(file = "image/sea.png")
        self.photo_light = tk.PhotoImage(file = "image/light.png")
        self.photo_trea = tk.PhotoImage(file = "image/treasure.png")
        self.resizable(False, False)


    def showFrame(self):
        frame_top = tk.Frame(self)
        frame_top.pack()
        frame1 = tk.Frame(self)
        frame1.pack(side=LEFT,padx=10, pady=10)
        frame2 = tk.Frame(self)
        frame2.pack(side=RIGHT,padx=10, pady=10)
        frame3 = tk.Frame(self)
        frame3.pack(side=RIGHT,padx=10, pady=10)

        tk.Label(frame_top, text = "TURN:", font=('arial', 15)).pack(side=LEFT) 
        self.label_turn = tk.Label(frame_top, text = "UID1", font=('arial', 15))
        self.label_turn.pack(side=LEFT)

        tk.Button(frame_top,text="turn",command=partial(self.set_turn, "hi")).pack(side=LEFT)

        tk.Label(frame3, image=self.photo_battle).pack()
        self.setMap(frame1, self.Buts_left, 20, 20, "UID1")
    
        self.setMap(frame2, self.Buts_right,  20, 20, "UID2")

    def set_turn(self, turn):
        self.label_turn.config(text="UID2")

    def set_light_tor(self):
        for PosX, PosY in self.memory_1[2:]:
            for i in range(PosX-1, PosX+2):
                for j in range(PosY-1, PosY+2):
                    if [i,j] not in self.light_tor_1 and [i,j] not in self.memory_1[2:]:
                        try:
                            self.Buts_left[i,j].config(height=36,width=28,image=self.photo_sea,text="light")
                            self.light_tor_1.append([i, j])
                        except:
                            pass

        for PosX, PosY in self.memory_2[2:]:
            for i in range(PosX-1, PosX+2):
                for j in range(PosY-1, PosY+2):
                    if [i,j] not in self.light_tor_2 and [i,j] not in self.memory_2[2:]:
                        try:
                            self.Buts_right[i,j].config(height=36,width=28,image=self.photo_sea,text="light")
                            self.light_tor_2.append([i, j])
                        except:
                            pass

    def move(self, side : int, loc):
        if side == SIDE_LEFT:
            buts = self.Buts_left
            mem = self.memory_1
            light = self.light_tor_1
        elif side == SIDE_RIGHT:
            buts = self.Buts_right
            mem = self.memory_2
            light = self.light_tor_2
        i,j = mem[0]
        if [i, j] in light:
            buts[i,j].config(height=36,width=28,image=self.photo_sea)
        else:
            buts[i,j].config(height=36,width=28,image=self.photo_fog)
        i,j = loc
        mem[0] = loc
        buts[i,j].config(height=36,width=28,image=self.photo)
        pass

    def setMap(self, frame, buts, width, height, text):
        frame_map = tk.Frame(frame)
        frame_map.pack()
        for x in range(width):   # tạo ma trận button Ox * Oy
            for y in range(height):
                buts[x, y] = tk.Button(frame_map, font=('arial', 15, 'bold'), height=1, width=2,
                                                    borderwidth=2)
                buts[x, y].grid(row=x, column=y)
        
        tk.Label(frame, text=text,font=('arial', 15), padx=10).pack()

    def set_location_light(self, side : int, listloc : list):
        if side == SIDE_LEFT:
            buts = self.Buts_left
        elif side == SIDE_RIGHT:
            buts = self.Buts_right
            
        for coor in listloc:
            try:
                i,j = coor.getPos()                   
                buts[i, j].config(height=36,width=28,image=self.photo_light)
            except:
                pass
        pass

    def set_light_en(self, side : int, listloc : list):
        if side == SIDE_LEFT:
            buts = self.Buts_left
            en_tor = self.en_tor_1
        elif side == SIDE_RIGHT:
            en_tor = self.en_tor_2
            buts = self.Buts_right

        if not listloc:
            try:
                for i,j in en_tor:
                    buts[i, j].config(height=36,width=28,image=self.photo_fog)
            except:         
                pass

        for coor in listloc:
            try:
                i,j = coor.getPos()                 
                buts[i, j].config(height=36,width=28,image=self.photo_tor_en)
            except:
                pass
        pass


    def set_location_neo(self, side : int, listloc : list):
        if side == SIDE_LEFT:
            buts = self.Buts_left
        elif side == SIDE_RIGHT:
            buts = self.Buts_right
        
        for coor in listloc:
            try:
                i,j = coor.getPos()                   
                buts[i, j].config(height=36,width=28,image=self.photo_neo)
            except:
                pass
        pass

    def set_location_tre(self, side : int, listloc : list):
        if side == SIDE_LEFT:
            buts = self.Buts_left
        elif side == SIDE_RIGHT:
            buts = self.Buts_right
        
        for coor in listloc:
            try:
                i,j = coor.getPos()                   
                buts[i, j].config(height=36,width=28,image=self.photo_fog_trea)
            except:
                pass
        pass

    def set_default(self, side):
        if side == SIDE_LEFT:
            for i,j in self.Buts_left:
                self.Buts_left[i,j].config(height=36,width=28,image=self.photo_fog)
        else:
            for i,j in self.Buts_right:
                self.Buts_right[i,j].config(height=36,width=28,image=self.photo_fog)

    def set_location(self, side : int, **kwargs):
        if side == SIDE_LEFT:
            buts = self.Buts_left
            mem = self.memory_1
            light = self.light_tor_1
        elif side == SIDE_RIGHT:
            buts = self.Buts_right
            mem = self.memory_2
            light = self.light_tor_2

        if kwargs:
            list_keys = kwargs.keys()
            if "ship" in list_keys:
                i, j = kwargs['ship'].getPos()
                buts[i, j].config(height=36,width=28,image=self.photo)
                mem[0] = [i,j]
            if "ship_en" in list_keys:
                i, j = kwargs['ship_en'].getPos()
                if i < 0:
                    i, j = mem[1]
                    if [i, j] in light:
                        buts[i,j].config(height=36,width=28,image=self.photo_sea)
                    else:
                        buts[i,j].config(height=36,width=28,image=self.photo_fog)
                else:
                    buts[i, j].config(height=36,width=28,image=self.photo_en)
                    
                    if [i,j] != mem[1]:
                        i,j = mem[1]
                        if [i, j] in light:
                            buts[i,j].config(height=36,width=28,image=self.photo_sea)
                        else:
                            buts[i,j].config(height=36,width=28,image=self.photo_fog)
                        mem[1] = kwargs['ship_en'].getArrPos()
            if "treasure" in list_keys:
                i, j = kwargs['treasure'].getPos()
                buts[i, j].config(height=36,width=28,image=self.photo_trea)
            if "light" in list_keys:
                i, j = kwargs['light'].getPos()
                mem.append([i,j])
                buts[i, j].config(height=36,width=28,image=self.photo_tor)      
        pass

if __name__ == "__main__":
    window = Window()
    window.showFrame()
    window.mainloop()