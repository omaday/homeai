import snowboydecoder
import signal
import os
import whisper         # Whisper 用于语音转文本
import ollama
import coquitts
import rec
import time
import board
import busio
import adafruit_sht31d
import bmp180
import opencc
import serial
import tq
#import fuzz
#import subprocess
#from multiprocessing import Process


#subprocess.Popen(['python', 'fuzz.py'])  # 后台运行

os.system("jack_control start")
interrupted = False
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

# 初始化串口
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # 根据实际串口设备修改端口名称和波特率
# 初始化 I2C 和 SHT31 传感器
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)
# 读取温度和湿度

temperature =sensor.temperature
humidity = sensor.relative_humidity
print(f"Temperature: {temperature:.2f} °C")
print(f"Humidity: {humidity:.2f} %")

temp, pressure, altitude = bmp180.readBmp180()
print("Temperature is ",temp)  # degC
print("Pressure is ",pressure) # Pressure in Pa
print("Altitude is ",altitude) # Altitude in meters
print("\n")

# 初始化天气预报
tq.init()

# 初始化语音合成
coquitts.init()

# 唤醒词模型文件
model = '../../resources/models/xdnh.pmdl'

# capture SIGINT signal, e.g., CtrC
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

def read_data(data_type):
    match data_type:
        case 1:
            temperature = int(sensor.temperature)
            return str(temperature)+"度"
        case 2:
            humidity = int(sensor.relative_humidity)
            return "%"+str(humidity)
        case 3:
            temp, pressure, altitude = bmp180.readBmp180()
            pressureh=int(pressure/100)
            return str(pressureh)+"百帕"
        case 4:
            weather=tq.weather(weather)
            return weather
        case 5:
            hex_command = "08050004FF00CD62"
            ser.write(bytes.fromhex(hex_command))
            print(f"发送指令: {hex_command}")
            time.sleep(0.1)  # 短暂停顿，确保命令发送完整
            devicefb="风扇已打开"
            return devicefb
        case 6:
            hex_command = "0805000400FFCCD2"
            ser.write(bytes.fromhex(hex_command))
            print(f"发送指令: {hex_command}")
            time.sleep(0.1)  # 短暂停顿，确保命令发送完整
            devicefb="风扇已关闭"
            return devicefb
        case 7:
            hex_command = "08050001FF00DD63"
            ser.write(bytes.fromhex(hex_command))
            print(f"发送指令: {hex_command}")
            time.sleep(0.1)  # 短暂停顿，确保命令发送完整
            devicefb="加湿器已打开"
            return devicefb
        case 8:
            hex_command = "0805000100FFDCD3"
            ser.write(bytes.fromhex(hex_command))
            print(f"发送指令: {hex_command}")
            time.sleep(0.1)  # 短暂停顿，确保命令发送完整
            devicefb="加湿器已关闭"
            return devicefb
        case 9:
            hex_command = "08050003FF007CA3"
            ser.write(bytes.fromhex(hex_command))
            print(f"发送指令: {hex_command}")
            time.sleep(0.1)  # 短暂停顿，确保命令发送完整
            devicefb="暖风已打开"
            return devicefb
        case 10:
            hex_command = "0805000300FF7D13"
            ser.write(bytes.fromhex(hex_command))
            print(f"发送指令: {hex_command}")
            time.sleep(0.1)  # 短暂停顿，确保命令发送完整
            devicefb="暖风已关闭"
            return devicefb
        case 11:
            hex_command = "08050002FF002D63"
            ser.write(bytes.fromhex(hex_command))
            print(f"发送指令: {hex_command}")
            time.sleep(0.1)  # 短暂停顿，确保命令发送完整
            devicefb="除湿机已打开"
            return devicefb
        case 12:
            hex_command = "0805000200FF2CD3"
            ser.write(bytes.fromhex(hex_command))
            print(f"发送指令: {hex_command}")
            time.sleep(0.1)  # 短暂停顿，确保命令发送完整
            devicefb="除湿器已关闭"
            return devicefb

# 录音之后的回调
# fname 音频文件路径
def audio_recorder_callback(fname):
    #text = offlinedecode.asr(fname)
    print("唤醒词检测到，开始录音...")
    rec.record_audio("temp.wav",6)
    # 使用 Whisper 将录音转为文本
    global whisper_model
    whisper_model = whisper.load_model("base")
    result = whisper_model.transcribe("temp.wav", language="zh",initial_prompt="以下是普通話句子。", fp16=False)
    textft = result["text"]
    cc = opencc.OpenCC("t2s")
    text= cc.convert(textft)
    print("转录文本:", text)
    if len(text) <= 1:
       return
    # 打印识别内容
    if "温度" in text:
       text=read_data(1)
       print(text)
    elif "湿度" in text:
       text=read_data(2)
       print(text)
    elif "气压" in text:
       text=read_data(3)
       print(text)
    elif "天气" in text:
       text=read_data(4)
       print(text)
    elif "打开风扇" in text:
       text=read_data(5)
       print(text)
    elif "关闭风扇" in text:
       text=read_data(6)
       print(text)
    elif "打开加湿器" in text:
       text=read_data(7)
       print(text)
    elif "关闭加湿器" in text:
       text=read_data(8)
       print(text)
    elif "打开暖风" in text:
       text=read_data(9)
       print(text)
    elif "关闭暖风" in text:
       text=read_data(10)
       print(text)
    elif "打开除湿机" in text:
       text=read_data(11)
       print(text)
    elif "关闭除湿机" in text:
       text=read_data(12)
       print(text)
    else:
       print(text)
       # 千问2.5
       #resp = rasabot.ask(text)
       resp = ollama.chat(model='qwen2.5:0.5b', messages=[
       {
         'role': 'user',
         'content': text,
       },
       ])
       print(resp['message']['content'])
       ttsfile = coquitts.tts(resp['message']['content'])
       print(ttsfile)
       if ttsfile != None:
         # 播放音频文件
         snowboydecoder.play_audio_file(fname=ttsfile)
         # 删除录音文件
       if isinstance(fname, str) and os.path.exists(fname):
         if os.path.isfile(fname):
               os.remove(fname)
       return

    #print(resp)
    # 语音合成
    ttsfile = coquitts.tts(text)
    print(ttsfile)
    if ttsfile != None:
      # 播放音频文件
      snowboydecoder.play_audio_file(fname=ttsfile)
      # 删除录音文件
      if isinstance(fname, str) and os.path.exists(fname):
         if os.path.isfile(fname):
               os.remove(fname)
    return
#def wake():
detector.start(detected_callback=snowboydecoder.play_audio_file,
                audio_recorder_callback=audio_recorder_callback,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)

detector.terminate()
# main loop
#p1 = Process(target=fuzz.fuzzy_control())
#p2 = Process(target=wake())
#p1.start()
#p2.start()

