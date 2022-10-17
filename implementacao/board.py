from tile import TileFactory


class Board:
    def __init__(self, player, tiles) -> None:
        self.player = player
        self.matrix = tiles

class BoardFactory:

    @staticmethod
    def create(player) -> Board:
        matrix = TileFactory.create()
        return Board(player, matrix)