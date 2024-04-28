import asyncio

from PyQt6.QtCore import QObject, pyqtSignal
from qasync import asyncSlot

from src.core.board import Board
from src.core.http import HttpService
from src.core.settings_manager import SettingsManager


class UsersService(QObject):
    def __init__(self, sm: SettingsManager, api: HttpService):
        super().__init__()
        self._api = api
        self._sm = sm

        self._users: dict[str: User] = dict()

    async def get(self, uid: str):
        if uid in self._users:
            return self._users[uid]
        user = await self._api.get(f'users/{uid}')
        user = User(user)
        self._users[uid] = user
        return user


class User:
    def __init__(self, data):
        self.id = data.get('uuid')
        self.name = data.get('username')
