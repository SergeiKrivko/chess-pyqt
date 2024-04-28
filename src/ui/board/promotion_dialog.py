from PyQt6.QtCore import Qt
from PyQtUIkit.themes.locale import KitLocaleString
from PyQtUIkit.widgets import *


class PromotionDialog(KitDialog):
    def __init__(self, parent, promotions: list[str]):
        super().__init__(parent)
        self.button_close = False
        self.promotion = None

        main_layout = KitHBoxLayout()
        main_layout.padding = 10
        main_layout.spacing = 6
        self.setWidget(main_layout)

        self._items = []
        for promotion in promotions:
            item = PromotionItem(promotion)
            self._items.append(item)
            main_layout.addWidget(item)
            item.on_click = lambda x, p=promotion: self._on_select(p)

    def _on_select(self, promotion):
        self.promotion = promotion
        self.accept()


class PromotionItem(KitLayoutButton):
    def __init__(self, promotion: str):
        super().__init__(Qt.Orientation.Vertical)

        self.padding = 6
        self.setFixedSize(76, 100)

        self._icon_widget = KitIconWidget(f'custom-{promotion}')
        self._icon_widget.setFixedSize(64, 64)
        self.addWidget(self._icon_widget)

        self._label = KitLabel(KitLocaleString.get(promotion))
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self._label)

