from enum import Enum
from typing import List

from tile import Tile, TileState


class ShipType(Enum):
    PORTA_AVIOES = {'name': 'Porta Aviões', 'size': 5},
    TESTE = {'name': 'Porta Aviões', 'size': 5},
    TESTE3 = {'name': 'Porta Aviões', 'size': 5},
    SUBMARINO = {'name': 'Porta Aviões', 'size': 5},

class Ship:

    def __init__(self, type: ShipType) -> None:
        self.type = type
        self.tiles = []

    def set_tiles(self, tiles: List[Tile]) -> None:
        self.tiles = tiles

    def get_type(self) -> ShipType:
        return self.type
    
    def is_alive(self):
        count = 0
        for tile in self.tiles:
            if tile.state == TileState.HIT:
                count +=1

        if count == self.get_type().size:
            return False
        else:
            return True
