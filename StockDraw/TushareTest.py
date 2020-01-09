import tushare as ts

if __name__ == "__main__":
    pro = ts.pro_api("8fef2d48965386e5b9f7517e0059dc3ea983b9c03214ab673be35442")
    df = pro.daily(ts_code='600398.SH', start_date='20190101', end_date='20200109')
    print(df.shape)
    #上影线不能超过0.5%的收盘价
    df1 = df[(df['high']<1.005*df['close'])]
    #收盘价要大于1%的开盘价，防止收十字星
    df2 = df1[df['close']>1.01 * df['open']]
    #全天波动值要大于收盘开盘波动的两倍
    df3 = df2[((df['high']-df['low'])>2 * (df['close'] - df['high']))]
    print(df3.shape)
    print("满足这样条件的天数:",df3.shape[0]/df.shape[0]*100,"%")
    print(df3)
    # print(df[(df['high']<1.005*df['close'])&((df['high']-df['low'])>2 * (df['close'] - df['high']))])