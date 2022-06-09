import sys
import webbrowser
import subprocess
import json
import requests
import platform
import os
from urllib.request import urlopen

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *


class Downloader(QThread):

    # Signal for the window to establish the maximum value
    # of the progress bar.
    setTotalProgress = pyqtSignal(int)
    # Signal to increase the progress.
    setCurrentProgress = pyqtSignal(int)
    # Signal to be emitted when the file has been downloaded successfully.
    succeeded = pyqtSignal()

    def __init__(self, url, filename):
        super().__init__()
        self._url = url
        self._filename = filename

    def run(self):

        try:
            os.makedirs(self._filename)
        except:
            pass
        self._filename = os.path.join(self._filename, "main.AppImage")
        readBytes = 0
        chunkSize = 1024
        # Open the URL address.
        with urlopen(self._url) as r:
            # Tell the window the amount of bytes to be downloaded.
            try:
                self.setTotalProgress.emit(int(r.info()["Content-Length"]))
            except:
                self.setTotalProgress.emit(0)
            with open(self._filename, "ab") as f:
                while True:
                    # Read a piece of the file we are downloading.
                    chunk = r.read(chunkSize)
                    # If the result is `None`, that means data is not
                    # downloaded yet. Just keep waiting.
                    if chunk is None:
                        continue
                    # If the result is an empty `bytes` instance, then
                    # the file is complete.
                    elif chunk == b"":
                        break
                    # Write into the local file the downloaded chunk.
                    f.write(chunk)
                    readBytes += chunkSize
                    # Tell the window how many bytes we have received.
                    self.setCurrentProgress.emit(readBytes)
        # If this line is reached then no exception has ocurred in
        # the previous lines.
        self.succeeded.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mineshaft Launcher")

        self.versions = self.get_versions()

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)

        tabs.addTab(self.main_tab(), "News")

        self.setCentralWidget(tabs)

    def downloadSucceeded(self):
        self.progress_bar.setFormat("download complete")

    def downloadFinished(self):
        self.progress_bar.setFormat("download finished")
        self.play_button.setEnabled(True)

    def main_tab(self):
        widget = QWidget()
        layout = QGridLayout()

        webview = QWebEngineView()
        webview.load(QUrl("https://mineshaft-game.github.io/changelog"))

        menu_spacer = QSpacerItem(100, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)

        website_button = QPushButton("Mineshaft")
        website_button.clicked.connect(
            lambda: webbrowser.open("mineshaft-game.github.io")
        )

        bug_button = QPushButton("Bug tracker")
        bug_button.clicked.connect(
            lambda: webbrowser.open("github.com/mineshaft-game/mineshaft/issues")
        )

        self.play_button = QPushButton("PLAY")
        self.play_button.clicked.connect(self.run_mineshaft)

        profile_widget = QWidget()
        profile_layout = QHBoxLayout()
        profile_label = QLabel("Profile:")
        profile_box = QComboBox()

        profile_layout.addWidget(profile_label)
        profile_layout.addWidget(profile_box)
        profile_widget.setLayout(profile_layout)

        self.version_box = QComboBox()
        for version in self.get_versions():
            self.version_box.addItem(version)

        self.progress_bar = QProgressBar()

        layout.addWidget(webview, 0, 0, 5, 6)
        # layout.addItem(menu_spacer,  4, 0)

        # layout.addWidget(website_button,  0, 4)
        # layout.addWidget(bug_button,  1, 4)

        layout.addWidget(profile_widget, 5, 0)
        # layout.addWidget(profile_label, 5,0)
        layout.addWidget(self.version_box, 5, 3)

        layout.addWidget(self.play_button, 5, 2)
        layout.addWidget(self.progress_bar, 5, 4)

        widget.setLayout(layout)

        return widget

    def run_mineshaft(self):
        try:
            subprocess.run(
                f".mineshaft/versions/{self.version_box.currentText()}/main.AppImage"
            )
        except Exception:
            self.download_version(self.version_box.currentText())

    def get_versions(self):
        try:
            return json.loads(
                requests.get("https://mineshaft-game.github.io/launcher.json").text
            )
        except:
            return json.loads(
                requests.get(
                    "https://raw.githubusercontent.com/Mineshaft-game/mineshaft-game.github.io/main/launcher.json"
                ).text
            )

    def download_version(self, version):
        if platform.system() == "Linux":
            system = "linux"
        elif platform.system() == "Darwin":
            system = "macos"
        elif platform.system() == "Windows":
            system = "windows"

        # Run the download in a new thread.
        self.progress_bar.setFormat("Starting Download.")
        self.play_button.setEnabled(False)
        try:
            self.downloader = Downloader(
                self.versions[version][system][platform.machine()],
                os.path.join(".mineshaft", "versions", f"{version}"),
            )
        except:
            msg_box = QMessageBox()
            msg_box.setText("This version isn't compaptible with your computer.")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.exec_()
            self.play_button.setEnabled(True)
            return
        # Connect the signals which send information about the download
        # progress with the proper methods of the progress bar.
        self.downloader.setTotalProgress.connect(self.progress_bar.setMaximum)
        self.downloader.setCurrentProgress.connect(self.progress_bar.setValue)
        # Qt will invoke the `succeeded()` method when the file has been
        # downloaded successfully and `downloadFinished()` when the
        # child thread finishes.
        self.downloader.succeeded.connect(self.downloadSucceeded)
        self.downloader.finished.connect(self.downloadFinished)
        try:
            self.downloader.start()
            self.progress_bar.resetFormat()
        except:
            self.progress_bar.setFormat("Download Failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
