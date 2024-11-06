import snowboydecoder
import os
import coquitts
import time

# 初始化语音合成
coquitts.init()


# 语音合成
start_time = time.time()
ttsfile = coquitts.tts('。')
end_time = time.time()
print(f"耗时: {end_time - start_time} 秒")
print(ttsfile)

