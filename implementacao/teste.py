from tile import Tile, TileStateOptions

test = [[Tile(x, y, TileStateOptions.INITIAL) for x in range(0,8)] for y in range(0,8)]

for column in test:
    for item in column:
        print (item, end='  '),
    print()