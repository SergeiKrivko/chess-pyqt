from PyQt6.QtCore import Qt, pyqtSignal
from PyQtUIkit.core import KitFont
from PyQtUIkit.themes.locale import KitLocaleString
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src.core.service import ApiService


class SignInScreen(KitVBoxLayout):
    signupRequested = pyqtSignal()

    def __init__(self, api: ApiService):
        super().__init__()
        self.alignment = Qt.AlignmentFlag.AlignCenter
        self._api = api

        h_layout = KitHBoxLayout()
        h_layout.alignment = Qt.AlignmentFlag.AlignCenter
        self.addWidget(h_layout)

        main_layout = KitVBoxLayout()
        main_layout.setFixedWidth(250)
        main_layout.spacing = 6
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

        self._error_label = KitLabel(KitLocaleString.error)
        self._error_label.main_palette = 'Danger'
        main_layout.addWidget(self._error_label)

        self._button_signin = KitButton(KitLocaleString.sign_in)
        self._button_signin.font_size = KitFont.Size.BIG
        self._button_signin.radius = 8
        self._button_signin.on_click = lambda: self._sign_in()
        self._button_signin.setFixedHeight(40)
        main_layout.addWidget(self._button_signin)

        self._button_signup = KitButton(KitLocaleString.sign_up)
        self._button_signup.main_palette = 'Bg'
        self._button_signup.border = 0
        self._button_signup.on_click = self.signupRequested.emit
        main_layout.addWidget(self._button_signup)

    @asyncSlot()
    async def _sign_in(self):
        await self._api.auth.auth(self._login_edit.text, self._password_edit.text)
