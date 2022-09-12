from tile import TileFactory


class Board:
    def __init__(self, player, tiles) -> None:
        self.player = player
        self.tiles = tiles


class BoardFactory:

    @staticmethod
    def create(player) -> Board:
        tiles = TileFactory.create()