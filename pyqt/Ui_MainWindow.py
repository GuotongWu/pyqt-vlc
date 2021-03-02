# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Github\pyqt-vlc\pyqt\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MediaPlayer(object):
    def setupUi(self, MediaPlayer):
        MediaPlayer.setObjectName("MediaPlayer")
        MediaPlayer.resize(809, 516)
        self.centralwidget = QtWidgets.QWidget(MediaPlayer)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.videoframe = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoframe.sizePolicy().hasHeightForWidth())
        self.videoframe.setSizePolicy(sizePolicy)
        self.videoframe.setMinimumSize(QtCore.QSize(521, 401))
        self.videoframe.setMaximumSize(QtCore.QSize(16777215, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.videoframe.setPalette(palette)
        self.videoframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.videoframe.setObjectName("videoframe")
        self.verticalLayout.addWidget(self.videoframe)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.positionslider = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.positionslider.sizePolicy().hasHeightForWidth())
        self.positionslider.setSizePolicy(sizePolicy)
        self.positionslider.setMinimumSize(QtCore.QSize(451, 0))
        self.positionslider.setOrientation(QtCore.Qt.Horizontal)
        self.positionslider.setObjectName("positionslider")
        self.horizontalLayout_2.addWidget(self.positionslider)
        self.timelabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timelabel.sizePolicy().hasHeightForWidth())
        self.timelabel.setSizePolicy(sizePolicy)
        self.timelabel.setObjectName("timelabel")
        self.horizontalLayout_2.addWidget(self.timelabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playButton.sizePolicy().hasHeightForWidth())
        self.playButton.setSizePolicy(sizePolicy)
        self.playButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\Github\\pyqt-vlc\\pyqt\\../src/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.playButton.setIcon(icon)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout.addWidget(self.playButton)
        spacerItem = QtWidgets.QSpacerItem(250, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.fullscreenButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fullscreenButton.sizePolicy().hasHeightForWidth())
        self.fullscreenButton.setSizePolicy(sizePolicy)
        self.fullscreenButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("d:\\Github\\pyqt-vlc\\pyqt\\../src/fullscreen.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.fullscreenButton.setIcon(icon1)
        self.fullscreenButton.setObjectName("fullscreenButton")
        self.horizontalLayout.addWidget(self.fullscreenButton)
        spacerItem1 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.soundButton = QtWidgets.QPushButton(self.centralwidget)
        self.soundButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.soundButton.sizePolicy().hasHeightForWidth())
        self.soundButton.setSizePolicy(sizePolicy)
        self.soundButton.setMinimumSize(QtCore.QSize(28, 25))
        self.soundButton.setMaximumSize(QtCore.QSize(28, 25))
        self.soundButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("d:\\Github\\pyqt-vlc\\pyqt\\../src/sound.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.soundButton.setIcon(icon2)
        self.soundButton.setObjectName("soundButton")
        self.horizontalLayout.addWidget(self.soundButton)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.volumeslider = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volumeslider.sizePolicy().hasHeightForWidth())
        self.volumeslider.setSizePolicy(sizePolicy)
        self.volumeslider.setMaximumSize(QtCore.QSize(100, 16777215))
        self.volumeslider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeslider.setObjectName("volumeslider")
        self.horizontalLayout.addWidget(self.volumeslider)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.toolframe = QtWidgets.QFrame(self.centralwidget)
        self.toolframe.setMinimumSize(QtCore.QSize(250, 0))
        self.toolframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toolframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolframe.setObjectName("toolframe")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.toolframe)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.toolframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(300000, 600000))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.label_time = QtWidgets.QLabel(self.frame)
        self.label_time.setObjectName("label_time")
        self.verticalLayout_4.addWidget(self.label_time)
        self.label_rtmp = QtWidgets.QLabel(self.frame)
        self.label_rtmp.setObjectName("label_rtmp")
        self.verticalLayout_4.addWidget(self.label_rtmp)
        self.label_audio = QtWidgets.QLabel(self.frame)
        self.label_audio.setObjectName("label_audio")
        self.verticalLayout_4.addWidget(self.label_audio)
        self.label_video = QtWidgets.QLabel(self.frame)
        self.label_video.setObjectName("label_video")
        self.verticalLayout_4.addWidget(self.label_video)
        self.label_bit = QtWidgets.QLabel(self.frame)
        self.label_bit.setObjectName("label_bit")
        self.verticalLayout_4.addWidget(self.label_bit)
        self.widget = MatplotlibWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_4.addWidget(self.widget)
        self.widget_2 = MatplotlibWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_4.addWidget(self.widget_2)
        self.verticalLayout_3.addWidget(self.frame)
        self.horizontalLayout_3.addWidget(self.toolframe)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        MediaPlayer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MediaPlayer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 809, 22))
        self.menubar.setObjectName("menubar")
        self.menuNetWork_Stream = QtWidgets.QMenu(self.menubar)
        self.menuNetWork_Stream.setObjectName("menuNetWork_Stream")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuExit = QtWidgets.QMenu(self.menubar)
        self.menuExit.setObjectName("menuExit")
        MediaPlayer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MediaPlayer)
        self.statusbar.setObjectName("statusbar")
        MediaPlayer.setStatusBar(self.statusbar)
        self.actionLocal_Video = QtWidgets.QAction(MediaPlayer)
        self.actionLocal_Video.setObjectName("actionLocal_Video")
        self.actionStream_URL = QtWidgets.QAction(MediaPlayer)
        self.actionStream_URL.setObjectName("actionStream_URL")
        self.actionMaximize = QtWidgets.QAction(MediaPlayer)
        self.actionMaximize.setObjectName("actionMaximize")
        self.actionMinimize = QtWidgets.QAction(MediaPlayer)
        self.actionMinimize.setObjectName("actionMinimize")
        self.actionDefault = QtWidgets.QAction(MediaPlayer)
        self.actionDefault.setObjectName("actionDefault")
        self.actionExit = QtWidgets.QAction(MediaPlayer)
        self.actionExit.setObjectName("actionExit")
        self.menuNetWork_Stream.addAction(self.actionLocal_Video)
        self.menuNetWork_Stream.addAction(self.actionStream_URL)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionMaximize)
        self.menuView.addAction(self.actionMinimize)
        self.menuView.addAction(self.actionDefault)
        self.menuExit.addAction(self.actionExit)
        self.menubar.addAction(self.menuNetWork_Stream.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuExit.menuAction())

        self.retranslateUi(MediaPlayer)
        QtCore.QMetaObject.connectSlotsByName(MediaPlayer)

    def retranslateUi(self, MediaPlayer):
        _translate = QtCore.QCoreApplication.translate
        MediaPlayer.setWindowTitle(_translate("MediaPlayer", "MainWindow"))
        self.timelabel.setText(_translate("MediaPlayer", "00:00/00:00"))
        self.label.setText(_translate("MediaPlayer", "无人机测试平台"))
        self.label_time.setText(_translate("MediaPlayer", "时间：--"))
        self.label_rtmp.setText(_translate("MediaPlayer", "rtmp域名：--"))
        self.label_audio.setText(_translate("MediaPlayer", "音频帧率：--"))
        self.label_video.setText(_translate("MediaPlayer", "视频帧率：--"))
        self.label_bit.setText(_translate("MediaPlayer", "比特率：--"))
        self.menuNetWork_Stream.setTitle(_translate("MediaPlayer", "Open"))
        self.menuView.setTitle(_translate("MediaPlayer", "View"))
        self.menuExit.setTitle(_translate("MediaPlayer", "Exit"))
        self.actionLocal_Video.setText(_translate("MediaPlayer", "Local Video"))
        self.actionStream_URL.setText(_translate("MediaPlayer", "Stream URL"))
        self.actionMaximize.setText(_translate("MediaPlayer", "Maximize"))
        self.actionMaximize.setShortcut(_translate("MediaPlayer", "Alt+A"))
        self.actionMinimize.setText(_translate("MediaPlayer", "Minimize"))
        self.actionMinimize.setShortcut(_translate("MediaPlayer", "Alt+S"))
        self.actionDefault.setText(_translate("MediaPlayer", "Default"))
        self.actionDefault.setShortcut(_translate("MediaPlayer", "Alt+Q"))
        self.actionExit.setText(_translate("MediaPlayer", "Exit"))
        self.actionExit.setShortcut(_translate("MediaPlayer", "Ctrl+W"))
from MatplotlibWidget import MatplotlibWidget
