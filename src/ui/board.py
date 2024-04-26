from PyQtUIkit.widgets import KitHBoxLayout, KitVBoxLayout, KitIconWidget, KitGridLayout

from src.core.figure import Figure
from src.ui.figure_widget import FigureWidget


class Board(KitHBoxLayout):
    def __init__(self):
        super().__init__()
        self._size = min(self.width(), self.height()) // 8 * 8

        v_layout = KitVBoxLayout()
        self.addWidget(v_layout)

        self.__grid = KitGridLayout()
        self.__grid.setMaximumSize(self._size, self._size)
        v_layout.addWidget(self.__grid)
        for i in range(8):
            for j in range(8):
                self.__grid.addWidget(Cage(i, j), i, j)

        self.__figures = []

    def add_figure(self, figure: Figure):
        widget = FigureWidget(figure)
        widget.set_size(self._size // 8)
        self.__figures.append(widget)
        widget.setParent(self.__grid)
        widget._set_tm(self._tm)

    def move_figure(self):
        pass

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._size = min(self.width(), self.height()) // 8 * 8
        self.__grid.setMaximumSize(self._size, self._size)
        for el in self.__figures:
            el.set_size(self._size // 8)

    def _set_tm(self, tm):
        super()._set_tm(tm)
        for widget in self.__figures:
            widget._set_tm(tm)

    def _apply_theme(self):
        super()._apply_theme()
        for widget in self.__figures:
            widget._apply_theme()


class Cage(KitHBoxLayout):
    def __init__(self, row, col):
        super().__init__()
        self.radius = 0
        if (row + col) % 2 == 0:
            self.main_palette = 'CageWhite'
        else:
            self.main_palette = 'CageBlack'
