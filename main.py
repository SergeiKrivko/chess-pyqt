from PyQtUIkit.widgets import KitAsyncApplication, KitApplication

from src import config
from src.ui.main_window import MainWindow


def main():
    KitApplication.setApplicationName(config.APP_NAME)
    KitApplication.setOrganizationName(config.APP_NAME)
    KitApplication.setApplicationVersion(config.APP_VERSION)
    KitAsyncApplication(MainWindow).exec()


if __name__ == '__main__':
    main()
