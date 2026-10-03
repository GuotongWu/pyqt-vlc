"""Optional Aliyun client. Credentials are read only from the environment."""
import json
import os
from datetime import datetime, timedelta, timezone


class Aliyun:
    def __init__(self):
        from aliyunsdkcore.client import AcsClient
        required = ['ALIBABA_CLOUD_ACCESS_KEY_ID', 'ALIBABA_CLOUD_ACCESS_KEY_SECRET', 'ALIYUN_LIVE_DOMAIN']
        if any(not os.environ.get(key) for key in required):
            raise ValueError('请配置阿里云 AccessKey 和 ALIYUN_LIVE_DOMAIN')
        self.domain = os.environ['ALIYUN_LIVE_DOMAIN']
        self.stream = os.environ.get('ALIYUN_LIVE_STREAM', '')
        self.app = os.environ.get('ALIYUN_LIVE_APP', '')
        self.clt = AcsClient(os.environ[required[0]], os.environ[required[1]],
                             os.environ.get('ALIYUN_REGION', 'cn-shenzhen'),
                             timeout=8, connect_timeout=5, max_retry_time=0)

    def describeLiveDomainFrameRateAndBitRateData(self, time=None):
        from aliyunsdklive.request.v20161101.DescribeLiveDomainFrameRateAndBitRateDataRequest import DescribeLiveDomainFrameRateAndBitRateDataRequest
        request = DescribeLiveDomainFrameRateAndBitRateDataRequest()
        request.set_accept_format('json')
        request.set_DomainName(self.domain)
        request.set_QueryTime(time or (datetime.now(timezone.utc) - timedelta(seconds=120)).strftime('%Y-%m-%dT%H:%M:%SZ'))
        response = json.loads(self.clt.do_action_with_exception(request))
        rows = (response.get('FrameRateAndBitRateInfos') or {}).get('FrameRateAndBitRateInfo') or []
        from urllib.parse import urlsplit
        for row in rows:
            path = urlsplit(row.get('StreamUrl', '')).path.strip('/').split('/')
            stream_name = row.get('StreamName') or (path[-1] if path else '')
            app_name = row.get('AppName') or (path[-2] if len(path) > 1 else '')
            if self.stream and stream_name != self.stream:
                continue
            if self.app and app_name != self.app:
                continue
            return row
        return {}
