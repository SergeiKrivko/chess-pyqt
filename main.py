from sys import argv

from PyQtUIkit.widgets import KitAsyncApplication, KitApplication

from src import config
from src.ui.main_window import MainWindow


def main():
    if '--test' in argv:
        config.APP_NAME += '-test'
    if '--local' in argv:
        config.API_URL = "http://localhost:8000"

    KitApplication.setApplicationName(config.APP_NAME)
    KitApplication.setOrganizationName(config.APP_NAME)
    KitApplication.setApplicationVersion(config.APP_VERSION)
    KitAsyncApplication(MainWindow).exec()


if __name__ == '__main__':
    main()
