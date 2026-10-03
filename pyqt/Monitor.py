"""Single background worker; never touches widgets or starts extra timers."""
from PyQt5 import QtCore
from aliyun_copy import Aliyun


class Monitor(QtCore.QThread):
    result = QtCore.pyqtSignal(dict)
    failed = QtCore.pyqtSignal(str)

    def run(self):
        try:
            self.result.emit(Aliyun().describeLiveDomainFrameRateAndBitRateData())
        except Exception as exc:
            # SDK exceptions can contain signed request URLs. Do not expose them.
            self.failed.emit('监控请求失败（' + type(exc).__name__ + '），请检查配置、权限及网络')
