import sys
import socket
import selectors
import types
from protocol import *
import tkinter as tk
from tkinter import Text
import random 
from Game import *

sel = selectors.DefaultSelector()
isRunning = True
game = Game()

def accept_wrapper(sock):
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
        recv_data = sock.recv(1024)  # Should be ready to read
        dict_data = unpack(recv_data)
        for _key in dict_data.keys():
            textbox.insert(tk.END,f"\n{str(_key) + ' : ' + str(dict_data[_key])}")
        data.inb = b""
        data.inb += recv_data
        # if check_type(recv_data) == 0 and game.status == SETUP:

        #         data.outb += recv_data
            # else:
            #     print(f"Closing connection to {data.addr}")
            #     sel.unregister(sock)
            #     sock.close()
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
            yield pkt_player(id=uid,n=20,m=20,k=8,location=Coordinates(4,0)).sending_data()
        else:
            yield pkt_accept(0,False).sending_data()
    elif _type == PKT_LOCATION_SHIP and game.status == SETUP:
        yield pkt_check_location(id=uid,check=1).sending_data()

    elif _type == PKT_LOCATION_LIGHT and game.status == SETUP:
        yield pkt_check_location(id=uid,check=1).sending_data()
        user.set_ready(True)
        if game.check_ready():
            textbox.insert(tk.END,f"Ca hai da san sang")
            send_sock(game.get_user_1(), pkt_treasure(Coordinates(18,8)).sending_data())
            send_sock(game.get_user_2(), pkt_treasure(Coordinates(18,8)).sending_data())
            game.status == PLAYING
    elif _type == PKT_MOVE and game.status == PLAYING:
        if user == game.get_user_1():
            send_sock(game.get_user_2(),pkt_turn(game.get_user_2().uid).sending_data())
        else:
            send_sock(game.get_user_1(),pkt_turn(game.get_user_1().uid).sending_data())

def send_sock(user, mess):
    # sent = sock.send(mess)
    print("sock",user.sock)
    user.sock.send(mess)
    textbox.insert(tk.END,f"\nEchoing {mess!r} to {user.id}")
    pass


def main(host, port, _textbox:Text):
    global textbox
    # host, port = "127.0.0.1", 12345
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