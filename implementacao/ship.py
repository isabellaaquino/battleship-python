from enum import Enum
from typing import List

from tile import Tile, TileState


class ShipType(Enum):
    PORTA_AVIOES = 5
    NAVIOS_TANQUE = 4,
    CONTRATORPEDEIRO = 3,
    SUBMARINO = 2,

class Ship:

    def __init__(self, type: ShipType) -> None:
        self.type = type
        self.tiles = []

    def get_tiles(self) -> List[Tile]:
        return self.tiles

    def set_tiles(self, tiles: List[Tile]) -> None:
        self.tiles = tiles

    def get_type(self) -> ShipType:
        return self.type
    
    @property
    def is_alive(self) -> bool:
        # Check if all the tiles were hit
        tiles_states = [tile.state for tile in self.get_tiles()]
        # The quantity of hit tiles is the same of the ship size
        if tiles_states.count(TileState.HIT) == self.get_type().value[0]:
            return False
        else:
            return True
