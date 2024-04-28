from enum import Enum


class Figure:
    class Type:
        BISHOP = 'bishop'
        ROOK = 'rook'
        QUEEN = 'queen'
        KNIGHT = 'knight'
        KING = 'king'
        PAWN = 'pawn'

    class Player:
        WHITE = 'white'
        BLACK = 'black'

    def __init__(self, figure: str, pos: str, player: str):
        self.type = figure
        self.pos = pos.lower()
        self.player = player

    def move(self, pos: str):
        self.pos = pos.lower()

    @property
    def x(self):
        return 'abcdefgh'.index(self.pos[0])

    @property
    def y(self):
        return int(self.pos[1]) - 1


