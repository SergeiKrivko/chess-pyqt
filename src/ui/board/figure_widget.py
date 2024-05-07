from PyQt6.QtCore import QPoint, QPropertyAnimation, QEasingCurve, pyqtSignal, Qt
from PyQtUIkit.widgets import KitIconWidget

from src import config
from src.core.figure import Figure


class FigureWidget(KitIconWidget):
    clicked = pyqtSignal(str)

    def __init__(self, fig: Figure, inversion: bool):
        super().__init__()
        self._fig = fig
        self._inversion = inversion
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
        self.__anim = False
        self.set_pos(self._fig.pos)

    def set_pos(self, pos, anim=False):
        self._fig.move(pos)

        if isinstance(self.__anim, QPropertyAnimation):
            self.__anim.stop()

        if anim:
            self.__anim = QPropertyAnimation(self, b'pos')
            self.__anim.setEndValue(QPoint(self._pos()))
            self.__anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.__anim.setDuration(config.MOVE_DURATION)
            self.__anim.start()
        else:
            self.move(self._pos())

    @property
    def figure(self):
        return self._fig

    def mousePressEvent(self, a0):
        super().mousePressEvent(a0)
        if a0.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._fig.pos)

    def set_size(self, size):
        self._size = size
        self.move(self._pos())
        self.setFixedSize(self._size, self._size)
        self.update()

    def _pos(self):
        if self._inversion:
            return QPoint((7 - self._fig.x) * self._size, (7 - self._fig.y) * self._size)
        return QPoint(self._fig.x * self._size, self._fig.y * self._size)
