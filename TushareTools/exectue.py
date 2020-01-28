import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts
from matplotlib.pylab import date2num

#获取PATH路径和股票代码(加上了SH和SZ的)
def getPathAndTC(ts_code):
    ts_code = (str)(ts_code)
    if ts_code[0] == '6':
        path = 'E:\StockData\SH\SH'+ts_code+'.csv'
        ts_code = ts_code + '.SH'
        print(path)
    elif (ts_code[0] == '3'or ts_code[0] == '0'):
        path = 'E:\StockData\SZ\SZ'+ts_code+'.csv'
        ts_code = ts_code + '.SZ'
        print(path)
    return ts_code,path

#获取股票数据
def getStockData(path,start_date,end_date,pro,ts_code):
    if not (os.path.exists(path)):
        print('数据库中无记录，需要从网上下载数据，故较慢，请稍候.....')
        df_origin = pro.daily(ts_code=ts_code, start_date='20170101', end_date='20200115')
        df_origin.to_csv(path,index=None)
    df_origin = pd.read_csv(path)
    df_origin = df_origin[df_origin.trade_date > (int)(start_date)]
    df_origin = df_origin[df_origin.trade_date < (int)(end_date)]
    df_origin = df_origin.reset_index(drop=True)
    df = df_origin.drop(['ts_code'],axis = 1)
    return df

#获取某日后x日的交易信息
def GetAfterInformationX(data,date,x):
    target = data[data.trade_date == date]
    targetPrice = target.close.values[0]
    index = target.index.values[0]
    if(index - x < 0):
        searched = data.loc[0:index]
    else:
        searched = data.loc[index-x:index]
    print("---------searched-----------")
    print(searched)
    print("---------searched-----------")
    return searched

#获取某日的前x日平均收盘价格及涨跌幅
def GetPriceBeforeX(data,date,x):
    target = data[data.trade_date == date]
    targetPrice = target.close.values[0]
    index = target.index.values[0]
    maxindex = data.shape[0]
    if(index + x > maxindex):
        searched = data.loc[index:]
    else:
        searched = data.loc[index:index+x]
    print("---------searched-----------")
    print(searched)
    print("---------searched-----------")
    mean_price = searched.close.mean()
    Achg = (targetPrice-mean_price)/mean_price
    return mean_price,Achg

#获取某日的后x日收盘平均价格及涨跌幅
def GetPriceAfterX(data,date,x):
    target = data[data.trade_date == date]
    targetPrice = target.close.values[0]
    index = target.index.values[0]
    if(index - x < 0):
        searched = data.loc[0:index]
    else:
        searched = data.loc[index-x:index]
    print("---------searched-----------")
    print(searched)
    print("---------searched-----------")
    mean_price = searched.close.mean()
    Achg = (mean_price - targetPrice) / targetPrice
    return mean_price,Achg

#将data转化为可以供mpf.candlestick_ochl接口使用的格式
def date_to_num(dates):
    num_time = []
    for date in dates:
        #为什么int转换后会有.0这样的问题
        date = (str)(date)
        date = date[:-2]
        date_time = datetime.datetime.strptime(date,'%Y%m%d')
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time

#获取某日的收盘价格
def GetPrice(data,date):
    target = data[data.trade_date == date]
    price = target.close.values[0]
    return price

#获取股票某点前x日区间的最高价和最低价及目前开盘价所位于的曲线百分比
def GetBeforeXMaxAndMin(data,date,x):
    target = data[data.trade_date == date]
    targetClosePrice = target.close.values[0]
    targetOpenPrice = target.open.values[0]
    index = target.index.values[0]
    maxindex = data.shape[0]
    if(index + x > maxindex):
        searched = data.loc[index:]
    else:
        searched = data.loc[index:index+x]
    # print("---------searched-----------")
    # print(searched)
    # print("---------searched-----------")
    HighMax = searched.high.max()
    LowMin = searched.low.min()
    Percent = (targetOpenPrice - LowMin)/(HighMax - LowMin)
    return HighMax,LowMin,Percent

