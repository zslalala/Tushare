import datetime
from matplotlib.pylab import date2num

def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.datetime.strptime(date,'%Y%m%d')
        print(date_time)
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time

if __name__ == "__main__":
    datas = ['20190107']
    num_time = date_to_num(datas)
    print(num_time)
