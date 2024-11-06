import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import serial
import time
import board
import busio
import adafruit_sht31d
import bmp180
import pandas as pd

# 初始化 I2C 和 SHT31 传感器
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)

# 初始化串口
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # 根据实际串口设备修改端口名称和波特率

# 定义输入变量
temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')  # 温度范围 0~50度
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')       # 湿度范围 0~100%

# 定义输出变量
humidifier = ctrl.Consequent(np.arange(0, 2, 1), 'humidifier')     # 加湿器开关（0-关闭，1-开启）
dehumidifier = ctrl.Consequent(np.arange(0, 2, 1), 'dehumidifier') # 除湿器开关（0-关闭，1-开启）
heater = ctrl.Consequent(np.arange(0, 2, 1), 'heater')             # 加热器开关（0-关闭，1-开启）
fan = ctrl.Consequent(np.arange(0, 2, 1), 'fan')                   # 风扇开关（0-关闭，1-开启）

# 定义模糊集合
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['comfortable'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 50])

humidity['dry'] = fuzz.trimf(humidity.universe, [0, 0, 40])
humidity['normal'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['humid'] = fuzz.trimf(humidity.universe, [60, 80, 100])

humidifier['off'] = fuzz.trimf(humidifier.universe, [0, 0, 0])
humidifier['on'] = fuzz.trimf(humidifier.universe, [1, 1, 1])

dehumidifier['off'] = fuzz.trimf(dehumidifier.universe, [0, 0, 0])
dehumidifier['on'] = fuzz.trimf(dehumidifier.universe, [1, 1, 1])

heater['off'] = fuzz.trimf(heater.universe, [0, 0, 0])
heater['on'] = fuzz.trimf(heater.universe, [1, 1, 1])

fan['off'] = fuzz.trimf(fan.universe, [0, 0, 0])
fan['on'] = fuzz.trimf(fan.universe, [1, 1, 1])

# 定义模糊规则

rule1 = ctrl.Rule(temperature['cold'], heater['on'])
rule2 = ctrl.Rule(temperature['cold'], fan['off'])
rule3 = ctrl.Rule(temperature['comfortable'],heater['off'])
rule4 = ctrl.Rule(temperature['comfortable'],fan['off'])
rule5 = ctrl.Rule(temperature['hot'],heater['off'])
rule6 = ctrl.Rule(temperature['hot'],fan['on'])
rule7 = ctrl.Rule(humidity['dry'], humidifier['on'])
rule8 = ctrl.Rule(humidity['dry'], dehumidifier['off'])
rule9 = ctrl.Rule(humidity['normal'], humidifier['off'])
rule10 = ctrl.Rule(humidity['normal'], dehumidifier['off'])
rule11 = ctrl.Rule(humidity['humid'], humidifier['off'])
rule12 = ctrl.Rule(humidity['humid'], dehumidifier['on'])

# 创建控制系统
control_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6,rule7, rule8, rule9, rule10, rule11, rule12])
control = ctrl.ControlSystemSimulation(control_system)

def send_command(device, status):
    if device=="HUMIDIFIER":
      hex_command = "08050001FF00DD63" if status > 0.5 else "0805000100FFDCD3"
    elif device=="DEHUMIDIFIER":
      hex_command = "08050002FF002D63" if status > 0.5 else "0805000200FF2CD3"
    elif device=="HEATER":
      hex_command ="08050003FF007CA3" if status > 0.5 else "0805000300FF7D13"
    elif device=="FAN":
      hex_command = "08050004FF00CD62" if status > 0.5 else "0805000400FFCCD2"

    # 发送HEX指令至串口
    ser.write(bytes.fromhex(hex_command))
    print(f"发送指令: {hex_command}")
    time.sleep(0.1)  # 短暂停顿，确保命令发送完整

# 设置控制逻辑
def update_devices(temp, hum,pressure):
    control.input['temperature'] = temp
    control.input['humidity'] = hum
    # 模拟传感器数据采集
    dict={
          'temperature': [temp],
          'humidity': [hum],
          'pressure': [pressure/100]
          }
    data = pd.DataFrame(dict)
    data.to_csv('data.csv',mode='a',header=False, index=False)
    control.compute()
    #stas= control.output['humidifier']
    #print("status:", stas)
    send_command("HUMIDIFIER", control.output['humidifier'])
    send_command("DEHUMIDIFIER", control.output['dehumidifier'])
    send_command("HEATER", control.output['heater'])
    send_command("FAN", control.output['fan'])

#def fuzzy_control():
while True:
    temp = sensor.temperature
    hum = sensor.relative_humidity
    temp2, pressure, altitude = bmp180.readBmp180()
    print(f"当前温度: {temp:.1f}°C, 湿度: {hum:.1f}%, 气压: {pressure/100:.1f}hpa")
    update_devices(temp, hum,pressure)
    time.sleep(10)  # 每10S检查一次
