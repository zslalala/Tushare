import datetime
import os

from TushareTools import exectue
import pandas as pd
import tushare as ts

#筛选出大阳线
def GetBigWhite(df,rate):
    df = df[df.close > (1+rate) * df.open]
    return df

#筛选底部大阳线
def GetBottomLine(origin_df,df,x):
    print(df)
    for i in range(df.shape[0]):
        date = (int)(df.iloc[i].trade_date)
        _,_,percent = exectue.GetBeforeXMaxAndMin(origin_df,date,x)
        if(percent < 0.2):
            print(df.iloc[i])

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

    #保存原始数据
    origin_df = df.copy()
    #获取大阳线日期集合
    df = GetBigWhite(df,0.04)

    GetBottomLine(origin_df,df,150)