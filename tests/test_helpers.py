import pytest
from player_utils import format_time, validate_url

@pytest.mark.parametrize('value,expected', [(-1,'00:00'), (0,'00:00'), (61000,'01:01'), (3661000,'01:01:01')])
def test_time(value, expected):
    assert format_time(value) == expected

@pytest.mark.parametrize('value', ['rtmp://live.example.com/app/stream', ' https://example.com/a.m3u8?token=x ', 'udp://@239.0.0.1:1234'])
def test_valid_urls(value):
    assert validate_url(value) == value.strip()

@pytest.mark.parametrize('value', ['', 'file:///tmp/video', 'https://', 'https://example.com:bad', 'https://example.com/a b'])
def test_invalid_urls(value):
    with pytest.raises(ValueError):
        validate_url(value)
