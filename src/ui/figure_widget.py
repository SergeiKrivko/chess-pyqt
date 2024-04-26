from PyQt6.QtCore import QPoint, QPropertyAnimation, QEasingCurve
from PyQtUIkit.widgets import KitIconWidget

from src.core.figure import Figure


class FigureWidget(KitIconWidget):
    def __init__(self, fig: Figure):
        super().__init__()
        self._fig = fig
        self._size = 0
        self.setContentsMargins(10, 10, 10, 10)
        match self._fig.type:
            case Figure.Type.BISHOP:
                self.icon = 'custom-bishop'
            case Figure.Type.ROOK:
                self.icon = 'custom-rook'
            case Figure.Type.QUEEN:
                self.icon = 'custom-queen'
            case Figure.Type.KNIGHT:
                self.icon = 'custom-knight'
            case Figure.Type.KING:
                self.icon = 'custom-king'
            case Figure.Type.PAWN:
                self.icon = 'custom-pawn'

        if self._fig.player == Figure.Player.WHITE:
            self.main_palette = 'FigureWhite'
        else:
            self.main_palette = 'FigureBlack'

        self.set_size(64)
        self._anim = Figure
        # self.set_pos(4, 4, anim=True)

    def set_pos(self, x, y, anim=False):
        self._fig.move(x, y)

        if isinstance(self._anim, QPropertyAnimation):
            self._anim.stop()

        if anim:
            self._anim = QPropertyAnimation(self, b'pos')
            self._anim.setEndValue(QPoint(self._pos()))
            self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            self._anim.setDuration(1000)
            self._anim.start()
        else:
            self.move(self._pos())

    def set_size(self, size):
        self._size = size
        self.move(self._pos())
        self.setFixedSize(self._size, self._size)
        self.update()

    def _pos(self):
        return QPoint(self._fig.x * self._size, self._fig.y * self._size)
