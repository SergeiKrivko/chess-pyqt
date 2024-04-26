from PyQtUIkit.widgets import KitMainWindow, KitVBoxLayout

from src.core.figure import Figure
from src.ui.board import Board
from src.ui.themes import THEMES


class MainWindow(KitMainWindow):
    def __init__(self):
        super().__init__()

        for key, item in THEMES.items():
            self.theme_manager.add_theme(key, item)
        self.set_theme('dark')
        self.theme_manager.add_icons('assets', 'custom')

        main_layout = KitVBoxLayout()
        self.setCentralWidget(main_layout)

        self._board = Board()
        main_layout.addWidget(self._board)

        self._board.add_figure(Figure(Figure.Type.BISHOP, 0, 0, Figure.Player.WHITE))
        self._board.add_figure(Figure(Figure.Type.KING, 0, 5, Figure.Player.BLACK))
