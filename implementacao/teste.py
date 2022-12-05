#from tile import Tile, TileState
from enum import Enum
from tile import Tile, TileState

from ship import Ship

#test = [[Tile(x, y, TileState.INITIAL) for x in range(0,8)] for y in range(0,8)]

# for column in test:
#     for item in column:
#         print (item, end='  '),
#     print()

class ShipType(Enum):
    PORTA_AVIOES = 5
    NAVIOS_TANQUE = 4
    CONTRATORPEDEIRO = 3
    SUBMARINO = 2

ships = []

teste = Ship(ShipType.CONTRATORPEDEIRO)
teste.set_tiles([Tile(0,0, TileState.HIT), Tile(0,1, TileState.HIT), Tile(0,2, TileState.HIT)])
ships.append(teste)

teste2 = Ship(ShipType.CONTRATORPEDEIRO)
teste2.set_tiles([Tile(0,0, TileState.SHIP), Tile(0,1, TileState.HIT), Tile(0,2, TileState.HIT)])
ships.append(teste2)

print([ship.is_alive for ship in ships])

if any([ship.is_alive for ship in ships]):
    print('existem navios vivos')
else:
    print('nao existem navios vivos')


