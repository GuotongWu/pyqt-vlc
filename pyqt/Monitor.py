from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from aliyun import Aliyun
from Ui_test import *
from pyqtgraph.Qt import QtGui, QtCore

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
        self.df = pd.DataFrame(columns=['Time','VideoFrameRate', 'AudioFrameRate', 'BitRate'])
        self.aliyun = Aliyun()

    def succGetData(self):
        self.streamUrl = self.aliyun.describeLiveDomainFrameRateAndBitRateData()['StreamUrl']
        start_time = datetime.datetime.strptime('2021-02-28T07:45:00Z', '%Y-%m-%dT%H:%M:%SZ')
        for i in range(0,100):
            start_time = start_time + datetime.timedelta(seconds=20)
            str_start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            data = list(self.aliyun.describeLiveDomainFrameRateAndBitRateData(str_start_time).values())
            if data:
                data.insert(0, start_time)
                self.df.loc[i] = data[:4]
                i = i + 1

    def update(self):
        pass

    def getData(self):
        time = datetime.datetime.now() - datetime.timedelta(seconds=120) # 延时120s
        applyTime = time - datetime.timedelta(hours=8,seconds=10) # datetime类型
        str_time = applyTime.strftime('%Y-%m-%dT%H:%M:%SZ')
        tmp = list(self.aliyun.describeLiveDomainFrameRateAndBitRateData(str_time).values())
        if not tmp:
            tmp = [0, 0, 0, '--']
        tmp.insert(0, time)
        return tmp

    def plot(self):
        self.df['Time'] = self.df['Time'].astype('datetime64[ns]')
        plt.figure()
        plt.plot(self.df.iloc[:,0], self.df.iloc[:,1:3])
        plt.show()


class TestWin(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.monitor = Monitor()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
    def plot(self):
        # x = np.random.normal(size=1000)
        # y = np.random.normal(size=1000)
        x, y = self.monitor.df.iloc[:,0], self.monitor.df.iloc[:,1]
        z = self.monitor.df.iloc[:,2]
        self.curve1 = self.graphicsView.plot(x, y)
        self.curve2 = self.graphicsView.plot(x, z)

    def update(self):
        self.monitor.getData()
        x, y = self.monitor.df.iloc[:,0], self.monitor.df.iloc[:,1]
        z = self.monitor.df.iloc[:,2]
        self.curve1.setData(x, y)
        self.curve2.setData(x, z)

if __name__ == '__main__':
    # pyqt对高分辨率屏幕调整
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    ## Always start by initializing Qt (only once per application)
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # view = TestWin()
    # view.setupUi(QWidget)
    monitor = Monitor()
    monitor.succGetData()
    monitor.plot()
    print(type(monitor.df.iloc[0,0]))
    # view.show()
    # view.plot()
    ## Start the Qt event loop
    sys.exit(app.exec_())