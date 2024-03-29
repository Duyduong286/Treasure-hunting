import socket
import selectors
import types
from protocol import *
import tkinter as tk
from tkinter import Text
from Game import *
from server2csg import *
import liveGUI

sel = selectors.DefaultSelector()
isRunning = True
connect2csg = False
game = Game()

def accept_wrapper(sock):
    if game.status == SET_MATCH:
        conn, addr = sock.accept()  # Should be ready to read
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", user=User(0,0), uid=-1)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

    if game.status == SETUP:
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        textbox.insert(tk.END,f"\nAccepted connection from {addr}")
        conn.setblocking(False)
        id, user = game.set_user(addr)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", user=user, uid=id)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    data.user.set_sock(sock)
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)  # Should be ready to read
            if game.status == SET_MATCH:
                global game_match
                game_match = recv_data.decode()
                if game_match:
                    game.status = SETUP
                    textbox.insert(tk.END,f"\nMATCH: {game_match}")
                    textbox.insert(tk.END,f"\nGAME STATUS: SETUP")
            else:
                if not recv_data:
                    raise None
                dict_data = unpack(recv_data)
                for _key in dict_data.keys():
                    textbox.insert(tk.END,f"\n{str(_key) + ' : ' + str(dict_data[_key])}")

                collect_data(dict_data, data.user)

                data.inb = b""
                data.inb += recv_data
        except:
            sock.send(b'END')
            print(f"Disconnected to {data.addr}, UID: {data.uid}")
            textbox.insert(tk.END,f"\nDisconnected to {data.addr}, UID: {data.uid}")
            sel.unregister(sock)
            sock.close()
            check_status_game(id=data.uid, user= data.user, remove= True)

    if mask & selectors.EVENT_WRITE:
        if data.inb:
            for pkt in sending_data(check_type(data.inb), data.user):
                data.outb = pkt
                if data.outb:
                    print(f"Echoing {data.outb!r} to {data.addr}")
                    textbox.insert(tk.END,f"\nEchoing {data.outb!r} to {data.addr}")
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]
            data.inb = b""

    check_status_game()

def check_status_game(**kwargs):
    if game.status == SETUP and 'remove' in kwargs.keys(): 
        game.remove_user(kwargs['id'] // 1000 - 1)
    
    if game.status == PLAYING and 'user' in kwargs.keys():
        if game.get_user() == [None, None]:
            print(f"\nVan dau da ket thuc!!!")
            textbox.insert(tk.END,f"\nVan dau da ket thuc!!!")
            game.status == SETUP
            return
        user = kwargs['user']
        
        if user == game.get_user_1():
            other = game.get_user_2()
        else:
            other = game.get_user_1()

        send_sock(other, pkt_won(other.uid,PKT_WON_DISCON).sending_data())
        pass

    if game.status == END:
        print(f"\nVan dau da ket thuc!!!")
        textbox.insert(tk.END,f"\nVan dau da ket thuc!!!")
        game.status = SETUP
        pass

def collect_data(dict_data : list, user : User):
    if dict_data['type'] == PKT_LOCATION_SHIP:
        user.memory[0] = dict_data['location'].getArrPos()
        textbox.insert(tk.END,f"\nUID: {user.uid}, MEM: {user.memory}")
    elif dict_data['type'] == PKT_LOCATION_LIGHT:
        if len(user.memory) == 0:
            user.memory.append([0,0])
        for coor in dict_data['listloc']:
            user.memory.append(coor.getArrPos())
        user.set_light_tor()
        textbox.insert(tk.END,f"\nUID: {user.uid}, MEM: {user.memory}, LIGHT: {user.light_tor}")
    elif dict_data['type'] == PKT_MOVE:
        user.memory[0] = dict_data['location'].getArrPos()
        textbox.insert(tk.END,f"\nUID: {user.uid}, MEM: {user.memory}")
    elif dict_data['type'] == PKT_SHOOT:
        user.shoot = dict_data['location'].getArrPos()
        textbox.insert(tk.END,f"\nUID: {user.uid}, Shoot: {user.shoot}")

def close_connect(key):
    sock = key.fileobj
    data = key.data
    print(f"Closing connection to uid: {data.uid}")
    textbox.insert(tk.END,f"Closing connection to uid: {data.uid}")
    sel.unregister(data)
    sock.close()

def sending_data(_type : int, user : User):
    uid = user.uid
    if _type == PKT_HELLO and game.status == SETUP:
        # if game.user1.status 
        if uid:
            yield pkt_accept(uid,True).sending_data()
            if user == game.get_user_1():
                listloc = config.ROW_1
                live_change(PKT_LOCATION_LIGHT, liveGUI.SIDE_LEFT, listloc=listloc)
                live_change(PKT_LOCATION_SHIP, liveGUI.SIDE_LEFT, listloc=config.SHIP_1)
            else:
                listloc = config.ROW_2
                live_change(PKT_LOCATION_LIGHT, liveGUI.SIDE_RIGHT, listloc=listloc)
                live_change(PKT_LOCATION_SHIP, liveGUI.SIDE_RIGHT, listloc=config.SHIP_2)
            yield pkt_player(id=uid, n=config.N, m=config.M, k=config.K,listloc=listloc).sending_data()
        else:
            yield pkt_accept(config.UNACCEPT, False).sending_data()
    elif _type == PKT_LOCATION_SHIP and game.status == SETUP:
        yield pkt_check_location(id=uid, check=config.CHECK).sending_data()

    elif _type == PKT_LOCATION_LIGHT and game.status == SETUP:
        yield pkt_check_location(id=uid, check=config.CHECK).sending_data()
        user.set_ready(True)
        if user == game.get_user_1():
            live_gui.set_default(liveGUI.SIDE_LEFT)
            live_change(PKT_LOCATION_LIGHT, liveGUI.SIDE_LEFT, arrloc=user.memory[1:])
            live_change(PKT_LOCATION_SHIP, liveGUI.SIDE_LEFT, loc=user.memory[0])
            live_gui.set_light_tor()
            live_change(PKT_TREASURE, liveGUI.SIDE_LEFT, loc=game.pos_treasure.getArrPos())
        else:
            live_gui.set_default(liveGUI.SIDE_RIGHT)
            live_change(PKT_LOCATION_LIGHT, liveGUI.SIDE_RIGHT, arrloc=user.memory[1:])
            live_change(PKT_LOCATION_SHIP, liveGUI.SIDE_RIGHT, loc=user.memory[0])
            live_gui.set_light_tor()
            live_change(PKT_TREASURE, liveGUI.SIDE_RIGHT, loc=game.pos_treasure.getArrPos())

        if game.check_ready():
            textbox.insert(tk.END,f"\nCa hai da san sang")
            textbox.insert(tk.END,f"\nVi tri cua kho bau: {game.pos_treasure}")
            send_sock(game.get_user_1(), pkt_treasure(config.TREASURE_LOCATION).sending_data())
            send_sock(game.get_user_2(), pkt_treasure(config.TREASURE_LOCATION).sending_data())
            game.status = PLAYING
            if connect2csg:
                asyncio.run(update(msg_begin(int(game_match))))

    elif _type == PKT_MOVE and game.status == PLAYING:
        if user == game.get_user_1():
            live_change(PKT_MOVE, liveGUI.SIDE_LEFT, loc=user.memory[0])
            other = game.get_user_2()
        else:
            live_change(PKT_MOVE, liveGUI.SIDE_RIGHT, loc=user.memory[0])
            other = game.get_user_1()
        
        if game.check_treasure(user):
            send_sock(other, pkt_lose(other.uid,PKT_WON_TREASURE).sending_data())
            send_sock(user, pkt_won(user.uid,PKT_WON_TREASURE).sending_data())
            game.status = END
            if connect2csg:
                if user.uid // 1000 == 1:
                    asyncio.run(update(msg_score(int(game_match),3,999,0)))
                else:
                    asyncio.run(update(msg_score(int(game_match),3,0,999)))
        else:
            send_sock(other,pkt_turn(other.uid).sending_data())
            pos, enemy_pos = game.sup_hanlde_collide(user, other)
                # send_sock(game.get_user_1(), pkt_location_ship(game.get_user_1().uid,Coordinates(pos[0],pos[1])).sending_data())

            if user == game.get_user_1():
                live_change(PKT_LOCATION_SHIP, liveGUI.SIDE_RIGHT, locen=pos)
                live_change(PKT_LOCATION_SHIP, liveGUI.SIDE_LEFT, locen=enemy_pos[0])
            else:
                live_change(PKT_LOCATION_SHIP, liveGUI.SIDE_LEFT, locen=pos)
                live_change(PKT_LOCATION_SHIP, liveGUI.SIDE_RIGHT, locen=enemy_pos[0])

            send_sock(other, pkt_location_ship(other.uid,Coordinates(pos[0],pos[1])).sending_data())
            send_sock(user, pkt_location_ship(user.uid,Coordinates(enemy_pos[0][0],enemy_pos[0][1])).sending_data())
            
            listloc=[]
            for [x, y] in enemy_pos[1:]:
                listloc.append(Coordinates(x,y))
            send_sock(user, pkt_location_light(user.uid, listloc).sending_data())
            if user == game.get_user_1():
                live_change(PKT_LOCATION_LIGHT, liveGUI.SIDE_LEFT, listlocen=listloc)
            else:
                live_change(PKT_LOCATION_LIGHT, liveGUI.SIDE_RIGHT, listlocen=listloc)


    elif _type == PKT_SHOOT and game.status == PLAYING:
        if user == game.get_user_1():
            other = game.get_user_2()
        else:
            other = game.get_user_1()

        if game.check_loc_shoot(user):
            if game.checkShoot(user, other) :
                textbox.insert(tk.END,f"\nUID: {other.uid} da bi ban trung")
                send_sock(other, pkt_lose(other.uid,PKT_WON_SHOOTED).sending_data())
                send_sock(user, pkt_won(user.uid,PKT_WON_SHOOTED).sending_data())
                game.status = END
                if connect2csg:
                    if user.uid // 1000 == 1:
                        asyncio.run(update(msg_score(int(game_match),3,999,0)))
                    else:
                        asyncio.run(update(msg_score(int(game_match),3,0,999)))
            else:
                send_sock(other,pkt_turn(other.uid).sending_data())
        else:
            yield pkt_check(user.uid, False).sending_data()


def live_change(_type, side, **kwargs):
    list_keys = kwargs.keys()
    if _type == PKT_HELLO and game.status == SETUP:
        pass
    elif _type == PKT_LOCATION_SHIP:
        if "listloc" in list_keys:
            live_gui.set_location_neo(side,kwargs['listloc'])
        if "loc" in list_keys:
            i,j = kwargs['loc']
            live_gui.set_location(side,ship = Coordinates(i,j))
        if "locen" in list_keys:
            i,j = kwargs['locen']
            print(i,j)
            live_gui.set_location(side,ship_en = Coordinates(i,j))
        pass
    elif _type == PKT_LOCATION_LIGHT:
        if "listloc" in list_keys:
            live_gui.set_location_light(side,kwargs['listloc'])
        if "arrloc" in list_keys:
            for i,j in kwargs['arrloc']:
                live_gui.set_location(side,light = Coordinates(i,j))
        if "listlocen" in list_keys:
            live_gui.set_light_en(side,kwargs['listlocen'])
        pass
    elif _type == PKT_MOVE and game.status == PLAYING:
        if "loc" in list_keys:
            live_gui.move(side, kwargs['loc'])
        pass
    elif _type == PKT_SHOOT and game.status == PLAYING:
        pass
    elif _type == PKT_TREASURE and game.status == SETUP:
        if "listloc" in list_keys:
            live_gui.set_location_trea(side,kwargs['listloc'])
        if "loc" in list_keys:
            i,j = kwargs['loc']
            live_gui.set_location(side,treasure = Coordinates(i,j))
        pass
        

def hanlde_collide():
    pass

def send_sock(user, mess):
    # sent = sock.send(mess)
    # print("sock",user.sock)
    user.sock.send(mess)
    # textbox.insert(tk.END,f"\nEchoing {unpack(mess)!r} to {user.uid}")
    dict_data = unpack(mess)
    textbox.insert(tk.END,f"\nEchoing to {user.uid}:")
    print(f"\nEchoing to {user.uid}:")
    for _key in dict_data.keys():
        textbox.insert(tk.END,f"   {str(_key) + ' : ' + str(dict_data[_key])}")
        print(f"   {str(_key) + ' : ' + str(dict_data[_key])}")
    pass


def main(host, port, _textbox:Text, liveGUI : liveGUI.Window, **kwargs):
    global textbox
    global game_match 
    global live_gui
    if not connect2csg:
        game.status = SETUP
    else:
        game.status = SET_MATCH

    live_gui = liveGUI

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print(f"Listening on {(host, port)}")
    textbox = _textbox
    textbox.insert(tk.END,f"\nListening on {(host, port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while isRunning:
            events = sel.select(timeout=5)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
        print("Stopped")
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()





# if mask & selectors.EVENT_WRITE:
#         if data.outb:
#             print(data.outb)
#             sdata = sending_data(check_type(data.outb))
#             print(f"Echoing {sdata!r} to {data.addr}")
#             textbox.insert(tk.END,f"Echoing {sdata!r} to {data.addr}")
#             sent = sock.send(sdata)  # Should be ready to write
#             data.outb = data.outb[sent:]