

from typing import List

from ship import Ship


class Player:

    def __init__(self) -> None:
        self.identifier = ""
        self.name = ""
        self.symbol = None
        self.is_turn = False
        self.is_winner = False
        self.ships = []

    def initialize(self, symbol, id, name): # TODO - finish
        self.reset()
        self.symbol = symbol
        self.identifier = id
        self.name = name

    def get_ships(self) -> List[Ship]:
        return self.ships

    def set_ships(self, ships: List[Ship]):
        self.ships = ships

    def get_turn(self) -> bool:
        return self.is_turn

    def get_name(self) -> str:
        return self.name

    def get_symbol(self) -> str:
        return self.symbol

    def toggle_turn(self):
        if self.is_turn == False:
            self.is_turn = True
        elif self.is_turn == True:
            self.is_turn = False

    def set_as_winner(self):
        self.is_winner = True

    def reset(self):
        self.identifier = ""
        self.name = ""
        self.is_turn = False
        self.is_winner = False
        self.ships = []
