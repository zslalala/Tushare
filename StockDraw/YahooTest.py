# 导入需要的库
import tushare as ts


if __name__ == "__main__":
    pro = ts.pro_api("8fef2d48965386e5b9f7517e0059dc3ea983b9c03214ab673be35442")
    df_origin = pro.daily(ts_code='002024.SZ', start_date='20170101', end_date='20200109')
    print(df_origin)