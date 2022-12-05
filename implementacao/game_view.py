# 	Gameview matchStatus
# 1 - no match (initial state)
# 2 - finished match (game with winner)
# 3 - your turn, match in progress AND is setting ships
# 4 - your turn, match in progress AND is select tile
# 5 - NOT your turn, match in progress - waiting ships to be set
# 6 - NOT your turn, match in progress - waiting select tile move
# 7 - match abandoned by opponent

from operator import itemgetter
from tkinter import messagebox
from typing import List, Tuple
from board import Board
from ship import Ship, ShipType
from player import Player


def is_occupied(tile, selected_tiles: List[tuple]): # Helper function
    return [tile[0], tile[1]] in selected_tiles

class GameView:
    def __init__(self) -> None:
        self.match_status = 1
        
        # Creating players

        self.local_player = Player()
        self.remote_player = Player()

        self.local_player.initialize(1, "Local Player", "Local Player")
        self.remote_player.initialize(2, "Remote Player", "Remote Player")

        self.remote_board = Board(self.remote_player, 0) # Board ID 0 for remote (opponenent) board
        self.local_board = Board(self.local_player, 1) # Board ID 1 for local (playing user) board


    def get_match_status(self):
        return self.match_status 

    def get_status(self) -> str:
        """	
        Gameview matchStatus

        1 - no match (initial state)
        2 - finished match (game with winner)
        3 - your turn, match in progress AND is setting ships
        4 - your turn, match in progress AND is select tile
        5 - NOT your turn, match in progress - waiting ships to be set
        6 - NOT your turn, match in progress - waiting select tile move
        7 - match abandoned by opponent
        """
        turn_player = self.get_turn_player()

        if self.match_status == 2:
            return "Vencedor: " + self.get_winner_name()
        elif self.match_status == 3:
            return turn_player.get_name() + ", selecione ladrinhos para colocação de navios. Clique em 'Confirmar navios' quando finalizar."
        elif self.match_status == 4:
            return turn_player.get_name() + ", selecione um ladrilho para atirar."
        elif self.match_status == 5:
            return "Aguardando colocação de navios do adversário: " + self.remote_player.get_name()
        elif self.match_status == 6:
            return "Aguardando tiro do adversário: " + self.remote_player.get_name()
        elif self.match_status == 7:
            return "Adversário abandonou a partida"


    def get_winner_name(self):
        local_player = self.get_local_player()
        if local_player.is_winner:
            return local_player.get_name()
            
        return self.get_remote_player().get_name()

    def get_remote_board(self):
        return self.remote_board

    def set_match_status(self, status):
        self.match_status = status

    def start_match(self, players, local_player_id):
        playerA_name = players[0][0]
        playerA_id = players[0][1]
        playerA_order = players[0][2]
        playerB_name = players[1][0]
        playerB_id = players[1][1]
        self.local_player.reset()
        self.remote_player.reset()
        self.local_player.initialize(1, playerA_id, playerA_name)
        self.remote_player.initialize(2, playerB_id, playerB_name)
        if playerA_order == "1":
            self.local_player.toggle_turn()
            self.match_status = 3  #  Waiting for setting ships
        else:
            self.remote_player.toggle_turn()
            self.match_status = 5  #  waiting remote action

    def receive_withdrawal_notification(self):
        self.match_status = 7
    
    def reset_game(self):
        self.match_status = 1
        
        # Creating players

        self.local_player = Player()
        self.remote_player = Player()

        self.local_player.initialize(1, "Local Player", "Local Player")
        self.remote_player.initialize(2, "Remote Player", "Remote Player")

        self.remote_board = Board(self.remote_player, 0) # Board ID 0 for remote (opponenent) board
        self.local_board = Board(self.local_player, 1) # Board ID 1 for local (playing user) board

    def get_local_player(self) -> Player:
        return self.local_player

    def get_remote_player(self) -> Player:
        return self.remote_player

    def is_local_player_turn(self) -> bool:
        return self.get_local_player().get_turn()

    def get_turn_player(self) -> Player:
        if self.get_local_player().get_turn():
            return self.local_player
        else:
            return self.remote_player

    def get_receiving_move_player(self) -> Player:
        if self.get_local_player().get_turn():
            return self.remote_player
        else:
            return self.local_player

    def get_local_board(self) -> Board:
        return self.local_board

    def get_remote_board(self) -> Board:
        return self.remote_board

    def is_local_board_id(self, id):
        # 0 - remote (opponent) board
        # 1 - local (playing user) board
        return id == self.get_local_board().get_id()

    def is_remote_board_id(self, id):
        # 0 - remote (opponent) board
        # 1 - local (playing user) board
        return id == self.get_remote_board().get_id()


    @staticmethod
    def is_tiles_sum_valid(selected_tiles: List[tuple]) -> bool:
        """
        PORTA_AVIOES x1 = 5x1 = 5 
        NAVIOS_TANQUE x1 = 4x1 = 4
        CONTRATORPEDEIRO x1 = 3x1 = 3
        SUBMARINO x2 = 2x2 = 4

        TOTAL = 5 + 4 + 3 + 4 = 16
        """
        return len(selected_tiles) == 16

    @staticmethod
    def are_there_ships_close(selected_tiles: List[List[int]]) -> bool:
        """
        This method will check if are there are any ships placed next to each other
        """

        selected_tiles = sorted(selected_tiles, key=itemgetter(1)) # Sorting by y first
        selected_tiles = sorted(selected_tiles, key=itemgetter(0)) # Sorting by x after

        for i in range(len(selected_tiles)):
            try:
                current_ship = []
                x = selected_tiles[0][0]
                y = selected_tiles[0][1]

                right_tile = [x, y+1]
                bottom_tile = [x+1, y]

                if right_tile in selected_tiles:
                    current_ship.append([x,y]) 
                    while is_occupied(right_tile, selected_tiles): # Checking if the ship was horizontally placed
                        bottom_tile = [right_tile[0]+1, right_tile[1]]
                        if is_occupied(bottom_tile, selected_tiles):
                            return True # There are ships close
                        current_ship.append((right_tile))

                        right_tile = [right_tile[0], right_tile[1]+1] # Gets the next bottom tile
                        if not is_occupied(right_tile, selected_tiles):# If the next tile is not occupied, break the ship loop 
                            for tile in current_ship:
                                selected_tiles.remove(tile) # Removes the tile so we don't have to do the verification again on the closing loop
                            break

                elif bottom_tile in selected_tiles:
                    current_ship.append([x,y]) 
                    while is_occupied(bottom_tile, selected_tiles): # Checking if the ship was horizontally placed
                        right_tile = [bottom_tile[0], bottom_tile[1]+1]
                        if is_occupied(right_tile, selected_tiles):
                            return True # There are ships close
                        current_ship.append((bottom_tile))
                        
                        bottom_tile = [bottom_tile[0]+1, bottom_tile[1]] # Gets the next bottom tile
                        if not is_occupied(bottom_tile, selected_tiles): # If the next tile is not occupied, break the ship loop
                            for tile in current_ship:
                                selected_tiles.remove(tile) # Removes the tile so we don't have to do the verification again on the closing loop
                            break

                else: # Single ship tile, therefore invalid
                    return True
            
            except IndexError: 
                break
        return False

    @staticmethod
    def are_all_ships_placed(selected_tiles: List[Tuple[int, int]]) -> Tuple[bool, List[Ship]]:
        """
        This method will check if all the required ships were placed in a setting of ships.
        
        SHIPS TYPES COUNT:

        PORTA_AVIOES x1 
        NAVIOS_TANQUE x1 
        CONTRATORPEDEIRO x1 
        SUBMARINO x2 
        """

        # Sorting selected tiles
        selected_tiles = sorted(selected_tiles, key=itemgetter(1)) # Sorting by y first
        selected_tiles = sorted(selected_tiles, key=itemgetter(0)) # Sorting by x after

        ships = []

        for i in range(len(selected_tiles)):
            current_ship = []
            try:
                x = selected_tiles[0][0]
                y = selected_tiles[0][1]
                current_ship.append([x,y])

                right_tile = [x, y+1]
                bottom_tile = [x+1, y]

                """
                Since there are no ships close (as checked previously),
                only one of these verifications below will be true,
                so we can have only one while loop.
                """
                if right_tile in selected_tiles:
                    direction = 'right'
                    current_tile = right_tile
                
                elif bottom_tile in selected_tiles:
                    direction = 'bottom'
                    current_tile = bottom_tile
                
                count = 1

                while is_occupied(current_tile, selected_tiles): # Checking if the ship was horizontally placed
                    count += 1
                    if count > 5:
                        return False, None # If the count surpasses 5, it means there is a ship longer than 5, which doesn't exist
                    current_ship.append((current_tile)) # Appends the chain of tiles to the current ship
                    
                    if direction == 'right':
                        current_tile = [current_tile[0], current_tile[1]+1] # Gets the next right tile
                    else:
                        current_tile = [current_tile[0]+1, current_tile[1]] # Gets the next bottom tile

                    if not is_occupied(current_tile, selected_tiles):  # If the next tile is not occupied, it means the ship ended
                        for tile in current_ship:
                            selected_tiles.remove(tile) # Removes the tiles so we don't have to do the verification again on the closing loop
                        ships.append(current_ship)
                        break
            
            except IndexError: 
                break

        ships_types = []
        for ship in ships:
            ship_type = ShipType(len(ship)).name
            """
            Since we are not actually manipulating the board yet,
            we append a tuple of the instance of the ship and the list of tiles coordinates
            that belong to it, so it can be retrieved later by the board.
            """
            ships_types.append(ship_type)

        # Checking count of each ship type:
        if ships_types.count(ShipType.SUBMARINO.name) != 2:
            return False, None

        if ships_types.count(ShipType.CONTRATORPEDEIRO.name) != 1:
            return False, None

        if ships_types.count(ShipType.NAVIOS_TANQUE.name) != 1:
            return False, None

        if ships_types.count(ShipType.PORTA_AVIOES.name) != 1:
            return False, None

        return True, ships # Tuple return so we can get the instantiated ships by the board


    def evaluate_end_of_match(self) -> bool:
        turn_player = self.get_local_player()
        player = self.get_receiving_move_player()
        ships = player.get_ships()

        if any([ship.is_alive for ship in ships]):
            return False
        else:
            turn_player.set_as_winner()
            return True
    
    def reset_game(self):
        self.match_status = 1
        
        # Creating players

        self.local_player = Player()
        self.remote_player = Player()

        self.local_player.initialize(1, "Local Player", "Local Player")
        self.remote_player.initialize(2, "Remote Player", "Remote Player")

        self.remote_board = Board(self.remote_player, 0) # Board ID 0 for remote (opponen) board
        self.local_board = Board(self.local_player, 1) # Board ID 1 for local (playing user) board

        