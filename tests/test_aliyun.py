import json
import pytest
pytest.importorskip("aliyunsdkcore")
from unittest.mock import MagicMock
from aliyun_copy import Aliyun


def client(rows):
    api = Aliyun.__new__(Aliyun)
    api.domain = 'live.example.com'
    api.stream = 'selected'
    api.app = 'app'
    api.clt = MagicMock()
    api.clt.do_action_with_exception.return_value = json.dumps({'FrameRateAndBitRateInfos': {'FrameRateAndBitRateInfo': rows}})
    return api


def test_select_stream_by_url_and_utc_query():
    target = {'StreamUrl': 'rtmp://live.example.com/app/selected', 'BitRate': 1500}
    api = client([{'StreamUrl': 'rtmp://live.example.com/app/other'}, target])
    assert api.describeLiveDomainFrameRateAndBitRateData() == target
    request = api.clt.do_action_with_exception.call_args.args[0]
    query = request.get_query_params()
    assert query['DomainName'] == api.domain
    assert query['QueryTime'].endswith('Z')


def test_no_data():
    assert client([]).describeLiveDomainFrameRateAndBitRateData() == {}


def test_missing_stream_does_not_use_another():
    assert client([{'StreamName': 'other', 'AppName': 'app'}]).describeLiveDomainFrameRateAndBitRateData() == {}
