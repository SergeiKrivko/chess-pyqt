import asyncio

from PyQt6.QtCore import pyqtSignal
from PyQtUIkit.themes.locale import KitLocaleString
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src import config
from src.core.board import Board, Move
from src.core.figure import Figure
from src.core.service import ApiService
from src.core.settings_manager import SettingsManager
from src.ui.board.board_widget import BoardWidget


class GameScreen(KitHBoxLayout):
    closeRequested = pyqtSignal()

    def __init__(self, sm: SettingsManager, api: ApiService):
        super().__init__()
        self._sm = sm
        self._api = api
        self._loading = False
        self._fig = None

        self.padding = 10
        self.spacing = 10

        right_layout = KitVBoxLayout()
        right_layout.spacing = 6
        right_layout.setFixedWidth(200)
        self.addWidget(right_layout)

        top_layout = KitHBoxLayout()
        top_layout.spacing = 6
        right_layout.addWidget(top_layout)

        self._button_back = KitIconButton('line-arrow-back')
        self._button_back.size = 32
        self._button_back.on_click = self.closeRequested.emit
        top_layout.addWidget(self._button_back)

        right_layout.addWidget(KitLabel(KitLocaleString.white + ':'))
        self._white_combo_box = KitComboBox()
        self._white_combo_box.currentValueChanged.connect(lambda: self._on_state_changed())
        right_layout.addWidget(self._white_combo_box)

        right_layout.addWidget(KitVBoxLayout(), 200)

        right_layout.addWidget(KitLabel(KitLocaleString.black + ':'))
        self._black_combo_box = KitComboBox()
        self._black_combo_box.currentValueChanged.connect(lambda: self._on_state_changed())
        right_layout.addWidget(self._black_combo_box)

        self._board_widget = BoardWidget()
        self._board_widget.figSelected.connect(lambda fig: self._on_figure_selected(fig))
        self._board_widget.moveSelected.connect(lambda pos, prom: self._on_move_selected(pos, prom))
        self.addWidget(self._board_widget)

        self._api.boards.boardUpdated.connect(lambda: self._load_ui())
        self._api.boards.newMove.connect(lambda move: self._on_new_move(move))

    def open(self):
        self._load_state()
        self._load_ui()

    def _load_state(self):
        self._board_widget.clear()
        print(self._api.boards.board.state)
        for item in self._api.boards.board.state.values():
            self._board_widget.add_figure(item)

    @asyncSlot()
    async def _on_figure_selected(self, figure: Figure):
        if self._api.boards.move_required:
            moves = await self._api.boards.available_moves(figure.pos)
            self._board_widget.show_available_moves(figure.pos, moves)
            self._fig = figure

    @asyncSlot()
    async def _on_move_selected(self, pos, promotion):
        await self._api.boards.move(self._fig.pos, pos, promotion)

    @asyncSlot()
    async def _on_new_move(self, move: Move):
        if move:
            self._board_widget.move_figure(move.src, move.dst)
            await asyncio.sleep(config.MOVE_DURATION / 1000)
        self._load_state()

    @asyncSlot()
    async def _load_ui(self):
        self._loading = True
        await self._update_combo_box(self._white_combo_box, self._api.boards.board.white)
        await self._update_combo_box(self._black_combo_box, self._api.boards.board.black)
        self._loading = False

    async def _update_combo_box(self, combo_box: KitComboBox, uid):
        combo_box.clear()
        user = await self._api.users.get(self._api.boards.board.owner)
        combo_box.addItem(KitComboBoxItem(user.name, user.id))
        for el in self._api.boards.board.invited:
            user = await self._api.users.get(el)
            combo_box.addItem(KitComboBoxItem(user.name, user.id))
        combo_box.setCurrentValue(uid)

    @asyncSlot()
    async def _on_state_changed(self):
        if self._loading:
            return

        board = self._api.boards.board
        board.white = self._white_combo_box.currentValue()
        board.black = self._black_combo_box.currentValue()
        await self._api.boards.upload_board(board)

