from PyQt6.QtCore import pyqtSignal
from PyQtUIkit.widgets import *

from src.core.service import ApiService
from src.core.settings_manager import SettingsManager
from src.ui.main.my_boards import MyBoardsScreen


class MainScreen(KitHBoxLayout):
    openBoardRequested = pyqtSignal(object)

    def __init__(self, sm: SettingsManager, service: ApiService):
        super().__init__()
        self._sm = sm
        self._service = service

        self._nav = KitNavigation()
        self._nav.addTab("My boards", 'solid-apps')
        self._nav.addTab("Public boards", 'solid-people')
        self._nav.addTab("Settings", 'solid-settings')
        self.addWidget(self._nav)

        self._tab_layout = KitTabLayout()
        self.addWidget(self._tab_layout)

        self._my_boards = MyBoardsScreen(self._sm, self._service)
        self._my_boards.openBoardRequested.connect(self.openBoardRequested.emit)
        self._tab_layout.addWidget(self._my_boards)

