"""Optional HTTP health probe, with no hard-coded server or GUI blocking."""
import os
from urllib.request import urlopen
from player_utils import validate_url


def getStatus(url=None):
    url = validate_url(url or os.environ.get('STREAM_HEALTH_URL', ''))
    if not url.startswith(('http://', 'https://')):
        raise ValueError('健康检查地址必须使用 HTTP 或 HTTPS')
    with urlopen(url, timeout=5) as response:
        return '服务可达' if response.status == 200 else f'HTTP {response.status}'


if __name__ == '__main__':
    print(getStatus())
