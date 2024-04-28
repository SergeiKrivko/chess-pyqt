from PyQtUIkit.widgets import KitTabLayout

from src.core.service import ApiService
from src.ui.auth.sign_in import SignInScreen
from src.ui.auth.sign_up import SignUpScreen


class AuthScreen(KitTabLayout):
    def __init__(self, api: ApiService):
        super().__init__()

        self._api = api

        self._sign_in = SignInScreen(self._api)
        self._sign_in.signupRequested.connect(lambda: self.setCurrent(1))
        self.addWidget(self._sign_in)

        self._sign_up = SignUpScreen(self._api)
        self._sign_up.backRequested.connect(lambda: self.setCurrent(0))
        self.addWidget(self._sign_up)
