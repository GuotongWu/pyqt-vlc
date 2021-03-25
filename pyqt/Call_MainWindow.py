import sys
import platform
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from random import randint
from Monitor import Monitor
from getStatus import *

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
        self.actionMaximize.triggered.connect(self.showMaximized)
        self.actionMinimize.triggered.connect(self.showMinimized)
        self.actionDefault.triggered.connect(self.showNormal)

        self.playButton.clicked.connect(self.play_pause)
        self.positionslider.sliderMoved.connect(self.set_position)
        self.positionslider.sliderPressed.connect(self.set_position)
        self.volumeslider.valueChanged.connect(self.set_volume)
        self.soundButton.clicked.connect(self.set_mute)
        self.getStatusButton.clicked.connect(self.setStatus)
        # vlc
        self.instance = vlc.Instance()
        self.media = None
        self.mediaplayer = self.instance.media_player_new()
        self.is_paused = False
        self.is_urlplay = False
        self.original_valume = 0
        # self.mediaplayer.set_fullscreen(True)
        # self.fullscreenButton.clicked.connect(self.set_fscreen)
        # timer
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)  # 设置更新时间为100ms
        self.timer.timeout.connect(self.update_ui)
        self.cnt = 0
        # 鼠标
        self.m_flag = False
        # 声音
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())   
        # 监控
        self.monitor = Monitor()
        # 绘图
        # self.widget.toolbar.setVisible(False)
        # self.widget_2.toolbar.setVisible(False)

    def getfps(self):
        return self.mediaplayer.get_fps()

    def set_fscreen(self):
        # self.mediaplayer.set_hwnd(0)
        self.mediaplayer.toggle_fullscreen()
        # print(self.mediaplayer.get_fullscreen())

    def set_mute(self):
        volume = self.mediaplayer.audio_get_volume()
        icon = QtGui.QIcon()
        if volume == 0: # 如果当前是静音
            self.mediaplayer.audio_set_volume(self.original_valume)
            icon.addPixmap(QtGui.QPixmap("src\sound.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.volumeslider.setValue(self.original_valume)
        else: # 如果当前有声音
            self.original_valume = self.mediaplayer.audio_get_volume()
            self.mediaplayer.audio_set_volume(0)
            self.volumeslider.setValue(0)
            icon.addPixmap(QtGui.QPixmap("src\mute.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.soundButton.setIcon(icon)

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
        icon = QtGui.QIcon()
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            icon.addPixmap(QtGui.QPixmap("src\play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.is_paused = True
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file()
                return
            self.mediaplayer.play()
            icon.addPixmap(QtGui.QPixmap("src\pause.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.timer.start()
            self.is_paused = False
        
        self.playButton.setIcon(icon)

    def update_ui(self):
        """Updates the user interface"""

        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        
        if self.is_urlplay == False: # 播放本地视频
            media_pos = int(self.mediaplayer.get_position() * 99)
            self.positionslider.setValue(media_pos)

            # No need to call this function if nothing is played
            if not self.mediaplayer.is_playing():
                self.timer.stop()

                # After the video finished, the play button stills shows "Pause",
                # which is not the desired behavior of a media player.
                # This fixes that "bug".
                if not self.is_paused:
                    self.stop()
        else:
            self.widget.mpl.start_dynamic_plot()
            data = self.monitor.getData()
            if data:
                [time, video, audio, bit, rtmp] = data
                time = time.strftime('%Y-%m-%dT%H:%M:%SZ')
                self.label_time.setText('时间：' + time)
                self.label_rtmp.setText('rtmp域名：' + str(rtmp))
                self.label_audio.setText('视频帧率：' + str(video))
                # self.label_video.setText('音频帧率：' + str(video))
                self.label_bit.setText('比特率：' + str(bit))
                    

        self.timelabel.setText(self.calculate_time())

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

        self.set_platform()

        self.play_pause()

    def set_platform(self):
        if platform.system() == "Linux": # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows": # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

    def play_url(self, url):
        self.set_platform()

        self.mediaplayer.set_mrl(url)
        self.is_urlplay = True
        self.mediaplayer.play()
        self.timer.start()
        self.is_paused = False

        # print(self.widget.__dict__)
        # self.widget.begin = True

    def set_position(self):
        if self.is_urlplay == False:
            self.timer.stop()
            pos = self.positionslider.value()
            self.mediaplayer.set_position(pos / 99.0)
            self.timer.start()

    def stop(self):
        self.mediaplayer.stop()

    def set_volume(self, volume):
        self.mediaplayer.audio_set_volume(volume)

    def calculate_time(self):
        timestring = '00:00/00:00'
        if self.mediaplayer.get_length() == -1:
            return timestring
        curr_msec = int(self.mediaplayer.get_time())
        curr_minute = 0
        curr_second = 0
        if curr_msec != 0:    
            curr_minute = curr_msec // (60 * 1000)
            curr_second = (curr_msec - (curr_minute * 60000)) // 1000
        if self.is_urlplay == False:
            vi_msec = self.mediaplayer.get_length()
            if vi_msec != 0:
                vi_minute = vi_msec // (60 * 1000)
                vi_second = (vi_msec - (vi_minute * 60000)) // 1000
                timestring = str_time(curr_minute) + ':' + str_time(curr_second) + '/' + str_time(vi_minute) + ':' + str_time(vi_second)
        else:
            timestring = str_time(curr_minute) + ':' + str_time(curr_second) + '/00:00'
        return timestring 

    def setStatus(self):
        time.sleep(3)
        self.label_status.setText('状态: ' + getStatus())

def str_time(time):
    if time < 10:
        return '0' + str(time)
    else:
        return(str(time))

if __name__ == '__main__':
    # pyqt对高分辨率屏幕调整
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    view = MainWin()
    
    # setup stylesheet
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    view.show()
    sys.exit(app.exec_())