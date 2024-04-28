from PyQt6.QtCore import Qt, pyqtSignal
from PyQtUIkit.themes.locale import KitLocaleString
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src.core.board import Board
from src.core.service import ApiService
from src.core.settings_manager import SettingsManager


class MyBoardsScreen(KitVBoxLayout):
    openBoardRequested = pyqtSignal(object)

    def __init__(self, sm: SettingsManager, api: ApiService):
        super().__init__()
        self._sm = sm
        self._api = api

        self.spacing = 6
        self.padding = 10

        top_layout = KitHBoxLayout()
        top_layout.spacing = 6
        self.addWidget(top_layout)

        self._button_new = KitButton(KitLocaleString.new)
        self._button_new.setFixedSize(60, 24)
        self._button_new.on_click = lambda: self._new_game()
        top_layout.addWidget(self._button_new)

        group = KitHGroup()
        group.setFixedSize(200, 24)
        top_layout.addWidget(group)

        self._line_edit = KitLineEdit()
        group.addItem(self._line_edit)

        self._button_join = KitButton(KitLocaleString.join)
        self._button_join.on_click = lambda: self._join()
        group.addItem(self._button_join)

        self._scroll_area = KitScrollArea()
        self._scroll_area.main_palette = 'Bg'
        self.addWidget(self._scroll_area)

        scroll_layout = KitVBoxLayout()
        scroll_layout.alignment = Qt.AlignmentFlag.AlignTop
        scroll_layout.spacing = 6
        self._scroll_area.setWidget(scroll_layout)

        scroll_layout.addWidget(KitLabel(KitLocaleString.owner + ':'))
        self._owner_layout = KitVBoxLayout()
        self._owner_layout.spacing = 2
        scroll_layout.addWidget(self._owner_layout)

        scroll_layout.addWidget(KitLabel(KitLocaleString.invited + ':'))
        self._invited_layout = KitVBoxLayout()
        self._invited_layout.spacing = 2
        scroll_layout.addWidget(self._invited_layout)

        self._api.boards.newBoard.connect(self.add_board)

    def add_board(self, board: Board):
        if board.owner == self._sm.get('user_id'):
            item = GameItem(self._api, board, True)
            self._owner_layout.addWidget(item)
        else:
            item = GameItem(self._api, board, False)
            self._invited_layout.addWidget(item)
        item.on_click = lambda: self.openBoardRequested.emit(board.id)

    @asyncSlot()
    async def _new_game(self):
        await self._api.boards.new()

    @asyncSlot()
    async def _join(self):
        await self._api.boards.join(self._line_edit.text)


class GameItem(KitLayoutButton):
    def __init__(self, api: ApiService, board: Board, is_owner: bool):
        super().__init__()
        self._api = api
        self._board = board
        self._is_owner = is_owner

        self.main_palette = 'Main'
        self.spacing = 6
        self.radius = 8
        self.border = 0
        self.setContentsMargins(7, 0, 7, 0)
        self.setFixedHeight(30)

        self._label = KitLabel(board.id)
        self.addWidget(self._label)

        self.addWidget(KitHBoxLayout(), 100)

        self._owner_label = KitLabel(board.owner)
        self._owner_label.hide()
        self.addWidget(self._owner_label)

        self._invitation_code_widget = KitHGroup()
        self._invitation_code_widget.hide()
        self._invitation_code_widget.height = 24
        self.addWidget(self._invitation_code_widget)

        self._code_line = KitLineEdit()
        self._code_line.setReadOnly(True)
        self._invitation_code_widget.addItem(self._code_line)

        self._button_copy_code = KitIconButton('solid-copy')
        self._button_copy_code.size = 24
        self._button_copy_code.on_click = lambda: KitApplication.clipboard().setText(self._code_line.text)
        self._invitation_code_widget.addItem(self._button_copy_code)

        self.on_click = lambda: print(self._label.text)

        self.load()

    @asyncSlot()
    async def load(self):
        if self._is_owner:
            self._invitation_code_widget.show()
            self._code_line.text = self._board.code
        else:
            self._owner_label.show()
            user = await self._api.users.get(self._board.owner)
            self._owner_label.text = user.name

