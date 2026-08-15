from PyQt5.QtCore import QObject, pyqtSlot

from chatbot import EduLensChatbot


class EduLensBridge(QObject):

    def __init__(self):
        super().__init__()
        self.chatbot = EduLensChatbot()

    @pyqtSlot(str, result="QVariant")
    def analyze(self, post):
        return self.chatbot.analyze(post)