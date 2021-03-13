# pyqt-vlc

![](https://img.shields.io/github/languages/top/GuotongWu/pyqt-vlc) ![](https://img.shields.io/github/license/GuotongWu/pyqt-vlc)

这是一个使用python-vlc实现的视频播放客户端，界面使用pyqt5开发的，有本地和视频流url两种方式，可以实现对阿里云直播服务的实时监测。

界面如下：

![image-20210311180730469](https://github.com/GuotongWu/pyqt-vlc/blob/main/src/img1.png)

![image-20210311194145796](https://github.com/GuotongWu/pyqt-vlc/blob/main/src/img2.png)

## 前提条件

已安装python3

## 使用步骤

1. 安装必要的支持

* 安装pyqt

```shell
sudo pip install pyqt
```

* 安装阿里云核心SDK和阿里云直播SDK

```shell
sudo pip install aliyun-python-sdk-core
sudo pip install aliyun-python-sdk-live
```

* 安装针对于Qt的CSS美化工具

```shell
sudo pip install qdarkstyle 
```

* 安装python调用vlc的支持库

```shell
sudo pip install python-vlc
```

2. 将仓库clone到本地

```shell
git clone https://github.com/GuotongWu/pyqt-vlc
```

3. 安装VLC

下载[VLC源码](http://download.videolan.org/pub/videolan/vlc/3.0.11/win64/vlc-3.0.11-win64.zip)，在工程文件中新建vlc-3.0.11文件夹

```shell
mkdir vlc-3.0.11
```

把下载的压缩包中的libvlc.dll、libvlccore.dll及plugins目录都放到到vlc-3.0.11文件夹里面

```shell
cp libvlc.dll libvlccore.dll plugins vlc-3.0.11
```

4. 运行Main.py

```shell
python pyqt/Main.py
```

## 注意

1. 此播放器针对于阿里云SDK，需要结合自己的AccessKey进行使用，即将下面源码中的XXXXXX修改为自己的账号和密码即可。

```python
# aliyun_copy.py
class Aliyun:
    def __init__(self):
        AK = 'xxxxxxxxxxxxxxxxxxxxxxxx'
        Secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.clt = client.AcsClient(AK, Secret, 'cn-shenzhen')
```
2. 播放前需要在适当的位置填写域名，streamName和appName，详情参见[阿里云直播文档](https://help.aliyun.com/document_detail/53272.html?spm=a2c4g.11174283.6.937.1bb2454eZusGK9)

```python
# aliyun_copy.py
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
```