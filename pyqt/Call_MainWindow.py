import os
import platform
from pathlib import Path
from collections import deque
from PyQt5 import QtCore, QtGui, QtWidgets
import vlc
from Call_inputURLwin import InputURLwin
from Monitor import Monitor
from player_utils import format_time, validate_url

STYLE = '''
QWidget { background: #111827; color: #e5eaf3; font-size: 14px; }
QMainWindow { background: #111827; }
QLabel, QCheckBox { background: transparent; }
QFrame#panel { background: #1b2638; border-radius: 12px; }
QLabel#title { font-size: 25px; font-weight: 600; }
QLabel#subtitle { color: #91a0b8; }
QPushButton { background: #26354b; border: 1px solid #35445b; border-radius: 7px; padding: 9px 14px; }
QPushButton:hover { background: #354762; }
QPushButton:disabled { color: #69788d; }
QPushButton#primary { background: #3478f6; border: none; }
QSlider::groove:horizontal { height: 5px; background: #35445b; border-radius: 2px; }
QSlider::sub-page:horizontal { background: #4d8dff; }
QSlider::handle:horizontal { background: #eef4ff; width: 13px; margin: -4px 0; border-radius: 6px; }
QLineEdit { background: #0c1422; border: 1px solid #35445b; padding: 10px; border-radius: 6px; }
QMenu { background: #1b2638; } QMenu::item:selected { background: #3478f6; }
QStatusBar { color: #91a0b8; }
'''


class HistoryChart(QtWidgets.QWidget):
    """Bounded local decode-FPS history; no network or animation timers."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.values = deque(maxlen=120)
        self.setMinimumHeight(120)

    def append(self, value):
        self.values.append(max(0, float(value)))
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        area = self.rect().adjusted(8, 12, -8, -22)
        painter.setPen(QtGui.QColor('#304057'))
        for i in range(4):
            y = area.top() + area.height() * i / 3
            painter.drawLine(QtCore.QPointF(area.left(), y), QtCore.QPointF(area.right(), y))
        if len(self.values) > 1:
            peak = max(30, max(self.values))
            path = QtGui.QPainterPath()
            for index, value in enumerate(self.values):
                point = QtCore.QPointF(area.left() + index * area.width() / (self.values.maxlen - 1), area.bottom() - value / peak * area.height())
                path.moveTo(point) if index == 0 else path.lineTo(point)
            painter.setPen(QtGui.QPen(QtGui.QColor('#57b6ff'), 2))
            painter.drawPath(path)
        painter.setPen(QtGui.QColor('#91a0b8'))
        painter.drawText(8, self.height() - 4, '本地解码帧率 · 最近 120 秒')


class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None, instance=None):
        super().__init__(parent)
        self.setWindowTitle('Stream Studio · 视频与直播播放器')
        self.resize(1200, 760)
        self.setMinimumSize(820, 540)
        self.setStyleSheet(STYLE)
        self.instance = instance if instance is not None else vlc.Instance('--no-video-title-show', '--network-caching=1200')
        if self.instance is None:
            raise RuntimeError('VLC 初始化失败')
        self.mediaplayer = self.instance.media_player_new()
        self.media = None
        self.is_urlplay = False
        self._closing = False
        self._ticks = 0
        self._last_state = None
        self.settings = QtCore.QSettings('pyqt-vlc', 'StreamStudio')
        self._build_ui()
        self.monitor = Monitor(self)
        self.monitor.result.connect(self._monitor_result)
        self.monitor.failed.connect(self.monitor_status.setText)
        self.monitor.finished.connect(self._monitor_finished)
        self.monitor_timer = QtCore.QTimer(self)
        self.monitor_timer.setInterval(30000)
        self.monitor_timer.timeout.connect(self.request_monitor)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start()
        self.volumeslider.setValue(int(self.settings.value('volume', 80)))
        self.set_volume(self.volumeslider.value())
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        self.setAcceptDrops(True)

    def _button(self, text, callback, layout):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(callback)
        layout.addWidget(button)
        return button

    def _build_ui(self):
        root = QtWidgets.QWidget()
        self.setCentralWidget(root)
        layout = QtWidgets.QVBoxLayout(root)
        layout.setContentsMargins(24, 18, 24, 12)
        layout.setSpacing(16)
        header = QtWidgets.QHBoxLayout()
        titles = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel('STREAM STUDIO')
        title.setObjectName('title')
        titles.addWidget(title)
        subtitle = QtWidgets.QLabel('视频播放 / 直播监看')
        subtitle.setObjectName('subtitle')
        titles.addWidget(subtitle)
        header.addLayout(titles)
        header.addStretch()
        self._button('打开文件', self.open_file, header)
        self._button('打开直播 URL', self.open_url_dialog, header).setObjectName('primary')
        layout.addLayout(header)
        split = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        left = QtWidgets.QWidget()
        video_layout = QtWidgets.QVBoxLayout(left)
        video_layout.setContentsMargins(0, 0, 0, 0)
        self.source_label = QtWidgets.QLabel('准备就绪 · 打开文件或拖入视频开始播放')
        self.source_label.setWordWrap(True)
        video_layout.addWidget(self.source_label)
        self.videoframe = QtWidgets.QFrame()
        self.videoframe.setAttribute(QtCore.Qt.WA_NativeWindow)
        self.videoframe.setStyleSheet('background: #050a12; border-radius: 8px;')
        video_layout.addWidget(self.videoframe, 1)
        seek = QtWidgets.QHBoxLayout()
        self.timelabel = QtWidgets.QLabel('00:00 / 00:00')
        self.positionslider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.positionslider.setRange(0, 1000)
        self.positionslider.setEnabled(False)
        self.positionslider.sliderReleased.connect(self.set_position)
        seek.addWidget(self.timelabel)
        seek.addWidget(self.positionslider, 1)
        video_layout.addLayout(seek)
        controls = QtWidgets.QHBoxLayout()
        self.playButton = self._button('播放', self.play_pause, controls)
        self._button('停止', self.stop, controls)
        controls.addStretch()
        self.soundButton = self._button('静音', self.set_mute, controls)
        self.volumeslider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volumeslider.setRange(0, 100)
        self.volumeslider.setMaximumWidth(130)
        self.volumeslider.valueChanged.connect(self.set_volume)
        controls.addWidget(self.volumeslider)
        self._button('全屏', self.set_fscreen, controls)
        video_layout.addLayout(controls)
        split.addWidget(left)
        panel = QtWidgets.QFrame()
        panel.setObjectName('panel')
        panel.setMinimumWidth(245)
        side = QtWidgets.QVBoxLayout(panel)
        side.setContentsMargins(18, 20, 18, 20)
        side.addWidget(QtWidgets.QLabel('播放概况'))
        self.state_label = QtWidgets.QLabel('待机')
        self.state_label.setStyleSheet('color: #67c7ff; font-size: 22px;')
        side.addWidget(self.state_label)
        self.fps_label = QtWidgets.QLabel('解码帧率  —')
        side.addWidget(self.fps_label)
        self.chart = HistoryChart()
        side.addWidget(self.chart)
        side.addSpacing(18)
        side.addWidget(QtWidgets.QLabel('阿里云直播监控'))
        self.monitor_status = QtWidgets.QLabel('未启用 · 需配置环境变量')
        self.monitor_status.setWordWrap(True)
        side.addWidget(self.monitor_status)
        self.cloud_metrics = QtWidgets.QLabel('视频帧率 —\n音频帧率 —\n码率 —')
        side.addWidget(self.cloud_metrics)
        self.monitor_enabled = QtWidgets.QCheckBox('启用监控（每 30 秒）')
        self.monitor_enabled.toggled.connect(self.toggle_monitor)
        side.addWidget(self.monitor_enabled)
        self.getStatusButton = self._button('立即刷新', self.request_monitor, side)
        side.addStretch()
        note = QtWidgets.QLabel('Space 播放 / 暂停\nF 全屏 · Esc 退出全屏\nCtrl+O 打开文件 · Ctrl+L 打开 URL')
        note.setWordWrap(True)
        note.setObjectName('subtitle')
        side.addWidget(note)
        split.addWidget(panel)
        split.setStretchFactor(0, 4)
        split.setStretchFactor(1, 1)
        layout.addWidget(split, 1)
        for key, callback in [('Space', self.play_pause), ('F', self.set_fscreen), ('Escape', self.exit_fullscreen), ('Ctrl+O', self.open_file), ('Ctrl+L', self.open_url_dialog)]:
            QtWidgets.QShortcut(QtGui.QKeySequence(key), self, activated=callback)
        self.statusBar().showMessage('支持本地视频、HTTP、RTMP 与 RTSP 网络媒体')

    def set_platform(self):
        handle = int(self.videoframe.winId())
        if platform.system() == 'Windows':
            self.mediaplayer.set_hwnd(handle)
        elif platform.system() == 'Darwin':
            self.mediaplayer.set_nsobject(handle)
        else:
            self.mediaplayer.set_xwindow(handle)

    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开媒体文件', self.settings.value('directory', str(Path.home())), '媒体文件 (*.mp4 *.mkv *.avi *.mov *.webm *.mp3 *.flac *.wav *.ts);;所有文件 (*)')
        if filename:
            self.load_file(filename)

    def load_file(self, filename):
        path = Path(filename).expanduser().resolve()
        if not path.is_file():
            self.statusBar().showMessage('文件不存在或不可访问')
            return
        self.settings.setValue('directory', str(path.parent))
        self._load(str(path), False, path.name)

    def open_url_dialog(self):
        dialog = InputURLwin(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.play_url(dialog.url)

    def play_url(self, url):
        try:
            url = validate_url(url)
        except ValueError as exc:
            self.statusBar().showMessage(str(exc))
            return
        # Do not show signed playback URLs in the window or save them to settings.
        from urllib.parse import urlsplit
        self._load(url, True, '网络媒体 · ' + urlsplit(url).hostname)

    def _load(self, source, is_url, title):
        self.mediaplayer.stop()
        previous = self.media
        self.media = self.instance.media_new(source)
        self.mediaplayer.set_media(self.media)
        if previous:
            previous.release()
        self.is_urlplay = is_url
        self.chart.values.clear()
        self.chart.update()
        self.positionslider.setValue(0)
        self.set_platform()
        self.source_label.setText(title)
        self._last_state = None
        if self.mediaplayer.play() == -1:
            self.statusBar().showMessage('无法播放该媒体，请检查文件或网络地址')
        else:
            self.statusBar().showMessage('正在加载媒体…')

    def play_pause(self):
        if self.media is None:
            self.open_file()
            return
        state = self.mediaplayer.get_state()
        if state == vlc.State.Playing:
            self.mediaplayer.set_pause(1)
        elif state == vlc.State.Paused:
            self.mediaplayer.set_pause(0)
        elif state not in (vlc.State.Opening, vlc.State.Buffering):
            if self.mediaplayer.play() == -1:
                self.statusBar().showMessage('播放失败')
        self.update_ui()

    def stop(self):
        self.mediaplayer.stop()
        self.positionslider.setValue(0)
        self.update_ui()

    def set_position(self):
        if self.mediaplayer.is_seekable():
            self.mediaplayer.set_position(self.positionslider.value() / 1000)

    def set_volume(self, volume):
        self.mediaplayer.audio_set_volume(volume)
        self.settings.setValue('volume', volume)

    def set_mute(self):
        muted = not bool(self.mediaplayer.audio_get_mute())
        self.mediaplayer.audio_set_mute(muted)
        self.soundButton.setText('取消静音' if muted else '静音')

    def calculate_time(self):
        length = self.mediaplayer.get_length()
        return format_time(self.mediaplayer.get_time()) + ' / ' + (format_time(length) if length > 0 else ('LIVE' if self.is_urlplay else '00:00'))

    def update_ui(self):
        state = self.mediaplayer.get_state()
        states = {vlc.State.NothingSpecial: '待机', vlc.State.Opening: '连接中', vlc.State.Buffering: '缓冲中', vlc.State.Playing: '播放中', vlc.State.Paused: '已暂停', vlc.State.Stopped: '已停止', vlc.State.Ended: '播放结束', vlc.State.Error: '播放失败'}
        self.state_label.setText(states.get(state, '待机'))
        self.playButton.setText('暂停' if state == vlc.State.Playing else '播放')
        self.positionslider.setEnabled(bool(self.mediaplayer.is_seekable()))
        if not self.positionslider.isSliderDown():
            self.positionslider.setValue(max(0, int(self.mediaplayer.get_position() * 1000)))
        self.timelabel.setText(self.calculate_time())
        fps = max(0, self.mediaplayer.get_fps())
        self.fps_label.setText(f'解码帧率  {fps:.1f} fps')
        self._ticks += 1
        if self._ticks % 4 == 0 and state == vlc.State.Playing:
            self.chart.append(fps)
        if state != self._last_state:
            if state == vlc.State.Error:
                self.statusBar().showMessage('媒体播放失败，请检查地址有效期、网络、权限或编解码器')
            elif state == vlc.State.Playing:
                self.statusBar().showMessage('媒体播放中')
            self._last_state = state

    def set_fscreen(self):
        self.showNormal() if self.isFullScreen() else self.showFullScreen()

    def exit_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()

    def toggle_monitor(self, enabled):
        if enabled:
            self.monitor_timer.start()
            self.request_monitor()
        else:
            self.monitor_timer.stop()
            self.monitor_status.setText('监控已关闭')

    def request_monitor(self):
        if self._closing or self.monitor.isRunning():
            return
        required = ('ALIBABA_CLOUD_ACCESS_KEY_ID', 'ALIBABA_CLOUD_ACCESS_KEY_SECRET', 'ALIYUN_LIVE_DOMAIN')
        if any(not os.environ.get(key) for key in required):
            self.monitor_status.setText('缺少配置：AccessKey / ALIYUN_LIVE_DOMAIN')
            self.monitor_enabled.setChecked(False)
            return
        self.getStatusButton.setEnabled(False)
        self.monitor_status.setText('正在查询…')
        self.monitor.start()

    def _monitor_result(self, data):
        self.monitor_status.setText('更新于 ' + QtCore.QDateTime.currentDateTime().toString('HH:mm:ss') + ' · 云端数据约延迟 2 分钟' if data else '暂无数据，请检查流名称与推流状态')
        self.cloud_metrics.setText('视频帧率 {} fps\n音频帧率 {} fps\n码率 {} bps'.format(data.get('VideoFrameRate', '—'), data.get('AudioFrameRate', '—'), data.get('BitRate', '—')))

    def _monitor_finished(self):
        self.getStatusButton.setEnabled(True)
        if self._closing:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        self.monitor_timer.stop()
        if not self._closing:
            self.settings.setValue('geometry', self.saveGeometry())
        self._closing = True
        if self.monitor.isRunning():
            self.hide()
            event.ignore()
            return
        self.mediaplayer.stop()
        self.mediaplayer.release()
        if self.media:
            self.media.release()
        self.instance.release()
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and any(url.isLocalFile() for url in event.mimeData().urls()):
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile():
                self.load_file(url.toLocalFile())
                event.acceptProposedAction()
                break
