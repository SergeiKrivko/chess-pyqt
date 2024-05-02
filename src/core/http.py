import asyncio
import uuid

import aiohttp
from PyQt6.QtCore import QObject

from src import config


class HttpService(QObject):
    def __init__(self):
        super().__init__()

        self._session: aiohttp.ClientSession | None = None
        self._url = '/api/v1'

        self._user_token = ''

        self._auth_id = None

    @staticmethod
    def _print_detail(m: str, url, resp):
        print(m.upper(), repr(url), resp.get('detail'))
        # print(resp)

    async def set_token(self, token):
        if self._session:
            await self._session.close()
        self._user_token = token
        self._session = aiohttp.ClientSession(config.API_URL, headers={
            'content-type': 'application/json',
            'authorization': f'Bearer {self._user_token}'
        })
        self._auth_id = uuid.uuid4()

    async def get(self, url):
        try:
            async with self._session.get(f'{self._url}/{url}') as response:
                res = await response.json()
                self._print_detail('get', url, res)
                return res.get('data')
        except aiohttp.ServerDisconnectedError:
            return None
        except aiohttp.ClientConnectionError:
            return None

    async def post(self, url, data):
        try:
            async with self._session.post(f'{self._url}/{url}', json=data) as response:
                res = await response.json()
                self._print_detail('post', url, res)
                return res.get('data')
        except aiohttp.ServerDisconnectedError:
            return None
        except aiohttp.ClientConnectionError:
            return None

    async def put(self, url, data):
        try:
            async with self._session.put(f'{self._url}/{url}', json=data) as response:
                res = await response.json()
                self._print_detail('put', url, res)
                return res.get('data')
        except aiohttp.ServerDisconnectedError:
            return None
        except aiohttp.ClientConnectionError:
            return None

    async def delete(self, url):
        try:
            async with self._session.delete(f'{self._url}/{url}') as response:
                res = await response.json()
                self._print_detail('delete', url, res)
                return res.get('data')
        except aiohttp.ServerDisconnectedError:
            return None
        except aiohttp.ClientConnectionError:
            return None

    async def poll(self, url, step=1):
        if not self._auth_id:
            return
        auth_id = self._auth_id
        while auth_id == self._auth_id:
            res = await self.get(url)
            yield res
            await asyncio.sleep(step)
