from aliyunsdkcore import client
from aliyunsdklive.request.v20161101 import DescribeLiveDomainBpsDataRequest
from aliyunsdklive.request.v20161101 import DescribeLiveStreamBitRateDataRequest
import json

class Aliyun:
    def __init__(self):
        AK = 'XXXXXXXXXXXXXXXXX'
        Secret = 'XXXXXXXXXXXXXXXXXXXXXXXX'
        self.clt = client.AcsClient(AK, Secret, 'cn-shenzhen')
    def describeLiveStreamBitRateDataRequest(self):
        request = DescribeLiveStreamBitRateDataRequest.DescribeLiveStreamBitRateDataRequest()
        request.set_AppName('apptransvideo')
        request.set_StreamName('streamtransvideo')
        request.set_DomainName('newpullstream.omysycamore.top')
        request.set_StartTime('2021-02-08T00:28:00Z')
        request.set_EndTime('2021-02-09T10:29:00Z')
        result = self.clt.do_action_with_exception(request)
        print(result)
        x = json.loads(result)
        with open('aliyun.json', 'w') as f:
            json.dump(x, f, indent=1)

if __name__ == '__main__':
    aliyun = Aliyun()
    aliyun.describeLiveStreamBitRateDataRequest()