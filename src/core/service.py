from PyQt6.QtCore import QObject, pyqtSignal
from qasync import asyncSlot

from src.core.auth import AuthService
from src.core.boards_service import BoardsService
from src.core.http import HttpService
from src.core.settings_manager import SettingsManager
from src.core.users_service import UsersService


class ApiService(QObject):
    userChanged = pyqtSignal(object)

    def __init__(self, sm: SettingsManager):
        super().__init__()
        self._sm = sm

        self.http = HttpService()
        self.auth = AuthService(self._sm)
        self.boards = BoardsService(self._sm, self.http)
        self.users = UsersService(self._sm, self.http)

        self.auth.userChanged.connect(self._on_user_changed)

        self._on_user_changed()

    @asyncSlot()
    async def _on_user_changed(self):
        await self.http.set_token(self._sm.get('access_token'))
        self.userChanged.emit(self._sm.get('user_id'))

        self.boards.run()
