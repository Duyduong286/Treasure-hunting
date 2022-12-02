import random

SETUP = 1
PLAYING = 2

class User:
    def __init__(self, id, ip):
        self.status = SETUP
        self.uid = id
        self.ip = ip
        self.is_ready = False
        self.sock = None

    def set_sock(self, sock):
        self.sock = sock

    def set_ready(self, is_ready):
        self.is_ready = is_ready

class Game:
    def __init__(self):
        self.status = SETUP
        self.users = [None, None]

    def set_user(self, ip):
        id = 1000+random.randint(10,100)
        if not self.users[0]:
            self.users[0] = User(id, ip)
            return id, self.users[0]
        elif not self.users[1]:
            id += 1000
            self.users[1] = User(id, ip)
            return id, self.users[1]
        return 0, None

    def get_user(self):
        return self.users[0], self.users[1]

    def get_user_1(self) -> User:
        return self.users[0]

    def get_user_2(self) -> User:
        return self.users[1]

    def remove_user(self, index):
        self.users[index] = None

    def check_ready(self):
        user_1, user_2 = self.get_user()
        try:
            check = user_1.is_ready and user_2.is_ready
        except:
            return False
        return check

    def check_slot(self):
        user_1, user_2 = self.get_user()
        if user_1 and user_2 :
            return True
        return False
