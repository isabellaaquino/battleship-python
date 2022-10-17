# 	Gameview matchStatus
# 1 - no match (initial state)
# 2 - finished match (game with winner)
# 3 - your turn, match in progress AND is setting ships
# 4 - your turn, match in progress AND is select tile
# 5 - NOT your turn, match in progress - waiting ships to be set
# 6 - NOT your turn, match in progress - waiting select tile move
# 7 - match abandoned by opponent

class GameView:
    def __init__(self) -> None:
        pass