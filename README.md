# homeai

#############################################

运行语音大模型程序
python homeai.py
#############################################
运行自动控制程序
python fuzz.py

##############################################

安装依赖库

修改swap分区配置（树莓派2G版本，其他版本可以忽略）
sudo nano /etc/dphys-swapfile
想设置4GiB的swap分区，可以设置“CONF_SWAPSIZE=4096
sudo /etc/init.d/dphys-swapfile restart
free -h

配置USB声卡
aplay -l
找到设备号2（USB声卡）
sudo nano /usr/share/alsa/alsa.conf
修改为2
defaults.ctl.card 2
defaults.pcm.card 2

sudo nano ~/.asoundrc
pcm.!default {
    type hw
    card 2
}

ctl.!default {
    type hw
    card 2
}

使用图形界面，可以右键点击任务栏上的音量图标，选择“音频输出设备”，并选择USB音频设备。

重启测试声卡

安装TTS
pip install coqui-tts  # from PyPI

error: can't find Rust compiler
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh 
 
pip install coqui-tts[zh]


测试（中文一定要加句号，不然会拖拉音）
tts --text "首次运行时的模型加载可能比较耗时。可以在初始化时预加载模型，以减少实际合成时的等待时间，尤其在需要连续使用的应用中效果明显。" \
    --model_name "tts_models/zh-CN/baker/tacotron2-DDC-GST" \
    --out_path output.wav


最新版本的Snowboy软件下载到Raspberry Pi上，运行以下命令来解压它。

请确认你位于Pi用户的主目录中。( /home/pi 或 ~)

snowboy编译出Makefile:73: recipe for target ‘_snowboydetect.so‘ failed


jack_control start

2.2 安装PyAudio,这个在requirements.txt里面要求了。

  PyAudio 提供了 PortAudio 的 Python 语言版本，所以上面要安装portaudio。

sudo pip install pyaudio
2.3 安装其它依赖包

sudo apt-get install swig sox libpcre3 libpcre3-dev libatlas-base-dev
3 安装Python2版本

cd snowboy/swig/Python
make
生成 _snowboydetect.so 就编译成功了
4 常见错误

 …/…/lib/ubuntu64/libsnowboy-detect.a:error adding symbols: File in wrong format
此错误是Makefile中没有使用正确版本的libsnowboy-detect.a

在snowboy/lib下一共有

aarch64-ubuntu1604/    --对应arm64 ubuntu1604,经验证ubuntu1804也可以使用
android/                         --对应android系统
ios/                                 --对应ios系统
node/
osx/                                 --对应macos
rpi/                                   --对应树莓派32位arm
ubuntu64/                        --对应PC Ubuntu64

其它系统，查询电脑类型就可以知道用上面哪个了

uname -m
因此按下面修改Makefile就可以解决这个问题了

SNOWBOYDETECTLIBFILE = $(TOPDIR)/lib/ubuntu64/libsnowboy-detect.a
ifneq (,$(findstring arm,$(shell uname -m)))
  SNOWBOYDETECTLIBFILE = $(TOPDIR)/lib/rpi/libsnowboy-detect.a
  ifeq ($(findstring fc,$(shell uname -r)), fc) 
    #fedora25-armv7这个没看到
    SNOWBOYDETECTLIBFILE = $(TOPDIR)/lib/fedora25-armv7/libsnowboy-detect.a
    LDLIBS := -L/usr/lib/atlas -lm -ldl -lsatlas
  endif
endif
 
#以下修改内容请根据系统选择，这里环境为ubuntu1804
ifneq (,$(findstring aarch64,$(shell uname -m)))
  SNOWBOYDETECTLIBFILE = $(TOPDIR)/lib/aarch64-ubuntu1604/libsnowboy-detect.a
endif
 
或者前面全部注释，用下面这句
SNOWBOYDETECTLIBFILE = $(TOPDIR)/lib/aarch64-ubuntu1604/libsnowboy-detect.a
5 测试

cd snowboy/examples/Python
python demo.py ../resources/models/snowboy.umdl
对着话筒说snowboy，如果出现以下提示，并听到叮的一声，就表示成功了。

INFO:snowboy:Keyword 1 detected at time: 2020-09-18 11:47:32
测试如果出现--问题1

Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
请安装jackd2

apt-get install -y jackd2
 
#pulseaudio --kill关闭 --start启动
jack_control start #启动 status查看状态 exit退出
安装jackd2后重启一下，否则可能出现--问题2

Cannot lock down 82274202 byte memory area (Cannot allocate memory)
python3版本可能出现问题3

 from . import snowboydetect
ImportError: attempted relative import with no known parent package
在目录example/Python3中添加空的__init__.py，另外在snowboydecoder.py

#!/usr/bin/env python
改为
#!/usr/bin/env python3
 
from . import snowboydetect
改为
import snowboydetect
问题3

出现了IOError: [Errno -9996] Invalid output device (no default output device)

原因是系统没有音频输出设备（喇叭、音箱）或者没有配置好。因为检测到唤醒词后会播放Ding.wav的声音。另外给两个关键词almixer和aplay。


安装Whisper（语音识别）
pip install -U openai-whisper

升级
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

安装必备库
sudo apt update && sudo apt install ffmpeg

whisper test.wav --model tiny --language zh

import whisper

model = whisper.load_model("tiny")
result = model.transcribe("test.mp3", fp16=False)
print(result["text"])

简体繁体不区分问题：
prompt='以下是普通话的句子'
result = model.transcribe(audioFile, task='translate',language='zh',verbose=True,initial_prompt=prompt)

pip install opencc

import opencc
cc = opencc.OpenCC(“t2s”)
simplified_result = cc.convert('漢字')  
print(“简体格式：”, simplified_result)
#输出结果为 简体格式：汉字


安装本地大模型，推荐qwen0.5b


然后安装
pip3 install ollama
测试不要用ollama.py命名

天气预测依赖库
pip install pandas scikit-learn statsmodels

自动化模糊控制依赖库
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


