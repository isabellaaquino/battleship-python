from typing import List
from ship import Ship


class Player:

    def __init__(self, name: str, ships: List[Ship]) -> None:
        self.name = name
        self.alive_ships = ships
        