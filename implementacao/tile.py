from enum import Enum
from typing import List


from utils import coord_letters

class TileStateOptions(Enum):
    WATER = 'Water'
    WATER_MISS = 'Miss'
    SHIP = 'Ship'
    HIT = 'Hit'


class Tile:
    
    def __init__(self, x: int, y: int , state: TileStateOptions) -> None:
        self.x = x
        self.y = y
        self.state = state

    def __repr__(self) -> str:
        return f'[X: {self.x} Y: {self.y}]'

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_state(self) -> TileStateOptions:
        return self.state

    def set_state(self, state: TileStateOptions):
        self.state = state


class TileFactory:

    @staticmethod
    def create() -> List[List[Tile]]:
        return [[Tile(x, y, TileStateOptions.WATER) for x in range(0,8)] for y in range(0,8)] 
