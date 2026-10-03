from PyQt5 import QtWidgets
from player_utils import validate_url


class InputURLwin(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('打开网络媒体')
        self.setMinimumWidth(540)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel('直播或网络视频地址'))
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText('https://… / rtmp://… / rtsp://…')
        self.lineEdit.setClearButtonEnabled(True)
        layout.addWidget(self.lineEdit)
        self.error = QtWidgets.QLabel()
        layout.addWidget(self.error)
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('开始播放')
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText('取消')
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

    def accept(self):
        try:
            self.url = validate_url(self.lineEdit.text())
        except ValueError as exc:
            self.error.setText(str(exc))
            return
        super().accept()
