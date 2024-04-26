from enum import Enum


class Figure:
    class Type(Enum):
        BISHOP = 1
        ROOK = 2
        QUEEN = 3
        KNIGHT = 4
        KING = 5
        PAWN = 6

    class Player(Enum):
        WHITE = 1
        BLACK = 2

    def __init__(self, figure: Type, x, y, player: Player):
        self.type = figure
        self.x = x
        self.y = y
        self.player = player

    def move(self, x, y):
        self.x = x
        self.y = y
