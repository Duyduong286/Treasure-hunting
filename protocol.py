import socket
import sys
import struct
import math
from coordinates import Coordinates

PKT_HELLO = 0
PKT_ACCEPT = 1
PKT_PLAYER = 2
PKT_LOCATION_SHIP = 3
PKT_CHECK_LOCATION = 4
PKT_TREASURE = 5
PKT_LOCATION_LIGHT = 6
PKT_TURN = 7
PKT_MOVE = 8
PKT_SHOOT = 9
PKT_CHECK = 10

MIN_SIZE = 10

class Header:
    header_len = 8
    def __init__(self, type : int, length : int):
        self.type = type
        self.length = length

class Packet:
    def __init__(self, header : Header, **kwargs):
        self.header = header
        if kwargs:
            list_keys = kwargs.keys()
            if "id" in list_keys:
                self.id = kwargs["id"]
            if "accept" in list_keys:
                self.accept = kwargs["accept"]
            if "check" in list_keys:
                self.n = kwargs["check"]
            if "n" in list_keys:
                self.n = kwargs["n"]
            if "m" in list_keys:
                self.m = kwargs["m"]
            if "k" in list_keys:
                self.k = kwargs["k"]
            if "location" in list_keys:
                self.location = kwargs["location"]
            if "listloc" in list_keys:
                self.location = kwargs["listloc"]
    
    def sending_data(self):
        return packed_little_endian_data(self.header.type, self.header.length, self.__dict__.values())

def packed_little_endian_data(_type : int, length : int, dict_data : dict):
    data = struct.pack('ii', _type, length)
    for item in dict_data:
        if type(item) == int:
            data += struct.pack('i', item)
        if type(item) == Coordinates:
            data += struct.pack('i', item.x)
            data += struct.pack('i', item.y)
        if type(item) == list:
            for i in item:
                if type(i) == int:
                    data += struct.pack('i', i)
                if type(i) == Coordinates:
                        data += struct.pack('i', i.x)
                        data += struct.pack('i', i.y)
    return data

def unpacked_little_endian_data(length : int, lit_data):
    return struct.unpack('i'*(length // 4), lit_data)

def check_type(mess) -> NotImplementedError:
    return unpacked_little_endian_data(length=4,lit_data=mess[0:4])[0]

def pkt_hello() -> Packet:
    header = Header(type=PKT_HELLO, length=0)
    return Packet(header=header)

def unpkt_hello(mess) -> Packet:
    header = Header(type=PKT_HELLO, length=0)
    data = unpacked_little_endian_data(length=8,lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
    }

def pkt_accept(id : int, accept : bool) -> Packet:
    acc = 1 if accept else 0
    header = Header(type=PKT_ACCEPT, length=8)
    return Packet(header=header, id=id, accept=acc)

def unpkt_accept(mess) -> dict:
    data = unpacked_little_endian_data(length=16,lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
        "id" : data[2],
        "accept" : data[3]
    }

def pkt_player(id : int, n : int, m : int, k : int, location : Coordinates) -> Packet:
    #m vi tri o co the chon
    #n kich thuoc ban do
    #k so luong o chon
    header = Header(type=PKT_PLAYER, length=24)      

    return Packet(header=header, id=id, n=n, m=m, k=k, location=location)

def unpkt_player(mess) -> dict:
    data = unpacked_little_endian_data(length=32, lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
        "id" : data[2],
        "n" : data[3],
        "m" : data[4],
        "k" : data[5],
        "location" : Coordinates(data[6], data[7])
    }

def pkt_location_ship(id : int, location : Coordinates) -> Packet:
    header = Header(type=PKT_LOCATION_SHIP, length=12)
    return Packet(header=header, id=id, location=location)

def unpkt_location_ship(mess) -> dict:
    data = unpacked_little_endian_data(length=20, lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
        "id" : data[2],
        "location" : Coordinates(data[3], data[4])
    }

def pkt_check_location(id : int, check : int) -> Packet:
    header = Header(type=PKT_CHECK_LOCATION, length=8)
    return Packet(header=header, id=id, check=check)

def unpkt_check_location(mess) -> dict:
    data = unpacked_little_endian_data(length=16, lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
        "id" : data[2],
        "check" : data[3]
    }

def pkt_treasure(location : Coordinates) -> Packet:
    header = Header(type=PKT_TREASURE, length=8)
    return Packet(header=header, location=location)

def unpkt_treasure(mess):
    data = unpacked_little_endian_data(length=16, lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
        "location" : Coordinates(data[2],data[3])
    }

def pkt_location_light(id : int, listloc : list) -> Packet:
    k=len(listloc)
    header = Header(type=PKT_LOCATION_LIGHT, length=4*k*2)
    return Packet(header=header, id=id, listloc=listloc) 

def unpkt_location_light(mess) -> dict:
    data = unpacked_little_endian_data(length=len(mess), lit_data=mess)
    k = (len(mess)-12)/8
    listloc = []
    for i in range(0,int(k)+2,2):
        listloc.append(Coordinates(data[3+i],data[4+i]))

    return {
        "type" : data[0],
        "len" : data[1],
        "id" : data[2],
        "listloc" : listloc
    }

def pkt_turn(id : int) -> Packet:
    header = Header(type=PKT_TURN, length=4)
    return Packet(header=header, id=id)

def unpkt_turn(mess) -> Packet:
    data = unpacked_little_endian_data(length=12, lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
        "id" : data[2]
    }

def pkt_move(id : int, location : Coordinates) -> Packet:
    header = Header(type=PKT_MOVE, length=12)
    return Packet(header=header, id=id, location=location)

def unpkt_move(mess) -> dict:
    data = unpacked_little_endian_data(length=20, lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
        "id" : data[2],
        "location" : Coordinates(data[3], data[4])
    }

def pkt_shoot(id : int, location : Coordinates) -> Packet:
    header = Header(type=PKT_SHOOT, length=12)
    return Packet(header=header, id=id, location=location)

def unpkt_shoot(mess) -> dict:
    data = unpacked_little_endian_data(length=20, lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
        "id" : data[2],
        "location" : Coordinates(data[3], data[4])
    }

def pkt_check(id : int, accept : bool) -> Packet:
    acc = 1 if accept else 0
    header = Header(type=PKT_CHECK, length=4)
    return Packet(header=header, id=id, accept=acc)

def unpkt_check(mess) -> dict:
    data = unpacked_little_endian_data(length=16,lit_data=mess)
    return {
        "type" : data[0],
        "len" : data[1],
        "id" : data[2],
        "check" : data[3]
    }

def unpack(mess):
    chk_type = check_type(mess)
    if chk_type == 0:
        return unpkt_hello(mess)
    elif chk_type == 1:
        return unpkt_accept(mess)
    elif chk_type == 2:
        return unpkt_player(mess)
    elif chk_type == 3:
        return unpkt_location_ship(mess)
    elif chk_type == 4:
        return unpkt_check_location(mess)
    elif chk_type == 5:
        return unpkt_treasure(mess)
    elif chk_type == 6:
        return unpkt_location_light(mess)
    elif chk_type == 7:
        return unpkt_turn(mess)
    elif chk_type == 8:
        return unpkt_move(mess)
    elif chk_type == 9:
        return unpkt_shoot(mess)
    elif chk_type == 10:
        return unpkt_check(mess)







































if __name__ == "__main__":
    # pkt = pkt_check(11,True)
    # print(pkt.sending_data())
    # print(check_type(b'\x00\x00\x00\x00\x00\x00\x00\x00'))

    # pkt = pkt_accept(1,True,5)
    # print(pkt.sending_data())
    # print(unpack(pkt.sending_data()))
    # pkt = pkt_player(id=1,n=20,m=5,k=2,location=Coordinates(1,2))
    # print(pkt.sending_data())
    # print(len(pkt.sending_data()))
    # print(unpack(pkt.sending_data())['location'].getPos())

    # tor1 = Coordinates(1,1)
    # tor2 = Coordinates(1,3)
    # tor3 = Coordinates(5,4)

    # listtor = [tor1, tor2, tor3]

    # pkt = pkt_location_light(id=1111,listloc=listtor)
    # print(pkt.sending_data())
    # print(unpack(mess=pkt.sending_data()))
    # for i in unpack(mess=pkt.sending_data())['listloc']:
    #     print(i.getPos())

    pkt = pkt_treasure()
    print(pkt.sending_data())
    print(unpack(pkt.sending_data())['location'].getPos())