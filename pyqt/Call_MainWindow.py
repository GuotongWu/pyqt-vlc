import sys
import platform
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from random import randint

import os
import time
import qdarkstyle

os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlc-3.0.11"
import vlc

from Ui_MainWindow import *


class MainWin(QMainWindow, Ui_MediaPlayer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 设置背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置无边框样式
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置背景颜色
        # self.setStyleSheet('QWidget{background-color:blue}')
        # 信号槽
        self.playButton.clicked.connect(self.play_pause)
        self.pauseButton.clicked.connect(self.play_pause)
        # vlc
        self.instance = vlc.Instance()
        self.media = None
        self.mediaplayer = self.instance.media_player_new()
        self.is_paused = False
        # timer
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)


    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
        
    def play_pause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            # self.playbutton.setText("Play")
            self.is_paused = True
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file()
                return

            self.mediaplayer.play()
            # self.playbutton.setText("Pause")
            self.timer.start()
            self.is_paused = False

    def update_ui(self):
        """Updates the user interface"""

        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        
        # media_pos = int(self.mediaplayer.get_position() * 1000)
        # self.positionslider.setValue(media_pos)

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows "Pause",
            # which is not the desired behavior of a media player.
            # This fixes that "bug".
            if not self.is_paused:
                self.stop()

    def open_file(self):
        """Open a media file in a MediaPlayer
        """

        dialog_txt = "Choose Media File"
        filename = QtWidgets.QFileDialog.getOpenFileName(self, dialog_txt, os.path.expanduser('~'))
        if not filename:
            return

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(filename[0])

        # Put the media in the media player
        self.mediaplayer.set_media(self.media)

        # Parse the metadata of the file
        self.media.parse()

        # Set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux": # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows": # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        self.play_pause()

    def stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        # self.playbutton.setText("Play")

if __name__ == '__main__':
    # pyqt对高分辨率屏幕调整
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    view = MainWin()
    
    # setup stylesheet
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    view.show()
    sys.exit(app.exec_())