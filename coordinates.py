import random
import numpy as np

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPos(self):
        return self.x, self.y

def rand_list_coor():
    pass  

if __name__ == "__main__":
    a=np.random.randint(5,size=(5,2))
    print(a)

