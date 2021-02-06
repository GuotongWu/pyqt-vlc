import sys
import qdarkstyle

from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

from random import randint

from Call_MainWindow import *
from Call_inputURLwin import *


class PlayMedier:
    """主类"""
    def loadMainWin(self):
        self.viewMain = MainWin()
        self.viewMain.actionStream.triggered.connect(self.openInputURLwin)
        self.viewMain.actionExit.triggered.connect(self.viewMain.close)
        self.viewMain.show()

    def loadinputURLwin(self):
        self.viewInputURLwin = InputURLwin()
        # self.viewInputURLwin.lineEdit.editingFinished.connect(self.get_URL) # 目前调试有错误
        self.viewInputURLwin.buttonBox.accepted.connect(self.get_URL)
        # self.viewInputURLwin.buttonBox.rejected.connect(self.closeInputURLwin)
        self.viewInputURLwin.show()

    def openInputURLwin(self):
        self.loadinputURLwin()

    def get_URL(self):
        self.url = self.viewInputURLwin.lineEdit.text()
        print(self.url)
        self.viewInputURLwin.close()


if __name__ == '__main__':
    # pyqt对高分辨率屏幕调整
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    player = PlayMedier()
    player.loadMainWin()
    
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    sys.exit(app.exec_())