from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
import numpy as np
import sys
import pyqtgraph as pg
from Ui_test import *
import qdarkstyle

class Monitor:
    def __init__(self):
        self.is_playing = False

    def plot(self):
        pass

class TestWin(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
    def plot(self):
        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        self.graphicsView.plot(x, y, pen=None, symbol='o')

if __name__ == '__main__':
    # pyqt对高分辨率屏幕调整
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    ## Always start by initializing Qt (only once per application)
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    view = TestWin()
    # view.setupUi(QWidget)
    view.show()
    view.plot()
    ## Start the Qt event loop
    sys.exit(app.exec_())