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
def GetBottomLine(origin_df,df,x,threshold):
    delname = []
    for i in range(df.shape[0]):
        name = df.iloc[i].name
        date = (int)(df.iloc[i].trade_date)
        _,_,percent = exectue.GetBeforeXMaxAndMin(origin_df,date,x)
        if(percent > threshold):
            delname.append(name)
    df = df.drop(delname)
    #测试时间终止于20191201，后面数据不足，不测
    df = df[df.trade_date < 20191201]
    return df

#买入点确定
#origin_data:原始数据
#BWdata:底部长白实体数据
#x:观察时期
#uprate:上涨多少就会入场
#downrate:x日不破长白实体百分比就会入场
def JoinPoint(origin_data,BWdata,x,uprate,downrate):

    BWdate = []
    BWOpen = []
    BWClose = []
    BuyPrice = []
    JoinDate = []
    JoinReason = []

    for i in range((BWdata.shape[0] - 1), -1, -1):
        #flag标注是否处理完毕
        flag = 1
        trade_date = (int)(BWdata.iloc[i].trade_date)
        #保存大阳线的开盘收盘价
        this_open = BWdata.iloc[i].open
        this_close = BWdata.iloc[i].close
        BWOpen.append(this_open)
        BWClose.append(this_close)
        BWdate.append(trade_date)

        joinPrice = (1+uprate)*this_close
        supportPrice = this_open + (this_close - this_open)*downrate

        dfAfter = exectue.GetAfterInformationX(origin_df, trade_date, x)

        for i in range((dfAfter.shape[0] - 2), -1, -1):
            high = dfAfter.iloc[i].high
            low = dfAfter.iloc[i].low
            trade_date = dfAfter.iloc[i].trade_date
            if high > joinPrice:
                flag = 0
                print("joinPrice",joinPrice)
                BuyPrice.append(joinPrice)
                JoinReason.append("上涨超过一定百分比")
                JoinDate.append((int)(trade_date))
                break
            elif low < supportPrice:
                flag = 0
                print("supportPrice",supportPrice)
                BuyPrice.append(-1)
                JoinReason.append("跌破支撑")
                JoinDate.append(-1)
                break
        if flag == 1:
            final_close = dfAfter.iloc[i].close
            BuyPrice.append(final_close)
            JoinReason.append("一定日期未跌破")
            JoinDate.append((int)(trade_date))
            print("final_close",final_close)

        dictionary = {'BWdate': BWdate,
                      'BWOpen': BWOpen,
                      'BWClose': BWClose,
                      'BuyPrice': BuyPrice,
                      'JoinDate': JoinDate,
                      'JoinReason': JoinReason
                      }

        frame = pd.DataFrame(dictionary)
        print(frame)



#主函数
if __name__ == "__main__":

    #tushare认证token，后续提到配置文件
    token = "8fef2d48965386e5b9f7517e0059dc3ea983b9c03214ab673be35442"
    pro = ts.pro_api(token)

    #输入参数，后续提到配置文件
    ts_code = '002572'              #股票代码
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


########################################################
#############数据整理第一部分，筛选底部大阳线###############
########################################################
    #获取大阳线日期集合
    df = GetBigWhite(df,0.04)
    #筛选出底部大阳线
    df = GetBottomLine(origin_df,df,150,0.2)


########################################################
#############第二部分:寻找买点，构建策略###################
########################################################
    #获取后x日交易信息
    JoinPoint(origin_df,df,5,0.03,0.25)
    print("---------------final-------------")
    # dfAfter = exectue.GetAfterInformationX(origin_df,20181022,5)
    # for i in range((dfAfter.shape[0]-1),-1,-1):
    #     print((int)(dfAfter.iloc[i].trade_date))