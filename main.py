import os
import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel

from backend import analyze_claim


class TruthLensBridge(QObject):
    @pyqtSlot(str, result="QVariant")
    def analyze(self, post):
        return analyze_claim(post)

app = QApplication(sys.argv)

browser = QWebEngineView()

channel = QWebChannel(browser.page())
channel.registerObject("truthlens", TruthLensBridge())
browser.page().setWebChannel(channel)

browser.setWindowTitle("TruthLens AI")

browser.resize(430, 900)

browser.setMinimumSize(390, 844)

path = Path(__file__).resolve().parent / "ui" / "CB1.html"

browser.load(QUrl.fromLocalFile(str(path)))

browser.show()

sys.exit(app.exec_())
