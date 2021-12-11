import numpy as np
import collections
import pickle
import calendar

from numpy.core.defchararray import less

import settings
from funcs import Check
from utils import save_pkl, load_pkl, get_sells_weight, get_time, transfer_date2tidx, dayhour2idx, idx2dayhour
from BaseInfo import LessonInfo

sets = settings.load_settings(settings.SETFILE)
ck = Check()

class DataMap:
    def __init__(self):
        self.datamap = {}
    
    def update_year(self, year, yearmap):
        assert type(year) == YearMap
        self.datamap[year] = yearmap

    def save_dict(self):
        save_pkl(filename='DataMap.pkl', dic=self.datamap)

    def load_dict(self):
        self.datamap = load_pkl(filename='DataMap.pkl')


class YearMap:
    def __init__(self, year):
        # yearmap: ()
        # day(366)*time(48), stunum(50), channel
        # Channel: 0. stuid, 1:teaid, 2: assistid
        self.year_map = np.zeros((366*48, 50, 3))
        self.year = year # int
        self.year_file = 'YearMap_{}.pkl'.format(str(self.year))
        self.default_start = '{}_0101_0000'.format(str(self.year))
        self.default_end = '{}_1231_2330'.format(str(self.year))
    
    def load_year(self, year, yearmap):
        assert type(year) == YearMap
        self.year_map = yearmap
    
    def save_dict(self, file=None):
        yearfile = self.year_file if file is None else file
        save_pkl(filename=yearfile, dic=self.lesson_all)

    def load_dict(self, file=None):
        yearfile = self.year_file if file is None else file
        self.lesson_all = load_pkl(filename=yearfile)

    def update_info(self, lessoninfo):
        assert type(lessoninfo)==LessonInfo
        lessontime = lessoninfo.lessontime
        year, total_days, hour_idx = transfer_date2tidx(lessontime)
        start_idx = dayhour2idx(total_days, hour_idx)
        assert year==self.year

        stulist = lessoninfo.student_list
        teacherid = lessoninfo.teacher
        assistid = lessoninfo.assist
        cost_time = lessoninfo.cost_time

        for i in range(len(stulist)):
            stuid = stulist[i]
            for dh in range(cost_time):
                self.year_map[start_idx + dh][i] = (stuid, teacherid, assistid)
    
    def get_detail_time(self, start_t, end_t):
        if int(start_t[:4])==self.year:
            _, start_day, start_hour = transfer_date2tidx(start_t)
        else:
            _, start_day, start_hour = transfer_date2tidx(self.default_start)

        if int(end_t[:4])==self.year:
            _, end_day, end_hour = transfer_date2tidx(start_t)
        else:
            _, end_day, end_hour = transfer_date2tidx(self.default_start)
        
        start_idx = dayhour2idx(start_day, start_hour)
        end_idx = dayhour2idx(end_day, end_hour)
        return start_idx, end_idx

    def query_stu_learned(self, tgtid, start_t='1900_0101_0000', end_t='2100_1231_2330'):
        start_idx, end_idx = self.get_detail_time(start_t, end_t)
        tgt_learned = []
        for idx in range(start_idx, end_idx):
            for s in range(50):
                stuid, teacherid, assistid = self.year_map[idx][s]
                day, hour = idx2dayhour(idx)
                if stuid == tgtid:
                    tgt_learned.append((day, hour, s, stuid, teacherid, assistid))
        return tgt_learned

    def query_tea_teached(self, tgtid, start_t='1900_0101_0000', end_t='2100_1231_2330'):
        start_idx, end_idx = self.get_detail_time(start_t, end_t)
        tgt_teached = []
        tgt_assist = []
        for idx in range(start_idx, end_idx):
            for s in range(50):
                stuid, teacherid, assistid = self.year_map[idx][s]
                day, hour = idx2dayhour(idx)
                if teacherid == tgtid:
                    tgt_teached.append((day,hour,s,stuid,teacherid,assistid))
                if assistid == tgtid:
                    tgt_assist.append((day,hour,s,stuid,teacherid,assistid))
        return tgt_teached, tgt_assist

def main():
    pass
if __name__ == '__main__':
    main()