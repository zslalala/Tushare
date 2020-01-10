import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import pandas as pd
import datetime
import os

#获取PATH路径和股票代码(加上了SH和SZ的)
def getPathAndTC(ts_code):
    ts_code = (str)(ts_code)
    if ts_code[0] == '6':
        path = 'D:\StockData\SH\SH'+ts_code+'.csv'
        ts_code = ts_code + '.SH'
        print(path)
    elif (ts_code[0] == '3'or ts_code[0] == '0'):
        path = 'D:\StockData\SZ\SZ'+ts_code+'.csv'
        ts_code = ts_code + '.SZ'
        print(path)
    return ts_code,path

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

#获取股票数据
def getStockData(path,start_date,end_date):
    if not (os.path.exists(path)):
        print('false')
        df_origin = pro.daily(ts_code=ts_code, start_date='20170101', end_date='20200109')
        df_origin.to_csv(path,index=None)
    df_origin = pd.read_csv(path)
    df_origin = df_origin[df_origin.trade_date > (int)(start_date)]
    df_origin = df_origin[df_origin.trade_date < (int)(end_date)]
    df_origin = df_origin.reset_index(drop=True)
    print(df_origin)
    df = df_origin.drop(['ts_code'],axis = 1)
    return df

#主函数
if __name__ == "__main__":

    #tushare认证token，后续提到配置文件
    token = "8fef2d48965386e5b9f7517e0059dc3ea983b9c03214ab673be35442"
    pro = ts.pro_api(token)

    #输入参数，后续提到配置文件
    ts_code = '601211'              #股票代码
    start_date = '20171001'         #开始查询日期
    end_date = '20200110'           #结束查询日期

    #获取股票数据存储路径和上证/深证代码
    ts_code,path = getPathAndTC(ts_code)

    #获取股票数据
    df = getStockData(path,start_date,end_date)

    #调整pandas数组的顺序
    order = ['trade_date','open','close','high','low','pre_close','change','pct_chg','vol','amount']
    df = df[order]

    #绘图部分
    candleDf = df.as_matrix()
    num_time = date_to_num(candleDf[:,0])
    candleDf[:,0] = num_time
    fig, ax = plt.subplots(figsize=(20, 5))
    fig.subplots_adjust(bottom=0.1)
    mpf.candlestick_ochl(ax, candleDf, width=0.6, colorup='r', colordown='g', alpha=1.0)
    plt.grid(True)
    # 设置日期刻度旋转的角度
    plt.xticks(rotation=30)
    plt.title(ts_code)
    plt.xlabel('Date')
    plt.ylabel('Price')
    # x轴的刻度为日期
    ax.xaxis_date()

    #股票分析部分
    #要求一:该天是上涨的,至少上涨0.3%
    df1 = df[df.close > 1.003 * df.open]
    #要求二:上影线不能超过0.5%的收盘价
    df1 = df1[df.high < 1.002 * df.close]
    #要求三:下影线要超过两倍的箱体
    df1 = df1[(df.open - df.low) > 2 * (df.close - df.open) ]
    print(df1)


    # #上影线不能超过0.5%的收盘价
    # df1 = df[(df['high']<1.005*df['close'])]
    # #收盘价要大于1%的开盘价，防止收十字星
    # df2 = df1[df1['close']>1.005 * df1['open']]
    # #全天波动值要大于收盘开盘波动的两倍
    # df3 = df2[((df2['high']-df2['low'])>2 * (df2['close'] - df2['open']))]
    # print(df3.shape)
    # print("满足这样条件的天数:",df3.shape[0]/df.shape[0]*100,"%")
    # print(df3)

    plt.show()