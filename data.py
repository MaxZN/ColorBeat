import numpy as np
import collections
import pickle
import settings
from funcs import Check

set = settings.load_settings()
class_set = set['class_setting']

class ClassType:
    def __init__(self, times_per_week, class_type):
        pass

class SellInfo:
    '''
    trial: 试听; gift: 赠送; referral: 转介绍; exper: 体验课
    discount: 折扣
    '''
    def __init__(self, 
        basic_num, trial=0, gift=0, referral=0, exper=0, discount=1.0,
        times_per_week=1, class_type=0):
        self.basic_num = basic_num
        self.trial = trial
        self.gift = gift
        self.referral = referral
        self.exper = exper
        self.discount = discount
        assert times_per_week in [1,2]

        # Generated info
        self.total = basic_num + trial + gift + referral + exper

class StudentInfo:
    def __init__(self, 
        name, lname=None, gender=0, #0:male, 1:female
        age=0,
        phone=13800000000,
        class_sell = (0,0,1) # times_per_week, class_type, class_num
        ):
        self.name = name
        self.lname = lname
        self.age = age
        
        Check.basic(gender, phone)
        self.gender = gender
        self.phone = phone

        cnt, class_type, class_num = class_sell
        Check.sell_info(cnt, class_type)

        # update when new sells
        self.cnt = cnt #times_per_week
        self.class_type = class_type #class_type
        self.class_num = class_num

        # update evry time
        self.class_learned_dates = {} # cost_time: [date1, date2]
        for i in set['cost_type']:
            self.class_learned_dates[i] = []
        self.class_res = class_num

        self.print()
    
    def print(self):
        name, age, phone = self.name, self.age, self.phone
        class_type, class_num, class_res = self.class_type, self.class_num, self.class_res
        class_type_info = '{} --- {}'.format(class_set[self.cnt]['name'], class_set[self.cnt][class_type])

        print('Student info: \n')
        print(' >>> Name: {}, Age: {}, PhoneNum: {}'.format(name, age, phone))
        print(' >>> class_info: {}, total_num: {}, class_res: {}'.format(\
            class_type_info, class_num, class_res))

    def more_class(self, class_sell):
        cnt, class_type, class_num = class_sell
        Check.sell_info(cnt, class_type)
        self.cnt = cnt #times_per_week
        self.class_type = class_type #class_type
        self.class_num = class_num
        self.print()

    def learned(self, date_str, cost_time):
        Check.cost_info(date_str, cost_time)
        try:
            assert self.class_res>=cost_time
        except:
            print('Too much class cost!!!')
            print('Last Time Res: {}, This time cost: {}'.format(self.class_res, cost_time))
            exit()

        self.class_learned_dates[cost_time].append(date_str)
        self.class_res -= cost_time
        self.print()

class StudentAll:
    def __init__(self) -> None:
        pass