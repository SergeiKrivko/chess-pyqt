import aiohttp
from PyQt6.QtCore import QObject, pyqtSignal

from src import config
from src.core.settings_manager import SettingsManager


class AuthService(QObject):
    userChanged = pyqtSignal()

    def __init__(self, sm: SettingsManager):
        super().__init__()
        self._sm = sm

        self._session = aiohttp.ClientSession(config.API_URL)

    async def auth(self, login, password):
        resp = await self._session.post('/api/v1/authentication', json={
            'username': login,
            'password': password,
        })
        resp = await resp.json()
        resp = resp['data']

        self._sm.set('access_token', resp['access_token'])
        self.userChanged.emit()
        self._sm.set('user_id', resp['user_uuid'])

        return resp

    async def create_user(self, login, password):
        resp = await self._session.post('/api/v1/users', json={
            'username': login,
            'password': password,
            'roles': [],
        })
        resp = await resp.json()
        print(resp)
        self._sm.set('user_login', login)
        return resp

