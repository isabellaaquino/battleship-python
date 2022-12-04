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

    def create_ships(self, instantiated_ships: List[Tuple[Ship, List[List[int]]]]):
        for i in range(len(instantiated_ships)):
            ship = instantiated_ships[i][0]
            ship.set_player(self.get_player())
            tiles_coords = instantiated_ships[i][1]
            tiles = []
            for coord in tiles_coords:
                tile = self.get_tile(coord[0], coord[1])
                tile.update_status(TileState.SHIP)
                tiles.append(tile)
            ship.set_tiles(tiles)


"""
TEST FUNCTIONS
"""


# def is_occupied(tile, selected_tiles: List[tuple]):
#     return (tile[0], tile[1]) in selected_tiles

# def are_all_ships_placed(selected_tiles: List[tuple]):
#     # Sorting selected tiles
#     selected_tiles = sorted(selected_tiles, key=itemgetter(1)) # Sorting by y first
#     selected_tiles = sorted(selected_tiles, key=itemgetter(0)) # Sorting by x after

#     ships = []

#     for i in range(len(selected_tiles)):
#         current_ship = []
#         try:
#             x, y = selected_tiles[i]
#             current_ship.append((x,y))

#             right_tile = (x+1, y)
#             bottom_tile = (x, y+1)

#             """
#             Since there are no ships close (as checked previously),
#             only one of these verifications below will be true,
#             so we can have only one while loop.
#             """
#             if right_tile in selected_tiles:
#                 direction = 'right'
#                 current_tile = right_tile
            
#             elif bottom_tile in selected_tiles:
#                 direction = 'bottom'
#                 current_tile = bottom_tile
            
#             count = 1

#             while is_occupied(current_tile, selected_tiles): # Checking if the ship was horizontally placed
#                 count += 1
#                 if count > 5:
#                     return False # If the count surpasses 5, it means there is a ship longer than 5, which doesn't exist
#                 current_ship.append((current_tile)) # Appends the chain of tiles to the current ship
                
#                 if direction == 'right':
#                     current_tile = (current_tile[0]+1, current_tile[1]) # Gets the next right tile
#                 else:
#                     current_tile = (current_tile[0], current_tile[1]+1) # Gets the next bottom tile

#                 if not is_occupied(current_tile, selected_tiles): # If the next tile is not occupied, it means the ship ended
#                     selected_tiles.remove(tile for tile in current_ship) # Removes the tiles so we don't have to do the verification again on the closing loop
#                     ships.append(current_ship)
#                     break
        
#         except IndexError: 
#             break

#     instantiated_ships = [] # To be reused on creating ships if they are valid
#     ships_types = []
#     for ship in ships:
#         ship_type = ShipType(len(ship)).name
#         """
#         Since we are not actually manipulating the board yet,
#         we append a tuple of the instance of the ship and the list of tiles coordinates
#         that belong to it, so it can be retrieved later by the board.
#         """
#         instantiated_ships.append((Ship(ship_type), ship)) 
#         ships_types.append(ship_type)

#     # Checking count of each ship type:
#     if ships_types.count(ShipType.SUBMARINO) != 2:
#         return False

#     if ships_types.count(ShipType.CONTRATORPEDEIRO) != 1:
#         return False

#     if ships_types.count(ShipType.NAVIOS_TANQUE) != 1:
#         return False

#     if ships_types.count(ShipType.PORTA_AVIOES) != 1:
#         return False

#     return True, instantiated_ships # Tuple return so we can get the instantiated ships by the board

# def are_there_ships_close(selected_tiles: List[tuple]):
#     # Sorting selected tiles
#     selected_tiles = sorted(selected_tiles, key=itemgetter(1)) # Sorting by y first
#     selected_tiles = sorted(selected_tiles, key=itemgetter(0)) # Sorting by x after

#     for i in range(len(selected_tiles)):
#         try:
#             current_ship = []
#             x, y = selected_tiles[i]

#             right_tile = (x+1, y)
#             bottom_tile = (x, y+1)


#             if right_tile in selected_tiles:
#                 while is_occupied(right_tile, selected_tiles): # Checking if the ship was horizontally placed
#                     bottom_tile = (right_tile[0], right_tile[1]+1)
#                     if is_occupied(bottom_tile, selected_tiles):
#                         return True # There are ships close
#                     current_ship.append((right_tile))

#                     right_tile = (right_tile[0]+1, right_tile[1]) # Gets the next bottom tile
#                     if not is_occupied(right_tile, selected_tiles): # If the next tile is not occupied, break the ship loop
#                         selected_tiles.remove(tile for tile in current_ship) # Removes the tile so we don't have to do the verification again on the closing loop
#                         break

#             elif bottom_tile in selected_tiles:
#                 while is_occupied(bottom_tile, selected_tiles): # Checking if the ship was horizontally placed
#                     right_tile = (bottom_tile[0]+1, bottom_tile[1])
#                     if is_occupied(right_tile, selected_tiles):
#                         return True # There are ships close
#                     current_ship.append((right_tile))
                     
#                     bottom_tile = (bottom_tile[0], bottom_tile[1]+1) # Gets the next bottom tile
#                     if not is_occupied(bottom_tile, selected_tiles): # If the next tile is not occupied, break the ship loop
#                         selected_tiles.remove(tile for tile in current_ship) # Removes the tile so we don't have to do the verification again on the closing loop
#                         break

#             else: # Single ship tile, therefore invalid
#                 return True
        
        
#         except IndexError: 
#             break
#     return False
