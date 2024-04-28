import asyncio

from PyQt6.QtCore import QObject, pyqtSignal
from qasync import asyncSlot

from src.core.board import Board, Move
from src.core.http import HttpService
from src.core.settings_manager import SettingsManager


class BoardsService(QObject):
    newBoard = pyqtSignal(object)
    newMove = pyqtSignal(object)
    boardUpdated = pyqtSignal()

    def __init__(self, sm: SettingsManager, api: HttpService):
        super().__init__()
        self._api = api
        self._sm = sm

        self._boards: dict[str: dict] = dict()
        self._current = None

        self._now_moves = None

        self._last_move: Move | None = None
        self._las_last_move_id: str | None = None

    @property
    def board(self) -> Board | None:
        if not self._current:
            return None
        return self._boards[self._current]

    @property
    def move_required(self):
        if self._now_moves == 'white':
            return self.is_white
        if self._now_moves == 'black':
            return self.is_black
        return False

    @property
    def is_white(self):
        return self._sm.uid == self.board.white

    @property
    def is_black(self):
        return self._sm.uid == self.board.black

    @property
    def now_moves(self):
        return self._now_moves

    def run(self):
        self._download_boards()

    @asyncSlot()
    async def _download_boards(self):
        while True:
            if self._current is None:
                res1 = await self._api.get(f"boards?owner={self._sm.uid}")
                res2 = await self._api.get(f"boards?invited={self._sm.uid}")
                for el in res1 + res2:
                    board = Board(el)
                    if board.id in self._boards:
                        continue
                    self._boards[board.id] = board
                    self.newBoard.emit(board)
            await asyncio.sleep(2)

    async def new(self):
        board_id = await self._api.post('boards', {
            'owner': self._sm.uid,
            'mode': 'online',
            'privacy': 'private'
        })
        invitation_code = await self._api.post('invitations', {
            'board': board_id,
        })

        board = await self._api.get(f'boards/{board_id}')
        self._boards[board_id] = board = Board(board)
        self.newBoard.emit(board)
        board.code = invitation_code
        return board_id, invitation_code

    async def enroll(self, code: str):
        invitation = await self._api.get(f'invitations/{code}')

        await self._api.post(f"boards/{invitation['board']}/invited", {
            'invitation': code,
            'invited': self._sm.uid,
        })

    def open(self, board_id):
        self._current = board_id
        self._poll()

    def close(self):
        self._current = None

    @asyncSlot()
    async def _poll(self):
        board_id = self._current
        while self._current == board_id:
            await self._check_move()
            await self._update_board()
            await asyncio.sleep(1)

    async def _check_move(self):
        move = await self._api.get(f'moves/last?board={self._current}')
        if not move:
            if self.board.white == self._sm.uid and not self.move_required:
                self._now_moves = 'white'
                self.newMove.emit(None)
            return
        move = Move(move)
        if move != self._last_move:
            if move.id == self._las_last_move_id:
                pass
            else:
                self._last_move = move
                self._now_moves = 'white' if move.actor == 'black' else 'black'
                self.newMove.emit(move)

    async def _update_board(self):
        board = self.board
        resp = await self._api.get(f'boards/{self._current}')

        flag = False
        if resp.get('owner') != board.owner:
            board.owner = resp.get('owner')
            flag = True
        if resp.get('invited') != board.invited:
            board.invited = resp.get('invited')
            flag = True
        if resp.get('white') != board.white:
            board.white = resp.get('white')
            flag = True
        if resp.get('black') != board.black:
            board.black = resp.get('black')
            flag = True

        if flag:
            self.boardUpdated.emit()

    async def upload_board(self, board: Board):
        await self._api.put(f'boards/{self._current}', {
            'mode': board.mode,
            'privacy': board.privacy,
            'invited': board.invited,
            'white': board.white,
            'black': board.black,
        })

    async def move(self, src, dst):
        if not self.move_required:
            print("Can not move now!")
            return
        self._now_moves = 'white' if self.is_black else 'black'
        move = await self._api.post(f'moves', dct := {
            'board': self._current,
            'actor': 'white' if self.is_white else 'black',
            'src': src,
            'dst': dst,
        })
        dct['uuid'] = move
        self._last_move = Move(dct)
        self.newMove.emit(self._last_move)

    async def available_moves(self, srs):
        # moves = await self._api.get(f'moves/available?board={self._current}')
        return [f"{'abcdefgh'[i]}{j + 1}" for i in range(8) for j in range(8)]
