import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from random import randint
import time

from Ui_MainWindow import *
from Ui_InputURL import *

class MainWin(QMainWindow, Ui_MediaPlayer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class InputURLwin(QWidget, Ui_InputURL):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class PlayMedier:
    def loadMainWin(self):
        self.viewMain = MainWin()
        self.viewMain.actionStream.triggered.connect(self.openInputURLwin)
        self.viewMain.show()

    def loadinputURLwin(self):
        self.viewInputURLwin = InputURLwin()
        self.viewInputURLwin.show()

    def openInputURLwin(self):
        self.loadinputURLwin()

if __name__ == '__main__':
    # pyqt对高分辨率屏幕调整
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    player = PlayMedier()
    player.loadMainWin()
    
    sys.exit(app.exec_())