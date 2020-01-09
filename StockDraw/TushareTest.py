import tushare as ts

if __name__ == "__main__":
    pro = ts.pro_api("8fef2d48965386e5b9f7517e0059dc3ea983b9c03214ab673be35442")
    df = pro.daily(ts_code='600398.SH', start_date='20200104', end_date='20200109')
    print(df)