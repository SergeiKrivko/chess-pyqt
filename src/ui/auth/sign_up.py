from PyQt6.QtCore import Qt, pyqtSignal
from PyQtUIkit.core import KitFont
from PyQtUIkit.themes.locale import KitLocaleString
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src.core.service import ApiService


class SignUpScreen(KitVBoxLayout):
    backRequested = pyqtSignal()

    def __init__(self, api: ApiService):
        super().__init__()
        self._api = api
        self.alignment = Qt.AlignmentFlag.AlignCenter

        h_layout = KitHBoxLayout()
        h_layout.alignment = Qt.AlignmentFlag.AlignCenter
        self.addWidget(h_layout)

        main_layout = KitVBoxLayout()
        main_layout.spacing = 6
        main_layout.setFixedWidth(250)
        h_layout.addWidget(main_layout)

        main_layout.addWidget(KitLabel(KitLocaleString.login + ':'))

        self._login_edit = KitLineEdit()
        self._login_edit.font_size = KitFont.Size.BIG
        main_layout.addWidget(self._login_edit)

        main_layout.addWidget(KitLabel(KitLocaleString.password + ':'))

        self._password_edit = KitLineEdit()
        self._password_edit.font_size = KitFont.Size.BIG
        self._password_edit.setEchoMode(KitLineEdit.EchoMode.Password)
        main_layout.addWidget(self._password_edit)

        main_layout.addWidget(KitLabel(KitLocaleString.password_again + ':'))

        self._password2_edit = KitLineEdit()
        self._password2_edit.font_size = KitFont.Size.BIG
        self._password2_edit.setEchoMode(KitLineEdit.EchoMode.Password)
        main_layout.addWidget(self._password2_edit)

        self._error_label = KitLabel(KitLocaleString.error)
        self._error_label.main_palette = 'Danger'
        main_layout.addWidget(self._error_label)

        button_layout = KitHBoxLayout()
        button_layout.spacing = 5
        main_layout.addWidget(button_layout)

        self._button_back = KitIconButton('line-arrow-back')
        self._button_back.size = 40
        self._button_back.radius = 8
        self._button_back.on_click = self.backRequested.emit
        button_layout.addWidget(self._button_back)

        self._button_signup = KitButton(KitLocaleString.sign_up)
        self._button_signup.font_size = KitFont.Size.BIG
        self._button_signup.setFixedHeight(40)
        self._button_signup.radius = 8
        self._button_signup.on_click = lambda: self._sign_up()
        button_layout.addWidget(self._button_signup)

    @asyncSlot()
    async def _sign_up(self):
        await self._api.auth.create_user(self._login_edit.text, self._password_edit.text)
        await self._api.auth.auth(self._login_edit.text, self._password_edit.text)
