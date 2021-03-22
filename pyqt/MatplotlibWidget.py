import sys
import random
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from Monitor import Monitor
import pandas as pd
import numpy as np
import matplotlib.dates as mdates

class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, width=1, height=1, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        self.monitor = Monitor()

        self.fig = Figure(figsize=(width,height),dpi=dpi, tight_layout=True, facecolor=(66/255,75/255,83/255))  # 新建一个figure
        # self.fig.canvas.window().statusBar().setVisible(False) # Remove status bar (bottom bar)
        self.axes_fps = self.fig.add_subplot(211)  # 建立一个子图，如果要建立复合图，可以在这里修改
        self.axes_bps = self.fig.add_subplot(212)

        self.data = [[], [], [], []]
        self.xfmt = mdates.DateFormatter('%H:%M:%S')
        self.begin = False

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    '''绘制静态图，可以在这里定义自己的绘图逻辑'''

    def start_static_plot(self):
        # self.fig.suptitle('测试图')
        t = arange(0.0, 3.0, 0.01)
        s = [1]*len(t)
        self.axes_fps.plot(t, s)
        self.axes_fps.set_ylabel('帧率/码率')
        self.axes_fps.set_xlabel('时间')
        self.axes_fps.grid(True)

    '''启动绘制动态图'''

    def start_dynamic_plot(self, *args, **kwargs):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)  # 每隔一段时间就会触发一次update_figure函数。
        timer.start(100)  # 触发的时间间隔为0.1秒。

    '''动态图的绘图逻辑可以在这里修改'''

    def update_figure(self):
        # if self.begin:
        # 更新图像
        tmp = self.monitor.getData()
        for i in range(0,4):
            self.data[i].append(tmp[i])
        if len(self.data[0]) > 20:   # 限制数据在20个以内
            for i in range(0,4):
                del self.data[i][0] # 超出则删除第一个元素
        # print(self.data[1])

        self.axes_fps.clear()
        self.axes_bps.clear()

        # self.axes_fps.xaxis.set_major_formatter(self.xfmt)
        self.axes_fps.plot(self.data[0], self.data[1], 'g')
        # self.axes_fps.plot(self.data[0], self.data[2], 'y')
        self.axes_fps.set_title('帧率变化图')
        self.axes_fps.set_ylabel('帧率（fps）')
        self.axes_fps.patch.set_facecolor((25/255,35/255,45/255)) # 设置 ax1 区域背景颜色
        self.axes_fps.patch.set_alpha(0.8)
        self.axes_fps.grid(True)


        self.axes_bps.plot(self.data[0], self.data[3], 'g')
        self.axes_bps.set_title('码率变化图')
        self.axes_bps.set_ylabel('码率（bps）')
        self.axes_bps.set_xlabel('时间（time）')
        self.axes_bps.patch.set_facecolor((25/255,35/255,45/255)) # 设置 ax1 区域背景颜色
        self.axes_bps.patch.set_alpha(0.8)
        self.axes_bps.grid(True)
        
        self.draw()


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self)
        # self.mpl.start_static_plot() # 如果你想要初始化的时候就呈现静态图，请把这行注释去掉
        # self.mpl.start_dynamic_plot() # 如果你想要初始化的时候就呈现动态图，请把这行注释去掉
        self.layout.addWidget(self.mpl)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    ui.mpl.start_static_plot()  # 测试静态图效果
    # ui.mpl.start_dynamic_plot() # 测试动态图效果
    ui.show()
    sys.exit(app.exec_()) 
