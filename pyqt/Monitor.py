from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from aliyun import Aliyun
from Ui_test import *

import numpy as np
import sys
import pyqtgraph as pg
import qdarkstyle
import datetime
import pandas as pd
import matplotlib.pyplot as plt

class Monitor:
    def __init__(self):
        self.is_playing = False # 判断是否url播放模式
        self.streamUrl = ''
        self.time = datetime.datetime.now() - datetime.timedelta(hours=8)
        # print(self.startTime)
        self.df = pd.DataFrame(columns=['Time','VideoFrameRate', 'AudioFrameRate', 'BitRate'])

    def succGetData(self):
        aliyun = Aliyun()
        self.streamUrl = aliyun.describeLiveDomainFrameRateAndBitRateData()['StreamUrl']
        start_time = datetime.datetime.strptime('2021-02-28T07:45:00Z','%Y-%m-%dT%H:%M:%SZ')
        for i in range(0,100):
            start_time = start_time + datetime.timedelta(seconds=20)
            str_start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            data = list(aliyun.describeLiveDomainFrameRateAndBitRateData(str_start_time).values())
            if data:
                data.insert(0, start_time)
                self.df.loc[i] = data[:4]
                i = i + 1

    def update(self):
        pass

    def plot(self):
        plt.figure()
        plt.plot(self.df.iloc[:,0], self.df.iloc[:,1:3])
        plt.show()

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
    m = Monitor()
    m.succGetData()
    m.plot()
    # view.setupUi(QWidget)
    view.show()
    view.plot()
    ## Start the Qt event loop
    sys.exit(app.exec_())