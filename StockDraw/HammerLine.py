import datetime
import os

from TushareTools import exectue
import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts
# import mplfinance as mpf
# from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num
import matplotlib.finance as mpf

#对目标点位进行标注
def drawPoint(df,length,marker,color,size):
    for i in range(length):
        plt.scatter(df.iloc[i].trade_date, df.iloc[i].low, marker=marker, color=color, s=size, label='First')

#df:原始数据的dataframe
#波动率:volatility
#上影线部分:SY_length
#下影线对箱体的倍数:times
def getFormatDFDOWN(df,volatility,SY_length,times):
    # 股票分析部分2
    # 要求一:该天是下跌的，至少下跌0.3%
    df2 = df[df.close < (1-volatility) * df.open]
    # 要求二:上影线不能超过0.5%的开盘价
    df2 = df2[df2.high < (1+SY_length) * df2.open]
    # 要求三:下影线要超过两倍的箱体
    df2 = df2[(df2.close - df2.low) > times * (df2.open - df2.close)]
    print('---------------df2---------------')
    print(df2)

    newdate = []
    for date in df2.trade_date:
        date = (str)(date)
        date_time = datetime.datetime.strptime(date, '%Y%m%d')
        date = date2num(date_time)
        newdate.append(date)
    #画图部分，不用删
    df2_temp = df2.copy()
    df2_temp.trade_date = newdate
    drawPoint(df2_temp, df2_temp.shape[0], 'x', 'black', 100)

    return df2

#df:原始数据的dataframe
#波动率:volatility
#上影线部分:SY_length
#下影线对箱体的倍数:times
def getFormatDFUP(df,volatility,SY_length,times):
    #股票分析部分
    #要求一:该天是上涨的,至少上涨0.3%
    df1 = df[df.close > (1+volatility) * df.open]
    #要求二:上影线不能超过0.5%的收盘价
    df1 = df1[df1.high < (1+SY_length) * df1.close]
    #要求三:下影线要超过两倍的箱体
    df1 = df1[(df1.open - df1.low) > times * (df1.close - df1.open) ]
    print('-----------------df1---------------------')
    print(df1)

    newdate = []
    for date in df1.trade_date:
        date = (str)(date)
        date_time = datetime.datetime.strptime(date, '%Y%m%d')
        date = date2num(date_time)
        newdate.append(date)
    #画图部分，不用了可以删
    df1_temp = df1.copy()
    df1_temp.trade_date = newdate
    drawPoint(df1_temp, df1_temp.shape[0], 'x', 'black', 100)

    return df1

#绘图
def drawPicture(df):
    #绘图部分
    candleDf = df.as_matrix()
    num_time = exectue.date_to_num(candleDf[:,0])
    candleDf[:,0] = num_time
    fig, ax = plt.subplots(figsize=(20, 5))
    fig.subplots_adjust(bottom=0.1)
    mpf.candlestick_ochl(ax, candleDf, width=1, colorup='r', colordown='g', alpha=1.0)
    plt.grid(True)
    # 设置日期刻度旋转的角度
    plt.xticks(rotation=30)
    plt.title(ts_code)
    plt.xlabel('Date')
    plt.ylabel('Price')

    # x轴的刻度为日期
    ax.xaxis_date()



#主函数
if __name__ == "__main__":

    #tushare认证token，后续提到配置文件
    token = "8fef2d48965386e5b9f7517e0059dc3ea983b9c03214ab673be35442"
    pro = ts.pro_api(token)

    #输入参数，后续提到配置文件
    ts_code = '600398'              #股票代码
    start_date = '20170101'         #开始查询日期
    end_date = '20200115'           #结束查询日期

    #获取股票数据存储路径和上证/深证代码
    ts_code,path = exectue.getPathAndTC(ts_code)

    #获取股票数据
    df = exectue.getStockData(path,start_date,end_date,pro,ts_code)

    #调整pandas数组的顺序
    order = ['trade_date','open','close','high','low','pre_close','change','pct_chg','vol','amount']
    df = df[order]

    Aprice,Achg = exectue.GetPriceAfterX(df,20190701,5)
    print(Achg)

    x, Avgb30_temp = exectue.GetPriceBeforeX(df, 20190701, 30)
    print(Avgb30_temp)

    #绘图
    drawPicture(df)

    #上涨锤子线/上吊线
    df1 = getFormatDFUP(df,0.005,0.003,2)

    # 下跌锤子线/上吊线
    df2 = getFormatDFDOWN(df,0.005,0.003,2)

    print(exectue.GetPriceAfterX(df,20170512,10))

    df3 = df1.append(df2)

    Code=[]
    Avgb30=[]
    Avgb15=[]
    Avgb5=[]
    Avgb2=[]
    Avga10=[]
    tradeDate=[]
    for i in range(df3.shape[0]):
        Code.append(ts_code)
        trade_date = (int)(df3.iloc[i].trade_date)
        tradeDate.append(trade_date)
        _, Avgb30_temp = exectue.GetPriceBeforeX(df,trade_date,30)
        _, Avgb15_temp = exectue.GetPriceBeforeX(df,trade_date,15)
        _, Avgb5_temp = exectue.GetPriceBeforeX(df, trade_date, 5)
        _, Avga10_temp = exectue.GetPriceAfterX(df, trade_date, 10)

        #2为震荡，1为涨，0为跌
        if(abs(Avga10_temp) < 0.015):
            Avga10_temp = 2
        elif(Avga10_temp >= 0.015):
            Avga10_temp = 1
        else:
            Avga10_temp = 0

        Avgb30.append(Avgb30_temp)
        Avgb15.append(Avgb15_temp)
        Avgb5.append(Avgb5_temp)
        Avga10.append(Avga10_temp)
    dictionary = {'Avgb30': Avgb30,
                  'Avgb15': Avgb15,
                  'Avgb5': Avgb5,
                  'Avga10':Avga10,
                  'Code':Code,
                  'trade_date':tradeDate
                  }
    frame = pd.DataFrame(dictionary)
    print(frame)
    plt.show()