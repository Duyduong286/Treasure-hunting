import random

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPos(self):
        return self.x, self.y

    def getArrPos(self):
        return [self.x, self.y]

    def __str__(self):
        return f"Pos: ({self.x}, {self.y})"

def rand_list_coor():
    pass  


