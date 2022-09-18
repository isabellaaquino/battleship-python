from tile import Tile, TileState

test = [[Tile(x, y, TileState.INITIAL) for x in range(0,8)] for y in range(0,8)]

for column in test:
    for item in column:
        print (item, end='  '),
    print()