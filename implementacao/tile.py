from enum import Enum
from typing import List


from utils import coord_letters

class TileStateOptions(Enum):
    INITIAL = 'Inicial'
    WATER = 'Água'
    HIT = 'Acerto'

class Tile:
    
    def __init__(self, x: int, y:int , state: TileStateOptions, player: 'Player') -> None: # TODO - Add player class
        self.x = x
        self.y = y
        self.state = state
        self.player = player # Probably not necessary as a parameter


class TileFactory:

    @staticmethod
    def create() -> List[List[Tile]]:
        matrix = {letter: [Tile(x,y, TileStateOptions.INITIAL) for x,y in range(1,9)] for letter in coord_letters}  # Dict option - no need for mapper
        matrix_ = [[coord for coord in range(1,9)] for x in range(0,8)]  # List option
