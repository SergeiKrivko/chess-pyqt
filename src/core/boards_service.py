import asyncio
from uuid import uuid4

from PyQt6.QtCore import QObject, pyqtSignal
from qasync import asyncSlot

from src.core.board import Board, Move, AvailableMove
from src.core.http import HttpService
from src.core.settings_manager import SettingsManager


class BoardsService(QObject):
    newBoard = pyqtSignal(object)
    boardDeleted = pyqtSignal(object)
    newMove = pyqtSignal(object)
    boardUpdated = pyqtSignal()

    def __init__(self, sm: SettingsManager, api: HttpService):
        super().__init__()
        self._api = api
        self._sm = sm

        self._boards: dict[str: dict] = dict()
        self._current = None

        self._now_moves = None
        self._available_moves = []

        self._last_move: Move | None = None
        self._last_last_move_id: str | None = None
        self._poll_id = None

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
    def is_owner(self):
        return self._sm.uid == self.board.owner

    @property
    def undo_available(self):
        if self._now_moves == 'white':
            return self._last_move is not None and self.is_black
        if self._now_moves == 'black':
            return self._last_move is not None and self.is_white
        return False

    @property
    def now_moves(self):
        return self._now_moves

    def run(self):
        self._download_boards()

    @asyncSlot()
    async def _download_boards(self):

        uid = self._sm.uid
        while uid == self._sm.uid:
            if self._current is None:
                res1 = await self._api.get(f"boards?owner={uid}")
                res2 = await self._api.get(f"boards?invited={uid}")
                for el in (res1 or []) + (res2 or []):
                    board = Board(el)
                    if board.id in self._boards:
                        continue

                    invitations = await self._api.get(f'invitations?board={board.id}')
                    if invitations:
                        board.code = invitations[0]['code']

                    self._boards[board.id] = board
                    self.newBoard.emit(board)

                if res1 is not None and res2 is not None:
                    ids = [el['uuid'] for el in res1 + res2]
                    for board_id in list(self._boards.keys()):
                        if board_id not in ids:
                            print(f"DELETE {board_id}")
                            self.boardDeleted.emit(board_id)
                            self._boards.pop(board_id)

            await asyncio.sleep(5)

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

    async def join(self, code: str):
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

    def clear(self):
        self.close()
        self._boards.clear()

    @asyncSlot()
    async def _poll(self):
        poll_id = self._poll_id = uuid4()
        await self._check_first_move()
        while self._poll_id == poll_id:
            await self._check_move()
            await self._update_board()
            await asyncio.sleep(3)

    async def _check_first_move(self):
        move = await self._api.get(f'moves/last?board={self._current}')
        self._last_last_move_id = None
        if not move:
            self._now_moves = 'white'
            self._last_move = None
        else:
            self._last_move = Move(move)
            self._now_moves = 'white' if self._last_move.actor == 'black' else 'black'

    async def _check_move(self):
        move = await self._api.get(f'moves/last?board={self._current}')
        move = None if move is None else Move(move)
        if move != self._last_move:
            if move is None and self._last_last_move_id is None or move.id == self._last_last_move_id:
                self._now_moves = 'white' if self._last_move.actor == 'white' else 'black'
                await self._update_board_state()
                self.newMove.emit(Move({
                    'actor': self._last_move.actor,
                    'src': self._last_move.dst,
                    'dst': self._last_move.src,
                }))
                self._last_move = None
            else:
                self._last_move = move
                self._now_moves = 'white' if move.actor == 'black' else 'black'
                await self._update_board_state()
                self.newMove.emit(move)
            self._available_moves.clear()

    async def _update_board(self):
        board = self.board
        if not board:
            return 
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

    async def _update_board_state(self):
        board = self.board
        resp = await self._api.get(f'boards/{self._current}')
        board.update_state(resp)

    async def upload_board(self, board: Board):
        await self._api.put(f'boards/{self._current}', {
            'mode': board.mode,
            'privacy': board.privacy,
            'invited': board.invited,
            'white': board.white,
            'black': board.black,
        })

    async def move(self, src, dst, promotion):
        if not self.move_required:
            print("Can not move now!")
            return
        move = await self._api.post(f'moves', dct := {
            'board': self._current,
            'actor': 'white' if self.is_white else 'black',
            'src': src,
            'dst': dst,
            'promotion': promotion or None,
        })
        if not move:
            return False
        self._now_moves = 'white' if self.is_black else 'black'
        dct['uuid'] = move
        self._last_move = Move(dct)
        await self._update_board_state()
        self.newMove.emit(self._last_move)
        self._available_moves.clear()
        return True

    async def undo_move(self):
        if not self.undo_available:
            print("Can not undo now!")
            return
        move = await self._api.delete(f'moves/last?board={self._current}')
        print(move)
        if not move:
            return False
        self._now_moves = 'white' if self.is_white else 'black'
        await self._update_board_state()
        self.newMove.emit(Move({
            'uuid': move,
            'src': self._last_move.dst,
            'dst': self._last_move.src,
            'actor': self._now_moves,
        }))
        self._last_move = None
        self._available_moves.clear()
        return True

    async def available_moves(self, src):
        if not self._available_moves:
            self._available_moves = await self._api.get(f'moves/legal?board={self._current}')
        return [AvailableMove(move) for move in filter(lambda m: m['src'] == src, self._available_moves)]
