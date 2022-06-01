import sys

from PyQt5.QtCore import QSize, Qt,  QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mineshaft Launcher")
        
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)
        
        tabs.addTab(self.main_tab(),  "Launcher")

        self.setCentralWidget(tabs)
        
    def main_tab(self):
        widget = QWidget()
        layout = QGridLayout()
        
        button = QWebEngineView()
        button.load(QUrl("https://mineshaft-game.github.io"))
        menu_spacer = QSpacerItem(100, 110,  QSizePolicy.Expanding, QSizePolicy.Minimum)

        #layout.addItem(menu_spacer,  0, 0)
        layout.addWidget(button,  0, 1)
        widget.setLayout(layout)
        
        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
