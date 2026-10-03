"""Application entry point: python pyqt/Main.py."""
import sys
from PyQt5 import QtCore, QtWidgets
from Call_MainWindow import MainWin


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Stream Studio')
    app.setOrganizationName('pyqt-vlc')
    app.setStyle('Fusion')
    try:
        window = MainWin()
    except (OSError, RuntimeError, NameError) as exc:
        QtWidgets.QMessageBox.critical(None, '无法启动播放器', '无法加载 VLC。请安装与 Python 位数一致的 VLC，并检查 PYTHON_VLC_LIB_PATH。\n' + str(exc))
        return 1
    window.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
