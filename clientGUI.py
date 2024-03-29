import tkinter as tk
from tkinter import DISABLED
from functools import partial
import threading
import socket
from tkinter import messagebox
from protocol import *
import time
import auto_config 
import config

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.auto_play = False
        self.title("Client")
        self.isRunning = False
        self.inputID = None
        self.Buts = {}
        self.memory = [0]
        self.mem_trea = []
        self.size_mem = [1,1,1,1]
        self.enemies = [0]
        self.photo = tk.PhotoImage(file = "image/ship3.png")
        self.photo_en = tk.PhotoImage(file = "image/ship.png")
        self.photo_tor_en = tk.PhotoImage(file = "image/torch1.png")
        self.photo_tor = tk.PhotoImage(file = "image/torch2.png")
        self.photo_neo = tk.PhotoImage(file = "image/neo.png")
        self.photo_fog = tk.PhotoImage(file = "image/fog.png")
        self.photo_fog_trea = tk.PhotoImage(file = "image/fog_trea.png")
        self.photo_sea = tk.PhotoImage(file = "image/sea.png")
        self.photo_light = tk.PhotoImage(file = "image/light.png")
        self.Ox = 0
        self.turn = False

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

        tk.Label(frame1, text="MyID", pady=4).grid(row=0, column=0)

        # Khung nhập địa chỉ ip
        self.inputID = tk.Entry(frame1, width=20)
        self.inputID.grid(row=0, column=1, padx=5)

        tk.Label(frame1, text="IP", pady=4).grid(row=0, column=2)

        # Khung nhập địa chỉ ip
        self.inputIp = tk.Entry(frame1, width=20)
        self.inputIp.grid(row=0, column=3, padx=5)
        self.inputIp.insert(0,"0.tcp.ap.ngrok.io")

        tk.Label(frame1, text="PORT", pady=4).grid(row=0, column=4)
        self.inputPort = tk.Entry(frame1, width=20)
        self.inputPort.grid(row=0, column=5, padx=5)
        self.inputPort.insert(0,"10139")

        tk.Label(frame1, text="PASSWD", pady=4).grid(row=0, column=6)
        inputPass = tk.Entry(frame1, width=20)
        inputPass.grid(row=0, column=7, padx=5)
        inputPass.insert(0,"123456")

        self.connectBT = tk.Button(frame1, text="Connect", width=10,
                              command=partial(self.connectServer, None, None, frame2))
        self.connectBT.grid(row=0, column=8, padx=3)

        self.startBT = tk.Button(frame1, text="Start", width=10,
                              command=partial(self.handle_startBT, self.connectBT))

        self.autoBT = tk.Button(frame1, text="Auto", width=10,
                              command=self.create_auto)   

    def disconnect(self):
        self.alert("Warning", "Warning", "DISCONNECTED")

    def connectServer(self, host, port, frame):
        self.connectBT.config(text="Disconnect",command=self.disconnect) 
        self.client_socket = socket.socket()  
        self.client_socket.connect((str(self.inputIp.get()).strip(),int(str(self.inputPort.get()).strip())))  
        self.isRunning = True
        self.thread = threading.Thread(target=self.createThreadClient, args=(frame,))
        self.thread.start()

    def alert(self, type, title, mess):
        if type == "Information":
            msg_box = messagebox.showinfo(title, mess)
        elif type == "Warning":
            msg_box = messagebox.showwarning(title, mess)
        elif type == "Error":
            msg_box = messagebox.showerror(title, mess)

        if msg_box == 'ok':
            self.client_socket.send(b'END')  
             
            if self.isRunning:
                self.isRunning = False
                try:
                    self.thread.join() 
                    self.client_socket.close()
                except:
                    pass
 
            self.destroy() 
            

    def createThreadClient(self, frame):
        self.client_socket.send(pkt_hello().sending_data())  
        while self.isRunning :

            rev_pkt = self.client_socket.recv(1024)
            rev_data = unpack(rev_pkt)
            try:
                if check_type(rev_pkt) == 1 and len(rev_pkt) > 100:
                    rev_data = unpack(rev_pkt[16:])
                if check_type(rev_pkt) == PKT_CHECK_LOCATION and len(rev_pkt) > 35:
                    rev_data = unpack(rev_pkt[32:])
            except:
                pass
            if not rev_data:
                continue
            
            if rev_data['type'] == PKT_ACCEPT :
                if rev_data['accept']:
                    if not rev_data['id']:
                        self.inputID.insert(0,rev_data['id'])
                else:
                    print("Khong duoc chap nhan ket noi")
                    self.alert("Error", "Error", "Khong duoc chap nhan ket noi!")
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
                self.startBT.grid(row=0, column=9, padx=3)
                self.autoBT.grid(row=0, column=10, padx=3)
                listloc = rev_data['listloc']
                m = rev_data['m']
                self.textbox.insert(tk.END,f"\nVui long chon vi tri cua tau!")
                
                self.uid = rev_data['id']
                if self.uid <= 0 or not self.uid:
                    if listloc[0][0] == 4 :
                        self.uid = 1032
                        self.inputID.insert(0,"1032")
                    else:
                        self.uid = 2039
                        self.inputID.insert(0,"2039")



                if self.uid - 2000 < 0 :
                    posX, posY = 0,0
                    self.turn = True
                else:
                    posX, posY = 0,self.Ox-5
                    self.turn = False

                for i in range(0,int(2)):
                    for j in range(0,int(5)):
                        try:
                            self.Buts[posX+i,posY+j].config(command=partial(self.set_pos_ship, x=posX+i, y=posY+j))
                            self.Buts[posX+i,posY+j].config(height=36,width=28,image=self.photo_neo,text="neo") 
                        except:
                            pass

                for coor in listloc:
                    try:
                        i,j = coor.getPos()                   
                        self.Buts[i, j].config(command=partial(self.set_pos_ship, x=i, y=j))

                        if i <= 10:
                            self.Buts[i, j].config(height=36,width=28,image=self.photo_light,text="light1")
                        else:
                            self.Buts[i, j].config(height=36,width=28,image=self.photo_light,text="light2")
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

            elif rev_data['type'] == PKT_TURN :
                self.textbox.insert(tk.END,f"\nDa den luot cua ban!")
                self.turn = True

            elif rev_data['type'] == PKT_LOCATION_SHIP:
                x,y = rev_data['location'].getPos()
                if [x,y] != [-1,-1]:
                    self.enemies[0] = 0
                    self.set_light(self.memory,[])
                    self.enemies[0] = [x, y]
                    self.Buts[x, y].config(bg='#f0f0f0',height=36,width=28,image=self.photo_en,text="ship_en")
                elif self.enemies[0] != 0 and len(self.enemies[0]) == 2:
                    [x, y] = self.enemies[0]
                    self.enemies[0] = 0
                    self.set_light(self.memory,[])

            elif rev_data['type'] == PKT_LOCATION_LIGHT:
                if len(self.enemies) == 0:
                    self.enemies[0] = 0
                self.enemies = [self.enemies[0]]
                for coor in rev_data['listloc']:
                    self.enemies.append(coor.getArrPos())
                    [x, y] = coor.getArrPos()
                try:
                    self.Buts[x, y].config(bg='#f0f0f0',height=36,width=28,image=self.photo_tor_en,text="torch_en")
                except:
                    if x > 2000:
                        self.textbox.insert(tk.END,f"\nLOSE! - SHOOTED")
                        self.alert("Warning", "Disappointed!!!", "LOSE\nBan da bi ban trung!")
                    pass
                # self.set_light(self.memory,[])

            elif rev_data['type'] == PKT_WON:
                if rev_data['res'] == PKT_WON_SHOOTED:
                    self.textbox.insert(tk.END,f"\nWON! - SHOOTED")
                    self.alert("Information", "Congratulation!!!", "WIN\nBan da ban trung dich!")
                elif rev_data['res'] == PKT_WON_TREASURE:
                    self.textbox.insert(tk.END,f"\nWON! - TREASURE")
                    self.alert("Information", "Congratulation!!!", "WIN\nBan da tim thay kho bau!")
                else:
                    self.textbox.insert(tk.END,f"\nWON! - DISCONNECTED")
                    self.alert("Information", "Congratulation!!!", "WIN\nKe dich da roi tran chien!")

            elif rev_data['type'] == PKT_LOSE:
                if rev_data['res'] == PKT_WON_SHOOTED:
                    self.textbox.insert(tk.END,f"\nLOSE! - SHOOTED")
                    self.alert("Warning", "Disappointed!!!", "LOSE\nBan da bi ban trung!")
                elif rev_data['res'] == PKT_WON_TREASURE:
                    self.textbox.insert(tk.END,f"\nLOSE! - TREASURE")
                    self.alert("Warning", "Disappointed!!!", "LOSE\nKe dich da tim thay kho bau truoc ban!")
                else:
                    self.textbox.insert(tk.END,f"\nLOSE! - DISCONNECTED")

            elif rev_data['type'] == PKT_CHECK:
                self.textbox.insert(tk.END,f"\nVi tri ban khong hop le! - Tam ban: 6")
                self.turn = True
        # if rev_data['type'] in [PKT_LOCATION_SHIP, PKT_LOCATION_LIGHT]:
        #     self.set_light(self.memory,[])

        self.client_socket.close()


    def set_playing(self):
        for x in range(self.Ox):   # tạo ma trận button Ox * Oy
            for y in range(self.Ox):
                self.Buts[x, y].config(command=partial(self.handleButPlaying, x=x, y=y))
                self.setBind(self.Buts[x, y], x, y)
                if [x, y] not in self.memory and [x, y] not in self.mem_trea:
                    self.Buts[x, y].config(height=36,width=28,image=self.photo_fog,text="fog")

        if self.turn:
            self.textbox.insert(tk.END,f"\nDen luot cua ban!")
        else:
            self.textbox.insert(tk.END,f"\nDoi den luot!")

    def set_light(self, arr_light, db_light, *args):
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
                    if [i,j] not in arr_light and [i,j] not in self.enemies:
                        try:
                            self.Buts[i, j].config(height=36,width=28,image=self.photo_sea,text="light")
                            self.light.append([i,j])
                        except:
                            pass

    def handleButPlaying(self, x, y):
        if self.turn:
            PosX = self.memory[0][0]
            PosY = self.memory[0][1]

            valid = []
            for i in range(PosX-1, PosX+2):
                for j in range(PosY-1, PosY+2):
                    valid.append([i,j])

            if [x,y] in valid and [x,y] not in self.memory and [x,y] not in self.enemies :
                self.move(x,y)
        else:
            self.textbox.insert(tk.END,f"\nChua den luot ban!")

    def move(self, PosX, PosY):
        self.turn = False
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

        self.send_data(pkt_move(id=self.uid, location=Coordinates(PosX,PosY)).sending_data())


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
                self.memory.append([0,0])
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

    def handle_startBT(self, button):
        self.send_data(pkt_location_ship(id=self.uid,location=Coordinates(self.memory[0][0], self.memory[0][1])).sending_data())

        listloc=[]
        print(self.memory[1:])
        
        for pos in self.memory[1:]:
            listloc.append(Coordinates(pos[0], pos[1]))

        print(listloc)
        self.send_data(pkt_location_light(id=self.uid,listloc=listloc).sending_data())    
    
    
    def handleButton(self, x, y):
        if self.Buts[x, y]['text'] == "fog":
            self.send_data(pkt_move(id=self.uid, location=Coordinates(x,y)).sending_data())
        pass

    def handleShoot(self, x, y, event):
        if self.turn:
            self.turn = False
            self.textbox.insert(tk.END,f"\nShoot: ({x},{y})")
            self.send_data(pkt_shoot(id=self.uid, location=Coordinates(x,y)).sending_data())
            pass

    def setBind(self, button, x, y):
        button.bind("<Button-3>", partial(self.handleShoot, x, y))

    def create_auto(self):
        #dichuyen: handleButPlaying
        #shoot:handleShoot
        if not self.auto_play:
            self.auto_play = False
            self.textbox.insert(tk.END,f"\nAuto Play")
            self.thread_auto = threading.Thread(target=self.auto)
            self.thread_auto.start()

    def auto(self):
        if self.uid - 2000 < 0 :
            for x,y in auto_config.LOCATION_1:
                self.set_pos_ship(x,y)
            # self.handle_startBT()
            while not self.mem_trea:
                pass

            time.sleep(2)
            self.auto_uid_1(auto_config.TURN_1)
        else:
            for x,y in auto_config.LOCATION_2:
                self.set_pos_ship(x,y)
            # self.handle_startBT()
            while not self.mem_trea:
                pass
            time.sleep(2)
            self.auto_uid_2(auto_config.TURN_2)
        pass

    def auto_uid_1(self,listloc : list):
        list_loc=listloc
        count = 0
        while True:
            # if not self.isRunning:
            #     break
            if self.turn:
                time.sleep(1.5)  
                Posx, Posy = self.memory[0]

                if self.enemies[0] != 0:
                    x ,y = self.enemies[0]
                    self.handleShoot(x,y,None)
                    break
                

                try:
                    x,y = list_loc[count]
                    self.handleButPlaying(x,y)
                except:
                    break


                if [Posx, Posy] != self.memory[0]:
                    count += 1

        pass

    def auto_uid_2(self,listloc):
        list_loc=listloc
        count = 0

        while True:
            # if not self.isRunning:
            #     break
            if self.turn:
                time.sleep(1.5)
                Posx, Posy = self.memory[0]

                if self.enemies[0] != 0:
                    x ,y = self.enemies[0]
                    self.handleShoot(x,y,None)
                    break

                try:
                    if len(list_loc) < 1:
                        break
                    x,y = list_loc[count]
                    self.handleButPlaying(x,y)
                except:
                    break
                
                if [Posx, Posy] != self.memory[0]:
                    count += 1
            
        pass


if __name__ == "__main__":
    window = Window()
    window.showFrame()
    window.mainloop()