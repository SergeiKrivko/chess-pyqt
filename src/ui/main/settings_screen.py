from PyQt6.QtCore import Qt
from PyQtUIkit.core import KitFont
from PyQtUIkit.themes.locale import KitLocaleString
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src.core.service import ApiService
from src.core.settings_manager import SettingsManager


class SettingsScreen(KitVBoxLayout):
    def __init__(self, sm: SettingsManager, api: ApiService):
        super().__init__()
        self._sm = sm
        self._api = api
        self.padding = 30
        self.spacing = 12
        self.alignment = Qt.AlignmentFlag.AlignTop

        layout = KitHBoxLayout()
        layout.spacing = 6
        self.addWidget(layout)

        icon = KitIconWidget('solid-person-circle')
        icon.setFixedSize(40, 40)
        layout.addWidget(icon)

        self._user_label = KitLabel()
        self._user_label.font_size = KitFont.Size.BIG
        layout.addWidget(self._user_label)

        layout = KitHBoxLayout()
        layout.spacing = 6
        layout.alignment = Qt.AlignmentFlag.AlignLeft
        self.addWidget(layout)

        self._button_sign_out = KitButton(KitLocaleString.sign_out)
        self._button_sign_out.on_click = self._api.auth.sign_out
        layout.addWidget(self._button_sign_out)

        self._button_change_password = KitButton(KitLocaleString.change_pass)
        layout.addWidget(self._button_change_password)

        self.addWidget(KitHSeparator())

        layout = KitHBoxLayout()
        layout.spacing = 6
        self.addWidget(layout)
        layout.addWidget(KitLabel(KitLocaleString.theme + ':'))

        self._theme_box = KitComboBox()
        self._theme_box.setFixedWidth(200)
        for el in ['light', 'dark']:
            self._theme_box.addItem(KitComboBoxItem(KitLocaleString.get(el), el))
        self._theme_box.setCurrentValue(self._sm.get('theme'))
        self._theme_box.currentValueChanged.connect(self._on_theme_changed)
        layout.addWidget(self._theme_box)
        layout.addWidget(KitHBoxLayout(), 100)

        layout = KitHBoxLayout()
        layout.spacing = 6
        self.addWidget(layout)
        layout.addWidget(KitLabel(KitLocaleString.language + ':'))

        self._locale_box = KitLanguageBox()
        self._locale_box.setFixedWidth(200)
        self._locale_box.langChanged.connect(self._on_lang_changed)
        layout.addWidget(self._locale_box)
        layout.addWidget(KitHBoxLayout(), 100)

        self.addWidget(KitVBoxLayout(), 100)

    def showEvent(self, a0):
        super().showEvent(a0)
        self._update_user_label()

    @asyncSlot()
    async def _update_user_label(self):
        name = await self._api.users.get(self._sm.uid)
        self._user_label.text = name.name

    def _on_lang_changed(self, lang):
        self._sm.set('language', lang)

    def _on_theme_changed(self, theme):
        self._sm.set('theme', theme)
        self.theme_manager.set_theme(theme)
