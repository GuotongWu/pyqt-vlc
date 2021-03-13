from aliyunsdkcore import client
from aliyunsdklive.request.v20161101 import DescribeLiveDomainBpsDataRequest
from aliyunsdklive.request.v20161101 import DescribeLiveStreamBitRateDataRequest
from aliyunsdklive.request.v20161101 import DescribeLiveDomainFrameRateAndBitRateDataRequest
import json

class Aliyun:
    def __init__(self):
        AK = 'xxxxxxxxxxxxxxxxxxxxxxxx'
        Secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.clt = client.AcsClient(AK, Secret, 'cn-shenzhen')

    def describeLiveStreamBitRateDataRequest(self):
        request = DescribeLiveStreamBitRateDataRequest.DescribeLiveStreamBitRateDataRequest()
        request.set_AppName('填写appName')
        request.set_StreamName('填写streamName')
        request.set_DomainName('填写域名')
        request.set_StartTime('2021-02-08T00:28:00Z')
        request.set_EndTime('2021-02-09T10:29:00Z')
        result = self.clt.do_action_with_exception(request)
        x = json.loads(result)
        with open('aliyun.json', 'w') as f:
            json.dump(x, f, indent=1)
    
    def describeLiveDomainFrameRateAndBitRateData(self, time='2021-02-28T07:45:00Z'):
        request = DescribeLiveDomainFrameRateAndBitRateDataRequest.DescribeLiveDomainFrameRateAndBitRateDataRequest()
        request.set_DomainName('填写推流域名')
        request.set_QueryTime(time)
        result = self.clt.do_action_with_exception(request)
        x = json.loads(result)
        if x['FrameRateAndBitRateInfos']:
            return x['FrameRateAndBitRateInfos']['FrameRateAndBitRateInfo'][0]
        else:
            return {}

if __name__ == '__main__':
    aliyun = Aliyun()
    print(aliyun.describeLiveDomainFrameRateAndBitRateData())