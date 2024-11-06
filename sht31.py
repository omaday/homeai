import board
import busio
import adafruit_sht31d

# 初始化 I2C 和 SHT31 传感器
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)

# 读取温度和湿度
temperature = sensor.temperature
humidity = sensor.relative_humidity
print(f"Temperature: {temperature:.2f} °C")
print(f"Humidity: {humidity:.2f} %")
