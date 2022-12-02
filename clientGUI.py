import tkinter as tk
from functools import partial
import threading
import socket
from tkinter import messagebox
import time
from protocol import *


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client")
        self.isRunning = False
        self.inputID = None
        self.Buts = {}
        self.memory = [0]
        self.mem_trea = []
        self.size_mem = [1,1,1,1]
        self.photo = tk.PhotoImage(file = "ship.png")
        self.photo_tor = tk.PhotoImage(file = "torch1.png")
        self.photo_neo = tk.PhotoImage(file = "neo.png")
        self.photo_fog = tk.PhotoImage(file = "fog.png")
        self.photo_fog_trea = tk.PhotoImage(file = "fog_trea.png")
        self.photo_sea = tk.PhotoImage(file = "sea.png")
        self.photo_light = tk.PhotoImage(file = "light.png")
        self.Ox = 0

    def showFrame(self):
        frame1 = tk.Frame(self)
        frame1.pack()
        # frame2 = tk.Frame(self)
        # frame2.pack()

        frame3 = tk.Frame(self)
        frame3.pack()

        frame2 = tk.Frame(frame3)
        frame2.pack(side="left")

        frame4 = tk.Frame(frame3)
        frame4.pack(side="right")

        self.textbox = tk.Text(frame4,width=50,height=50)

        # Undo = tk.Button(frame1, text="Undo", width=10,  # nút quay lại
        #                  command=partial(self.Undo, synchronized=True))
        # Undo.grid(row=0, column=0, padx=30)

        tk.Label(frame1, text="MyID", pady=4).grid(row=0, column=0)

        # Khung nhập địa chỉ ip
        self.inputID = tk.Entry(frame1, width=20)
        self.inputID.grid(row=0, column=1, padx=5)

        tk.Label(frame1, text="IP", pady=4).grid(row=0, column=2)

        # Khung nhập địa chỉ ip
        inputIp = tk.Entry(frame1, width=20)
        inputIp.grid(row=0, column=3, padx=5)
        inputIp.insert(0,"127.0.0.1")

        tk.Label(frame1, text="PORT", pady=4).grid(row=0, column=4)
        inputPort = tk.Entry(frame1, width=20)
        inputPort.grid(row=0, column=5, padx=5)
        inputPort.insert(0,"3456")

        connectBT = tk.Button(frame1, text="Connect", width=10,
                              command=partial(self.connectServer,"127.0.0.1",3456, frame2))
        connectBT.grid(row=0, column=6, padx=3)

        self.startBT = tk.Button(frame1, text="Start", width=10,
                              command=partial(self.handle_startBT))

        # makeHostBT = tk.Button(frame1, text="MakeHost", width=10,  # nút tạo host
        #                        command=lambda: self.Threading_socket.serverAction())
        # makeHostBT.grid(row=0, column=4, padx=30)
        # for x in range(Ox):   # tạo ma trận button Ox * Oy
        #     for y in range(Oy):
        #         self.Buts[x, y] = tk.Button(frame2, font=('arial', 15, 'bold'), height=1, width=2,
        #                                     borderwidth=2, command=partial(self.handleButton, x=x, y=y))
        #         self.Buts[x, y].grid(row=x, column=y)

    def connectServer(self, host, port, frame):
        self.client_socket = socket.socket()  
        self.client_socket.connect((host, port))  
        self.isRunning = True
        t2 = threading.Thread(target=self.createThreadClient, args=(frame,))
        t2.start()

    def createThreadClient(self, frame):
        self.client_socket.send(pkt_hello().sending_data())  
        while self.isRunning :
            rev_pkt = self.client_socket.recv(1024)
            
            rev_data = unpack(rev_pkt)
        
            if rev_data['type'] == PKT_ACCEPT :
                if rev_data['accept']:
                    self.inputID.insert(0,rev_data['id'])
                else:
                    print("Khong duoc chap nhan ket noi")
            elif rev_data['type'] == PKT_PLAYER :
                self.Ox = rev_data['n']
                for x in range(self.Ox):   # tạo ma trận button Ox * Oy
                    for y in range(self.Ox):
                        self.Buts[x, y] = tk.Button(frame, font=('arial', 15, 'bold'), height=1, width=2,
                                                    borderwidth=2, command=partial(self.handleButton, x=x, y=y))
                        self.Buts[x, y].config(height=36,width=28,image=self.photo_fog,text="fog")
                        self.Buts[x, y].grid(row=x, column=y)
                self.textbox.pack()
                self.textbox.insert(tk.END,f"Hello!")
                self.startBT.grid(row=0, column=7, padx=3)

                location = rev_data['location']
                m = rev_data['m']
                x, y = location.getPos()
                self.textbox.insert(tk.END,f"\nVui long chon vi tri cua tau!")
                
                if rev_data['id'] - 2000 < 0 :
                    posX, posY = 0,0
                else:
                    posX, posY = 0,self.Ox-5

                for i in range(0,int(2)):
                    for j in range(0,int(5)):
                        try:
                            self.Buts[posX+i,posY+j].config(command=partial(self.set_pos_ship, x=posX+i, y=posY+j))
                            self.Buts[posX+i,posY+j].config(height=36,width=28,image=self.photo_neo,text="neo") 
                        except:
                            pass

                for i in range(0,int(m/6)):
                    for j in range(0,int(m)):
                        try:
                            self.Buts[x+i, y+j].config(command=partial(self.set_pos_ship, x=x+i, y=y+j))
                            self.Buts[x+i, y+j].config(height=36,width=28,image=self.photo_light,text="light1")
                            self.Buts[x+i+8, y+j].config(command=partial(self.set_pos_ship, x=x+i+8, y=y+j))
                            self.Buts[x+i+8, y+j].config(height=36,width=28,image=self.photo_light,text="light2")
                            # self.memory.append([x,y])
                        except:
                            pass        

                self.size_mem = [len(self.memory), int(rev_data['k']/2) , int(rev_data['k']/2), 1]

            elif rev_data['type'] == PKT_CHECK_LOCATION :
                check = rev_data['check']
                if check == 1:
                    self.textbox.insert(tk.END,f"\nVi tri hop le")
                elif check == 2:
                    self.textbox.insert(tk.END,f"\nVi tri tau khong hop le")
                elif check == 3 :
                    self.textbox.insert(tk.END,f"\nVi tri diem sang khong hop le")

            elif rev_data['type'] == PKT_TREASURE :
                location = rev_data['location']
                posX, posY = location.getPos()
                for i in range(0,2):
                    for j in range(0,5):
                        try:
                            self.Buts[posX+i,posY+j].config(command=partial(self.set_pos_ship, x=posX+i, y=posY+j))
                            self.Buts[posX+i,posY+j].config(height=36,width=28,image=self.photo_fog_trea,text="fog_trea")
                            self.mem_trea.append([posX+i,posY+j]) 
                        except:
                            pass
                self.set_playing()
                self.set_light(self.memory,[])

        self.client_socket.close()


    def set_playing(self):
        for x in range(self.Ox):   # tạo ma trận button Ox * Oy
            for y in range(self.Ox):
                self.Buts[x, y].config(command=partial(self.handleButPlaying, x=x, y=y))
                if [x, y] not in self.memory and [x, y] not in self.mem_trea:
                    self.Buts[x, y].config(height=36,width=28,image=self.photo_fog,text="fog")

    def set_light(self, arr_light, db_light):
        self.light = []
        for i, j in db_light:
            try:
                if [i,j] not in self.memory:
                    self.Buts[i, j].config(height=36,width=28,image=self.photo_fog,text="fog")
                    if [i,j] in self.light:
                        self.light.remove([i,j])
            except:
                pass

        for PosX, PosY in arr_light:
            for i in range(PosX-1, PosX+2):
                for j in range(PosY-1, PosY+2):
                    if [i,j] not in arr_light:
                        try:
                            self.Buts[i, j].config(height=36,width=28,image=self.photo_sea,text="light")
                            self.light.append([i,j])
                        except:
                            pass

    def handleButPlaying(self, x, y):
        PosX = self.memory[0][0]
        PosY = self.memory[0][1]

        valid = []
        for i in range(PosX-1, PosX+2):
            for j in range(PosY-1, PosY+2):
                valid.append([i,j])

        if [x,y] in valid and [x,y] not in self.memory:
            self.move(x,y)

    def move(self, PosX, PosY):
        x = self.memory[0][0]
        y = self.memory[0][1]
        self.Buts[x, y].config(command=partial(self.handleButPlaying, x=x, y=y))
        self.Buts[x, y].config(height=36,width=28,image=self.photo_fog,text="fog")

        db_light = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                db_light.append([i,j])
        for i in range(PosX-1, PosX+2):
            for j in range(PosY-1, PosY+2):
                if [i,j] in db_light:
                    db_light.remove([i,j])

        self.memory[0] = [PosX, PosY]
        self.Buts[PosX, PosY].config(bg='#f0f0f0',height=36,width=28,image=self.photo,text="ship")

        self.textbox.insert(tk.END,f"\nMove: ({PosX},{PosY})")

        self.set_light(self.memory, db_light)

        self.send_data(pkt_move(id=int(self.inputID.get()), location=Coordinates(PosX,PosY)).sending_data())


    def send_data(self, data):
        self.client_socket.send(data)


    def set_pos_ship(self, x, y):
        if self.Buts[x, y]['text'] == "neo" and self.size_mem[3] > 0:
            if self.memory[0] == 0:
                self.Buts[x, y].config(bg='#f0f0f0',height=36,width=28,image=self.photo,text="ship")
                self.memory[0] = [x,y]
                print([x,y])
                self.size_mem[3] -= 1
                # self.send_data(pkt_location_ship(id=int(self.inputID.get()),location=Coordinates(x,y)).sending_data())
        elif self.Buts[x, y]['text'] == "light1" and self.size_mem[1] > 0:
            if len(self.memory) == 0:    
                self.memory.append(0)
            self.Buts[x, y].config(bg='#f0f0f0',height=36,width=28,image=self.photo_tor,text="torch1")
            self.memory.append([x,y])
            print([x,y])
            self.size_mem[1] -= 1
        elif self.Buts[x, y]['text'] == "light2" and self.size_mem[2] > 0:
            if len(self.memory) == 0:    
                self.memory.append(0)
            self.Buts[x, y].config(bg='#f0f0f0',height=36,width=28,image=self.photo_tor,text="torch2")
            self.memory.append([x,y])
            print([x,y])
            self.size_mem[2] -= 1
            # self.send_data(pkt_location_ship(id=int(self.inputID.get()),location=Coordinates(x,y)).sending_data())
        elif self.Buts[x, y]['text'] == "ship":
            print("ship")
            self.memory[0] = 0
            self.Buts[x, y].config(height=36,width=28,image=self.photo_neo,text="neo")
            self.size_mem[3] += 1
        elif self.Buts[x, y]['text'] == "torch1":
            print("torch")
            self.memory.remove([x,y])
            self.Buts[x, y].config(height=36,width=28,image=self.photo_light,text="light1")
            self.size_mem[1] += 1
        elif self.Buts[x, y]['text'] == "torch2":
            print("torch")
            self.memory.remove([x,y])
            self.Buts[x, y].config(height=36,width=28,image=self.photo_light,text="light2")
            self.size_mem[2] += 1

    def handle_startBT(self):
        self.send_data(pkt_location_ship(id=int(self.inputID.get()),location=Coordinates(self.memory[0][0], self.memory[0][1])).sending_data())

        listloc=[]
        for pos in self.memory[1:]:
            listloc.append(Coordinates(pos[0], pos[1]))

        self.send_data(pkt_location_light(id=int(self.inputID.get()),listloc=listloc).sending_data())    
    
    
    def handleButton(self, x, y):
        if self.Buts[x, y]['text'] == "fog":
            self.send_data(pkt_move(id=int(self.inputID.get()), location=Coordinates(x,y)).sending_data())
        pass

    # def handleButton(self, x, y):
    #     if self.Buts[x, y]['text'] == "": #Kiểm tra ô có ký tự rỗng hay không
    #         if self.memory.count([x, y]) == 0:
    #             self.memory.append([x, y])
    #         if len(self.memory) % 2 == 1:
    #             self.Buts[x, y]['text'] = 'O'
    #             self.Threading_socket.sendData("{}|{}|{}|".format("hit", x, y))
    #             if(self.checkWin(x, y, "O")):
    #                 self.notification("Winner", "O")
    #                 self.newGame()
    #         else:
    #             print(self.Threading_socket.name)
    #             self.Buts[x, y]['text'] = 'X'
    #             self.Threading_socket.sendData("{}|{}|{}|".format("hit", x, y))
    #             if(self.checkWin(x, y, "X")):
    #                 self.notification("Winner", "X")
    #                 self.newGame()

        

    def notification(self, title, msg):
        messagebox.showinfo(str(title), str(msg))

    def checkWin(self, x, y, XO):
        return False

    def Undo(self, synchronized):
        if(len(self.memory) > 0):
            x = self.memory[len(self.memory) - 1][0]
            y = self.memory[len(self.memory) - 1][1]
            # print(x,y)
            self.Buts[x, y]['text'] = ""
            self.memory.pop()
            if synchronized == True:
                self.Threading_socket.sendData("{}|".format("Undo"))
            print(self.memory)
        else:
            print("No character")

    # def newGame(self):
    #     for x in range(Ox):
    #         for y in range(Oy):
    #             self.Buts[x, y]["text"] = ""


if __name__ == "__main__":
    Ox = 20  # Số lượng ô theo trục X
    Oy = 20 # Số lượng ô theo trục Y
    window = Window()
    window.showFrame()
    window.mainloop()