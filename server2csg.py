import asyncio
import websockets
import json
import socket

PORT=3456
MATCH = []
ARR_MATCH = []
STATUS = 1
IP = "localhost"
class match():
    def __init__(self, match, id1, id2, passwd):
        self.match = match
        self.id1 = id1
        self.id2 = id2
        self.passwd = passwd

    def __str__(self) -> str:
        return f"'match': {self.match}, 'id1': {self.id1}, 'id2': {self.id2}, 'passwd': {self.passwd}"

def msg_info(ip, port):
    return {
        "result" : 1,
        "ip" : ip,
        "port" : port,
        "path" : "path"
    }

# msg = {
#     "result" : 2,
#     "match" : MATCH,
#     "status" : 1,
#     "id1" : 100,
#     "id2" : 1000
# }

def msg_begin(match):
    return {
        "result" : 1,
        "match" : match 
    }

def msg_end(match) :
    return {
        "result" : 3,
        "match" : match
        }

def msg_score(match,status,sc1,sc2) :
    return {
        "result" : 2,
        "match" : match,
        "status" : status,
        "id1" : sc1,
        "id2" : sc2
    }

def msg_err(match):
    return {
        "result" : 0,
        "match" : match
    }

async def echo(websocket):
    async for message in websocket:
        data = json.loads(message)
        print(data)
        if data["action"] == 1:
            new_match = match(match=data["match"], id1=data["id1"], id2=data["id2"], passwd=data["passwd"])
            ARR_MATCH.append(new_match)
            send_match(str(data["match"]))
            print("arr_match: ")
            for i in ARR_MATCH:
                print(i)
            await websocket.send(json.dumps(msg_info(ip=game_info[0], port=game_info[1])))
        elif data["action"] == 2:
            check = True
            for mat in ARR_MATCH:
                if data["match"] == mat:
                    check = False
                    await websocket.send(json.dumps(msg_score(mat,1,0,0)))
            if check:
                await websocket.send(json.dumps(msg_err(mat)))

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

def main_run(ip, port):
    global game_info
    game_info = [ip, port]
    asyncio.run(main())

def send_match(game_match : str):
    client_socket = socket.socket()  
    client_socket.connect(('127.0.0.1', PORT)) 
    client_socket.send(game_match.encode())
    client_socket.close()

async def update(data):
    async with websockets.connect("ws://104.194.240.16/ws/channels/") as websocket:
        await websocket.send(json.dumps(data))
        # await websocket.recv()

# def msg_update() {
#     "result" : 2,
#     "match" : 22,
#     "status" : 1,
#     "id1" : 100,
#     "id2" : 1000
# }


# def update_status():
