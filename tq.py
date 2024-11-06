import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from datetime import date

def init():
    # 模拟传感器数据采集
    data = pd.DataFrame({
          'temperature': np.random.uniform(15, 25, 100),
          'humidity': np.random.uniform(40, 60, 100),
          'pressure': np.random.uniform(1000, 1020, 100)
          })
    data.to_csv('data.csv', index=False)
def weather(weather):
    # 加载数据
    data = pd.read_csv('data.csv')
    # 判断行数是否超过1000
    if len(data) > 1000:
       # 保留最后100行
       data = data.tail(100)

    # 将结果保存回CSV文件
    data.to_csv('data.csv', index=False)
    # 加载数据
    data = pd.read_csv('data.csv')
    # 设定时间索引
    data['time'] = pd.date_range(start=date.today(), periods=len(data), freq='T')
    data.set_index('time', inplace=True)

    # ARIMA模型预测温度
    model = ARIMA(data['temperature'], order=(5, 1, 0))
    model_fit1 = model.fit()
    model = ARIMA(data['humidity'], order=(5, 1, 0))
    model_fit2 = model.fit()
    model = ARIMA(data['pressure'], order=(5, 1, 0))
    model_fit3 = model.fit()
    # 预测未来30分钟
    forecast1 = model_fit1.forecast(steps=30)
    print("未来30分钟温度预测值:", forecast1[29])
    forecast2 = model_fit2.forecast(steps=30)
    print("未来30分钟湿度预测值:", forecast2[29])
    forecast3 = model_fit3.forecast(steps=30)
    print("未来30分钟气压预测值:", forecast3[29])
    if(forecast2[29]>80)and(forecast3[29]<1000):
       werther="预计30分钟后有雨，请带伞"
       print(weather)
    else:
       werther="预计未来半小时没有雨"
       print(weather)
    return weather
