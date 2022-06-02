import sys
import webbrowser

from PyQt5.QtCore import *
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
        
        tabs.addTab(self.main_tab(),  "News")

        self.setCentralWidget(tabs)
        
    def main_tab(self):
        widget = QWidget()
        layout = QGridLayout()
        
        webview = QWebEngineView()
        webview.load(QUrl("https://mineshaft-game.github.io"))
        
        
        menu_spacer = QSpacerItem(100, 10,  QSizePolicy.Expanding,  QSizePolicy.Minimum)
        
        website_button = QPushButton("Mineshaft")
        website_button.clicked.connect(lambda: webbrowser.open("mineshaft-game.github.io"))
        
        bug_button = QPushButton("Bug tracker")
        bug_button.clicked.connect(lambda: webbrowser.open("github.com/mineshaft-game/mineshaft/issues"))
        
        play_button = QPushButton("PLAY")
        
        version_box = QComboBox()
        version_box2 = QComboBox()

        
        layout.addWidget(webview,  0, 0,  5,  6)
        layout.addItem(menu_spacer,  4, 0)
        
        #layout.addWidget(website_button,  0, 4)
        #layout.addWidget(bug_button,  1, 4)
        
        layout.addWidget(version_box,  5, 0,  1,  1)
        layout.addWidget(version_box2,  5, 3)
        
        layout.addWidget(play_button,  5,1)
        
        
        widget.setLayout(layout)
        
        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
