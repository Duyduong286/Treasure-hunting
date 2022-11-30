import tkinter as tk
from functools import partial
import threading
import socket
from tkinter import messagebox
import time
from threading_sk import Threading_socket
from protocol import *


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client")
        self.isRunning = False
        self.inputID = None
        self.Buts = {}
        self.memory = []
        self.Threading_socket = Threading_socket(self)
        print(self.Threading_socket.name)

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
                self.inputID.insert(0,rev_data['id'])
        
            elif rev_data['type'] == PKT_PLAYER :
                Ox = rev_data['n']
                for x in range(Ox):   # tạo ma trận button Ox * Oy
                    for y in range(Ox):
                        self.Buts[x, y] = tk.Button(frame, font=('arial', 15, 'bold'), height=1, width=2,
                                                    borderwidth=2, command=partial(self.handleButton, x=x, y=y))
                        self.Buts[x, y].grid(row=x, column=y)
                self.textbox.pack()
                self.textbox.insert(tk.END,f"Hello!")

                location = rev_data['location']
                m = rev_data['m']
                x, y = location.getPos()
                self.textbox.insert(tk.END,f"\nVui long chon vi tri cua tau!")
                for i in range(0,m):
                    for j in range(0,m):
                        self.Buts[x+i, y+j].config(bg='blue',command=partial(self.set_pos_ship, x=x+i, y=y+j))


                k = rev_data['k']

            elif rev_data['type'] == PKT_CHECK_LOCATION :
                check = rev_data['check']
                if check == 1:
                    self.textbox.insert(tk.END,f"\nVi tri hop le")
                elif check == 2:
                    self.textbox.insert(tk.END,f"\nVi tri tau khong hop le")
                elif check == 3 :
                    self.textbox.insert(tk.END,f"\nVi tri diem sang khong hop le")
                    
        self.client_socket.close()

    def send_data(self, data):
        self.client_socket.send(data)


    def set_pos_ship(self, x, y):
        if self.Buts[x, y]['text'] == "":
            if not self.memory:
                self.photo = tk.PhotoImage(file = "ship.png")
                self.Buts[x, y].config(bg='#f0f0f0',height=30,width=30,image=self.photo)
                self.memory.append([x,y])
                self.send_data(pkt_location_ship(id=int(self.inputID.get()),location=Coordinates(x,y)).sending_data())
            else:
                self.photo_tor = tk.PhotoImage(file = "torch.png")
                self.Buts[x, y].config(bg='#f0f0f0',height=30,width=30,image=self.photo_tor)
                self.memory.append([x,y])
                self.send_data(pkt_location_ship(id=int(self.inputID.get()),location=Coordinates(x,y)).sending_data())
        pass

    def handleButton(self, x, y):
        if self.Buts[x, y]['text'] == "":
            self.Buts[x, y]['text'] = 'X'
            self.send_data(pkt_move(123, Coordinates(x,y)).sending_data())

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

    def newGame(self):
        for x in range(Ox):
            for y in range(Oy):
                self.Buts[x, y]["text"] = ""


if __name__ == "__main__":
    Ox = 20  # Số lượng ô theo trục X
    Oy = 20 # Số lượng ô theo trục Y
    window = Window()
    window.showFrame()
    window.mainloop()