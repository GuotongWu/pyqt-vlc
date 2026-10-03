"""Compatibility chart widget for the archived Qt Designer layouts.

The active UI uses HistoryChart and has no Matplotlib dependency or network timer.
"""
from PyQt5 import QtWidgets
from Call_MainWindow import HistoryChart


class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.mpl = HistoryChart(self)
        layout.addWidget(self.mpl)
