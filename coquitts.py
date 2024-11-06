from TTS.api import TTS
import time

global ttszh
# 初始化coqui tts
def init():
    global ttszh
    ttszh = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST", progress_bar=False, gpu=False)

# 语音合成（文本转语音）
# text 文本内容
# return 音频文件地址 or None
def tts(text):
    print(text)
    if len(text)==0:
        return None
    try:
        filename='tts' + '.wav'
        global ttszh
        if text.endswith('。'):
             ttszh.tts_to_file(text=text,file_path=filename)
        else:
             ttszh.tts_to_file(text=text+"。",file_path=filename)
        return filename
    except:
        return  None
