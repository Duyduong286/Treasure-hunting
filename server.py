import sys
import socket
import selectors
import types
from protocol import *
import tkinter as tk
from tkinter import Text
import random 

sel = selectors.DefaultSelector()
isRunning = True

def accept_wrapper(sock, textbox):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    textbox.insert(tk.END,f"\nAccepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(data.outb)
            sdata = sending_data(check_type(data.outb))
            print(f"Echoing {sdata!r} to {data.addr}")
            sent = sock.send(sdata)  # Should be ready to write
            data.outb = data.outb[sent:]

def sending_data(_type):
    if _type == 0:
        return pkt_accept(16855,True,random.randint(20, 25)).sending_data()


def main(host, port, textbox:Text):
    # host, port = "127.0.0.1", 12345
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print(f"Listening on {(host, port)}")
    textbox.insert(tk.END,f"\nListening on {(host, port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while isRunning:
            events = sel.select(timeout=5)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj, textbox)
                else:
                    service_connection(key, mask)
        print("Stopped")
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()