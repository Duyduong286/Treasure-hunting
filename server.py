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
    game.set_user_1(addr)

    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
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
            for pkt in sending_data(check_type(data.inb)):
                data.outb = pkt
                if data.outb:
                    print(f"Echoing {data.outb!r} to {data.addr}")
                    textbox.insert(tk.END,f"\nEchoing {data.outb!r} to {data.addr}")
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]
            data.inb = b""


def sending_data(_type):
    if _type == PKT_HELLO and game.status == SETUP:
        # if game.user1.status 
        yield pkt_accept(16855,True).sending_data()
        yield pkt_player(id=16855,n=20,m=5,k=2,location=Coordinates(1,2)).sending_data()
    elif _type == PKT_LOCATION_SHIP and game.status == SETUP:
        yield pkt_check_location(id=16855,check=1).sending_data()


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