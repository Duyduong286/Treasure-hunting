import random

SETUP = 1

class User:
    def __init__(self, id, ip):
        self.status = SETUP
        self.uid = id
        self.ip = ip

class Game:
    def __init__(self):
        self.status = SETUP

    def set_user_1(self, ip):
        id = 1000+random.randint(10,100)
        self.user1 = User(id, ip)

    def set_user_2(self, ip):
        id = 1000+random.randint(10,100)
        self.user2 = User(id, ip)