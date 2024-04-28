import asyncio
import uuid

import aiohttp
from PyQt6.QtCore import QObject


class HttpService(QObject):
    def __init__(self):
        super().__init__()

        self._session: aiohttp.ClientSession | None = None
        self._url = '/api/v1'

        self._user_token = ''

        self._auth_id = None

    @staticmethod
    def _print_detail(url, resp):
        print(repr(url), resp.get('detail'))
        # print(resp)

    async def set_token(self, token):
        if self._session:
            await self._session.close()
        self._user_token = token
        self._session = aiohttp.ClientSession('http://localhost:8000', headers={
            'content-type': 'application/json',
            'authorization': f'Bearer {self._user_token}'
        })
        self._auth_id = uuid.uuid4()

    async def get(self, url):
        async with self._session.get(f'{self._url}/{url}') as response:
            res = await response.json()
            self._print_detail(url, res)
            return res.get('data')

    async def post(self, url, data):
        async with self._session.post(f'{self._url}/{url}', json=data) as response:
            res = await response.json()
            self._print_detail(url, res)
            return res.get('data')

    async def put(self, url, data):
        async with self._session.put(f'{self._url}/{url}', json=data) as response:
            res = await response.json()
            self._print_detail(url, res)
            return res.get('data')

    async def delete(self, url):
        async with self._session.delete(f'{self._url}/{url}') as response:
            res = await response.json()
            self._print_detail(url, res)
            return res.get('data')

    async def poll(self, url, step=1):
        if not self._auth_id:
            return
        auth_id = self._auth_id
        while auth_id == self._auth_id:
            res = await self.get(url)
            yield res
            await asyncio.sleep(step)
