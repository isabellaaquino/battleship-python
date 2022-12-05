from typing import List, Tuple
from ship import Ship, ShipType
from player import Player
from tile import Tile, TileFactory, TileState
from operator import itemgetter


class Board:
    def __init__(self, player: Player, id: int) -> None:
        self.id = id
        self.player = player
        self.matrix = TileFactory.create()

    def get_id(self):
        return self.id

    def get_matrix(self) -> List[List[Tile]]:
        return self.matrix

    def get_tile(self, x, y) -> Tile:
        return self.matrix[x][y]

    def get_player(self):
        return self.player

    def create_ships(self, ship_tiles: List[List[int]]):
        instantiated_ships = []
        for ship in ship_tiles:
            ship_type = ShipType(len(ship)).name
            ship_instance = Ship(ship_type)
            instantiated_ships.append(ship_instance)
            ship_instance.set_player(self.get_player())
            tiles = []
            for coord in ship:
                tile = self.get_tile(coord[0], coord[1])
                tile.set_state(TileState.SHIP)
                tiles.append(tile)
            ship_instance.set_tiles(tiles)

        self.get_player().set_ships(instantiated_ships)

