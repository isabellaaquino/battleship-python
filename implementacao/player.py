from typing import List
from ship import Ship


class Player:

    def __init__(self, identifier: str, ships: List[Ship]) -> None:
        self.identifier = identifier
        self.alive_ships = ships
        