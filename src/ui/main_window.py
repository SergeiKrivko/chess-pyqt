from PyQtUIkit.widgets import KitMainWindow, KitTabLayout

from src.core.service import ApiService
from src.core.settings_manager import SettingsManager
from src.ui.auth import AuthScreen
from src.ui.board.game_screen import GameScreen
from src.ui.main import MainScreen
from src.ui.themes import THEMES


class MainWindow(KitMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 600)

        for key, item in THEMES.items():
            self.theme_manager.add_theme(key, item)
        self.set_theme('dark')
        self.theme_manager.add_icons('assets', 'custom')
        self.theme_manager.set_locales_path('src.locale')
        self.theme_manager.set_locale('ru', 'en')

        self._sm = SettingsManager()
        self._api = ApiService(self._sm)

        self._main_layout = KitTabLayout()
        self.setCentralWidget(self._main_layout)

        self._auth = AuthScreen(self._api)
        self._main_layout.addWidget(self._auth)

        self._main = MainScreen(self._sm, self._api)
        self._main_layout.addWidget(self._main)

        self._game_screen = GameScreen(self._sm, self._api)
        self._game_screen.closeRequested.connect(self._close_board)
        self._main_layout.addWidget(self._game_screen)

        self._api.userChanged.connect(self._on_user_changed)
        self._main.openBoardRequested.connect(self._open_board)

    def _on_user_changed(self, user_id):
        if user_id:
            self._main_layout.setCurrent(1)
        else:
            self._main_layout.setCurrent(0)

    def _open_board(self, board_id):
        self._api.boards.open(board_id)
        self._main_layout.setCurrent(2)
        self._game_screen.open()

    def _close_board(self):
        self._api.boards.close()
        self._main_layout.setCurrent(1)
