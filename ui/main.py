import os
import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl
from bridge import EduLensBridge


app = QApplication(sys.argv) 

browser = QWebEngineView()

browser.setWindowTitle("EduLens AI")
browser.resize(430, 900)
browser.setMinimumSize(390, 844)

# Create WebChannel
channel = QWebChannel()

bridge = EduLensBridge()

channel.registerObject("edulens", bridge)

browser.page().setWebChannel(channel)

# Load first screen
path = Path(__file__).resolve().parent / "CB1.html"

browser.load(QUrl.fromLocalFile(str(path)))

browser.show()

sys.exit(app.exec_())
