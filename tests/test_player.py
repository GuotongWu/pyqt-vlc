from unittest.mock import MagicMock
import pytest
from PyQt5 import QtWidgets
import vlc
from Call_MainWindow import MainWin
from Call_inputURLwin import InputURLwin

@pytest.fixture(scope='session')
def app():
    return QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

@pytest.fixture
def window(app):
    instance = MagicMock()
    player = instance.media_player_new.return_value
    player.get_state.return_value = vlc.State.NothingSpecial
    player.get_length.return_value = -1
    player.get_time.return_value = -1
    player.get_position.return_value = 0
    player.get_fps.return_value = 0
    player.is_seekable.return_value = False
    player.play.return_value = 0
    win = MainWin(instance=instance)
    yield win
    win.close()


def test_cancel_does_not_create_media(window, monkeypatch):
    monkeypatch.setattr(QtWidgets.QFileDialog, 'getOpenFileName', lambda *a: ('', ''))
    window.open_file()
    window.instance.media_new.assert_not_called()


def test_stream_to_local_resets_mode(window, tmp_path):
    window.play_url('https://example.com/live?token=secret')
    assert window.is_urlplay
    assert 'secret' not in window.source_label.text()
    old_media = window.media
    video = tmp_path / 'video.mp4'
    video.write_bytes(b'placeholder')
    window.load_file(video)
    assert not window.is_urlplay
    old_media.release.assert_called_once()


def test_opening_is_not_mistaken_for_end(window):
    window.mediaplayer.get_state.return_value = vlc.State.Opening
    window.update_ui()
    window.mediaplayer.stop.assert_not_called()
    assert window.state_label.text() == '连接中'


def test_seek_only_when_seekable(window):
    window.set_position()
    window.mediaplayer.set_position.assert_not_called()
    window.mediaplayer.is_seekable.return_value = True
    window.positionslider.setValue(750)
    window.set_position()
    window.mediaplayer.set_position.assert_called_once_with(.75)


def test_missing_cloud_config_disables_schedule(window, monkeypatch):
    monkeypatch.delenv('ALIBABA_CLOUD_ACCESS_KEY_ID', raising=False)
    window.monitor_enabled.setChecked(True)
    assert not window.monitor_timer.isActive()
    assert not window.monitor.isRunning()


def test_dialog_validation(app):
    dialog = InputURLwin()
    dialog.lineEdit.setText('bad')
    dialog.accept()
    assert dialog.result() != QtWidgets.QDialog.Accepted
    dialog.lineEdit.setText('https://example.com/live')
    dialog.accept()
    assert dialog.result() == QtWidgets.QDialog.Accepted
