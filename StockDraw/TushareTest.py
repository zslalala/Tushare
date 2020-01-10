import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import datetime

def date_to_num(dates):
    num_time = []
    for date in dates:
        date = (str)(date)
        date_time = datetime.datetime.strptime(date,'%Y%m%d')
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time

if __name__ == "__main__":
    pro = ts.pro_api("8fef2d48965386e5b9f7517e0059dc3ea983b9c03214ab673be35442")

    df_origin = pro.daily(ts_code='600398.SH', start_date='20190109', end_date='20200109')
    df = df_origin.drop(['ts_code'],axis = 1)
    print(df['trade_date'].dtype)

    print(df[:3])

    order = ['trade_date','open','close','high','low','pre_close','change','pct_chg','vol','amount']
    df = df[order]

    candleDf = df.as_matrix()
    num_time = date_to_num(candleDf[:,0])
    candleDf[:,0] = num_time

    fig, ax = plt.subplots(figsize=(15, 5))
    fig.subplots_adjust(bottom=0.5)
    mpf.candlestick_ochl(ax, candleDf, width=0.6, colorup='r', colordown='g', alpha=1.0)
    plt.grid(True)
    # 设置日期刻度旋转的角度
    plt.xticks(rotation=30)
    plt.title('600398')
    plt.xlabel('Date')
    plt.ylabel('Price')
    # x轴的刻度为日期
    ax.xaxis_date()

    print(df.shape)
    #上影线不能超过0.5%的收盘价
    df1 = df[(df['high']<1.005*df['close'])]
    #收盘价要大于1%的开盘价，防止收十字星
    df2 = df1[df['close']>1.005 * df['open']]
    #全天波动值要大于收盘开盘波动的两倍
    df3 = df2[((df['high']-df['low'])>2 * (df['close'] - df['open']))]
    print(df3.shape)
    print("满足这样条件的天数:",df3.shape[0]/df.shape[0]*100,"%")
    print(df3)

    plt.show()