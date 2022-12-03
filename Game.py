import random
from coordinates import Coordinates

SETUP = 1
PLAYING = 2
END = 3

class User:
    def __init__(self, id, ip):
        self.status = SETUP
        self.uid = id
        self.ip = ip
        self.is_ready = False
        self.sock = None
        self.memory = [0]
        self.light_tor = [] #only torch
        self.shoot = [-1,-1]

    def set_light_tor(self):
        for PosX, PosY in self.memory[1:]:
            for i in range(PosX-1, PosX+2):
                for j in range(PosY-1, PosY+2):
                    if [i, j] not in self.light_tor:
                        self.light_tor.append([i, j])

    def set_sock(self, sock):
        self.sock = sock

    def set_ready(self, is_ready):
        self.is_ready = is_ready

    def get_pos(self):
        return self.memory[0][0], self.memory[0][1]

class Game:
    def __init__(self):
        self.status = SETUP
        self.users = [None, None]
        Posx = random.randint(18,19)
        Posy = random.randint(8,12)
        self.pos_treasure = Coordinates(Posx,Posy)

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

    # def hanlde_collide():
    #     user_1, user_2 = self.get_user()
    
    def sup_hanlde_collide(self, user : User, enemy : User):
        ship_light = [] 
        PosX, PosY = enemy.get_pos()
        for i in range(PosX-1, PosX+2):
            for j in range(PosY-1, PosY+2):
                ship_light.append([i,j])
        
        pos = [-1,-1]
        if user.memory[0] in enemy.light_tor or user.memory[0] in ship_light:
            pos = user.memory[0]
        
        enemy_pos = [[-1,-1]]
        PosX, PosY = user.memory[0]
        for i in range(PosX-1, PosX+2):
            for j in range(PosY-1, PosY+2):
                if [i, j] == enemy.memory[0]:
                    enemy_pos[0] = [i,j]
                    continue
                if [i, j] in enemy.memory[1:]:
                    enemy_pos.append([i,j])

        if enemy.memory[0] in user.light_tor:
            enemy_pos[0] = enemy.memory[0]

        # if user.memory[0] in enemy.light_tor:
        #     enemy_pos.append([i,j])

        return pos, enemy_pos

    def checkShoot(self, user : User, enemy : User):
        return user.shoot == enemy.memory[0] and user.shoot != [-1,-1]

    def check_loc_shoot(self, user : User):
        _range = 6
        x, y = user.memory[0]
        if x >=0 and y >= 0 :
            if user.shoot in user.memory :
                return False
            if user.shoot[0] - x <= _range and user.shoot[1] - y <= _range:
                return True
    
        return False

    def check_treasure(self, user : User):
        ship_light = []
        PosX, PosY = user.memory[0]
        for i in range(PosX-1, PosX+2):
            for j in range(PosY-1, PosY+2):
                ship_light.append([i,j])

        return self.pos_treasure.getArrPos() in  ship_light
        

        


