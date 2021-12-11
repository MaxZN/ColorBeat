import os
import pickle
import math
from datetime import datetime

def save_pkl(filename, dic):
    d = datetime.now()
    curtime = d.strftime('%m%d_%H%M%S')
    oldname = '{}.bk.{}'.format(filename, curtime)
    if os.path.exists(filename):
        os.rename(filename, oldname)

    with open(filename, 'wb') as fo:
        pickle.dump(dic, fo)
        fo.close()

def load_pkl(filename):
    with open(filename, 'rb') as f:
        set = pickle.load(f)
        f.close()
    return set

def get_sells_level(sells):
    if 0<sells<=100000: 
        weight_level = 0
    else:
        weight_level = math.ceil((sells - 100000) / 10000)

def get_sells_weight(sells):
    base_weight = 0.025
    weight_level = get_sells_level(sells)
    weight = base_weight + weight_level*0.001
    return weight

def get_time(date_str):
    year, md, hm = date_str.split('_')
    month = md[:2]
    day = md[2:]
    return int(year), int(month), int(day), hm

def transfer_date2tidx(date_str):
    yr, md, hm = date_str.split('_')
    year = int(yr)
    month = int(md[:2])
    day = int(md[2:])

    day_of_second = 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
    days_of_month = (31, day_of_second, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    # 累加前几个月的总天数
    # total_days = 0
    # for i in range( month -1 ):# 0 1 2 3
    #     total_days += days_of_month[i]
    total_days = sum(days_of_month[: month - 1])

    #  累加当月天数
    total_days += day
    hour_idx = transfer_hm2idx(hm)
    return year, total_days, hour_idx

def transfer_hm2idx(hm):
    hour = int(hm[:2])
    mini = int(hm[2:])
    assert hour in range(0,24)
    assert mini in (0, 30)
    idx = hour * 2 + mini // 30
    return idx

def dayhour2idx(day, hour):
    return day*24 + hour

def idx2dayhour(idx):
    day = idx // 24
    hour = idx % 24
    return day, hour

def main():
    a = '2330'
    print(transfer_hm2idx(a))
if __name__ == '__main__':
    main()