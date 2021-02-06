import sys
import qdarkstyle

from Ui_InputURL import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class InputURLwin(QWidget, Ui_InputURL):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 设置背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置无边框样式
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置cancel键响应
        self.buttonBox.rejected.connect(self.closeInputURLwin)
        # 设置背景颜色
        # self.setStyleSheet('QWidget{background-color:white}')


    def closeInputURLwin(self):
        self.close()

if __name__ == '__main__':
    # pyqt对高分辨率屏幕调整
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    view = InputURLwin()
    
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    view.show()
    sys.exit(app.exec_())