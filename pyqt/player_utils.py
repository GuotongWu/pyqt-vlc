"""Validation and presentation helpers, independent of Qt and VLC."""
from urllib.parse import urlsplit


def validate_url(value):
    value = value.strip()
    parsed = urlsplit(value)
    if parsed.scheme.lower() not in {'http', 'https', 'rtmp', 'rtmps', 'rtsp', 'rtsps', 'udp', 'rtp'} or not parsed.hostname:
        raise ValueError('请输入有效的 HTTP、RTMP、RTSP、UDP 或 RTP 播放地址')
    try:
        parsed.port
    except ValueError as exc:
        raise ValueError('地址端口无效') from exc
    if any(c.isspace() for c in value):
        raise ValueError('地址不能包含空格或换行')
    return value


def format_time(milliseconds):
    seconds = max(0, int(milliseconds)) // 1000
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}' if hours else f'{minutes:02}:{seconds:02}'
