from enum import Enum
from typing import List
from board import Board


from utils import coord_letters

class TileState(Enum):
    WATER = 'Water'
    WATER_MISS = 'Miss'
    SHIP = 'Ship'
    HIT = 'Hit'


class Tile:
    
    def __init__(self, x: int, y: int , state: TileState) -> None:
        self.x = x
        self.y = y
        self.state = state

    def __repr__(self) -> str:
        return f'[X: {self.x} Y: {self.y}]'

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_state(self) -> TileState:
        return self.state

    def set_state(self, state: TileState):
        self.state = state

    def right_occupied(self, board: Board) -> bool:
        matrix = board.get_matrix()
        try:
            is_occupied = matrix[self.x][self.y+1].get_state() == TileState.SHIP
            return is_occupied
        except IndexError:
            return False
    
    def top_occupied(self, board: Board) -> bool:
        matrix = board.get_matrix()
        try:
            is_occupied = matrix[self.x-1][self.y].get_state() == TileState.SHIP
            return is_occupied
        except IndexError:
            return False
    
    def bottom_occupied(self, board: Board) -> bool:
        matrix = board.get_matrix()
        try:
            is_occupied = matrix[self.x+1][self.y].get_state() == TileState.SHIP
            return is_occupied
        except IndexError:
            return False

    def left_occupied(self, board: Board) -> bool:
        matrix = board.get_matrix()
        try:
            is_occupied = matrix[self.x][self.y-1].get_state() == TileState.SHIP
            return is_occupied
        except IndexError:
            return False

class TileFactory:

    @staticmethod
    def create() -> List[List[Tile]]:
        return [[Tile(x, y, TileState.WATER) for x in range(0,8)] for y in range(0,8)] 
