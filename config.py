from coordinates import *
DEFAULT = 0
ACCEPT = 1
UNACCEPT = 0
CHECK = 1
WON = 2

DEFAULT_N = 20
DEFAULT_M = 60
DEFAULT_K = 8

DEFAULT_LOCATION = Coordinates(-1,-1)
DEFAULT_LOCATION_PLAYER = Coordinates(4,0)
DEFAULT_TREASURE_LOCATION = Coordinates(18,8)

N = DEFAULT_N
M = DEFAULT_M
K = DEFAULT_K
LOCATION_PLAYER = DEFAULT_LOCATION_PLAYER

TREASURE_LOCATION = DEFAULT_TREASURE_LOCATION

ROW_1_1 = [Coordinates(4,i) for i in range(0,20)]
ROW_2_1 = [Coordinates(8,i) for i in range(0,20)]
ROW_3_1 = [Coordinates(12,i) for i in range(0,20)]

ROW_1 = []
ROW_1.extend(ROW_1_1)
ROW_1.extend(ROW_2_1)
ROW_1.extend(ROW_3_1)

ROW_1_2 = [Coordinates(6,i) for i in range(0,20)]
ROW_2_2 = [Coordinates(10,i) for i in range(0,20)]
ROW_3_2 = [Coordinates(14,i) for i in range(0,20)]

ROW_2 = []
ROW_2.extend(ROW_1_2)
ROW_2.extend(ROW_2_2)
ROW_2.extend(ROW_3_2)

SHIP_1_1 = [Coordinates(0,i) for i in range(0,5)]
SHIP_2_1 = [Coordinates(1,i) for i in range(0,5)]

SHIP_1 = []
SHIP_1.extend(SHIP_1_1)
SHIP_1.extend(SHIP_2_1)

SHIP_1_2 = [Coordinates(0,i) for i in range(15,20)]
SHIP_2_2 = [Coordinates(1,i) for i in range(15,20)]

SHIP_2 = []
SHIP_2.extend(SHIP_1_2)
SHIP_2.extend(SHIP_2_2)

DOM = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4]]
TREA = [Coordinates(8 + i,18 + j) for i,j in DOM]