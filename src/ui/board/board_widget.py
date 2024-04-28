from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QSizePolicy
from PyQtUIkit.widgets import KitHBoxLayout, KitVBoxLayout, KitGridLayout, KitIconWidget, KitLayoutButton

from src.core.figure import Figure
from src.ui.board.figure_widget import FigureWidget


class BoardWidget(KitHBoxLayout):
    figSelected = pyqtSignal(Figure)
    figDeselected = pyqtSignal()
    moveSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._size = min(self.width(), self.height()) // 8 * 8

        v_layout = KitVBoxLayout()
        self.addWidget(v_layout)

        self.__moves = []

        self.__cages: dict[str: Cage] = dict()

        self.__grid = KitGridLayout()
        self.__grid.setMaximumSize(self._size, self._size)
        v_layout.addWidget(self.__grid)
        for i in range(8):
            for j in range(8):
                cage = Cage(i, j)
                self.__cages[pos := f"{'abcdefgh'[j]}{i + 1}"] = cage
                cage.on_click = lambda x, p=pos: self._on_click(p)
                self.__grid.addWidget(cage, i, j)

        self.__figures: dict[str, FigureWidget] = {}

    def add_figure(self, figure: Figure):
        widget = FigureWidget(figure)
        self.__figures[figure.pos] = widget
        widget.setParent(self.__grid)
        widget.set_size(self._size // 8)
        widget._set_tm(self._tm)
        widget.clicked.connect(self._on_click)
        widget.show()

    def move_figure(self, src, dst):
        if src not in self.__figures:
            return
        fig = self.__figures[src]
        fig.set_pos(dst, anim=True)
        if dst in self.__figures:
            self.__figures[dst].setParent(None)
        self.__figures[dst] = fig
        self.__figures.pop(src)

    def _on_click(self, pos):
        if self.__moves:
            if pos in self.__moves:
                self.moveSelected.emit(pos)
            else:
                self.figDeselected.emit()
                self.hide_available_moves()
                if pos in self.__figures:
                    self.figSelected.emit(self.__figures[pos].figure)
            self.hide_available_moves()
        elif pos in self.__figures:
            self.figSelected.emit(self.__figures[pos].figure)

    def show_available_moves(self, src, moves: list):
        for cage in self.__cages.values():
            cage.set_not_available()
        self.__cages[src].set_move_this()
        if src in moves:
            moves.remove(src)
        for move in moves:
            if move in self.__figures:
                self.__cages[move].set_eat_available()
            else:
                self.__cages[move].set_move_available()
        self.__moves = moves

    def hide_available_moves(self):
        for cage in self.__cages.values():
            cage.set_not_available()
        self.__moves.clear()

    def clear(self):
        for el in self.__figures.values():
            el.hide()
            el.setParent(None)
        self.__figures.clear()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._size = min(self.width(), self.height()) // 8 * 8
        self.__grid.setMaximumSize(self._size, self._size)
        for el in self.__figures.values():
            el.set_size(self._size // 8)

    def _set_tm(self, tm):
        super()._set_tm(tm)
        for widget in self.__figures.values():
            widget._set_tm(tm)

    def _apply_theme(self):
        super()._apply_theme()
        for widget in self.__figures.values():
            widget._apply_theme()


class Cage(KitLayoutButton):
    def __init__(self, row, col):
        super().__init__()
        self.radius = 0
        self.border = 0
        if (row + col) % 2 == 0:
            self.main_palette = 'CageWhite'
        else:
            self.main_palette = 'CageBlack'
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._move_this = KitIconWidget('solid-add-circle')
        self._move_this.main_palette = 'Success'
        self._move_this.setFixedSize(30, 30)
        self._move_this.hide()
        self.addWidget(self._move_this)

        self._move_available = KitIconWidget('solid-add-circle')
        self._move_available.main_palette = 'Warning'
        self._move_available.setFixedSize(30, 30)
        self._move_available.hide()
        self.addWidget(self._move_available)

        self._eat_available = KitIconWidget('solid-add-circle')
        self._eat_available.main_palette = 'Danger'
        self._eat_available.setFixedSize(30, 30)
        self._eat_available.hide()
        self.addWidget(self._eat_available)

    def set_move_this(self):
        self._eat_available.hide()
        self._move_available.hide()
        self._move_this.show()

    def set_move_available(self):
        self._move_this.hide()
        self._eat_available.hide()
        self._move_available.show()

    def set_eat_available(self):
        self._move_this.hide()
        self._move_available.hide()
        self._eat_available.show()

    def set_not_available(self):
        self._move_this.hide()
        self._move_available.hide()
        self._eat_available.hide()
