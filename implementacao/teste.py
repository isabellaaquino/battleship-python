#from tile import Tile, TileState
from enum import Enum

#test = [[Tile(x, y, TileState.INITIAL) for x in range(0,8)] for y in range(0,8)]

# for column in test:
#     for item in column:
#         print (item, end='  '),
#     print()

class ShipType(Enum):
    PORTA_AVIOES = 5
    NAVIOS_TANQUE = 4,
    CONTRATORPEDEIRO = 3,
    SUBMARINO = 2,

print(ShipType(5).name)
