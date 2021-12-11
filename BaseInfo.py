import numpy as np
import collections
import pickle
import calendar

import settings
from funcs import Check
from utils import save_pkl, load_pkl, get_sells_weight, get_time

sets = settings.load_settings(settings.SETFILE)
ck = Check()

class SellInfo:
    '''
    课程数目：basic_num: 基础课程包; trial: 试听; gift: 赠送; referral: 转介绍; exper: 体验课
    价格计算：baseMoney: 基础价格, discount: 折扣, discountMoney: [] 抵扣(体验+团报+转介绍)
    >> income_cal = baseMoney*basic_num*discount - sum(discountMoney)
    收入统计:income_cal: 需缴费, income_done: 实缴费, income_res: 待缴费
    '''
    def __init__(self, 
        basic_num, trial=0, gift=0, referral=0, exper=0,
        times_per_week=1, class_type=0, 
        baseMoney=160, income=None, discount=1.0, discountMoney=[0,0,0],
        seller='yiyi'):
        self.basic_num = basic_num
        self.trial = trial
        self.gift = gift
        self.referral = referral
        self.exper = exper
        assert times_per_week in sets['class_type'].keys()
        assert class_type in sets['class_type'][times_per_week].keys()

        # Money
        income_cal = baseMoney*basic_num*discount - sum(discountMoney)
        self.income_cal = income_cal
        self.income_done = income
        self.discount = discount
        self.income_res = income_cal - income

        self.seller = seller

        # Lesson Generated info
        total = basic_num + trial + gift + referral + exper
        self.class_sell = (times_per_week, class_type, total)

class TeacherInfo:
    '''
    name, phone, base: 基础薪资, lessonfee: 课时费    

    WorkDay: normal: 正常上班; intern: 试用; ill: 请假
    SellMoney: IntroValue=0, CoSell=0, IndiSell=0
    LessonType: assist: 助教; formal: 正式; 
    '''
    def __init__(self, name, phone, startdate='1900_0101',
        base=0, lessonfee=12):
        self.name = name
        self.phone = phone
        self.startdate = startdate

        self.lessonfee = lessonfee
        self.base = base
        self.fee_list = {}
        self.formal_list = {}
        self.assist_list = {}
    
    def update_info(self, base=None, lessonfee=None):
        if base is not None:
            self.base = base
        if lessonfee is not None:
            self.lessonfee = lessonfee
    
    def update_learned(self, date_str, cost_time, is_formal=True):
        ck.cost_info(date_str, cost_time)
        # TODO
        if date_str not in self.formal_list:
            self.formal_list[date_str] = 0
            self.assist_list[date_str] = 0 #TODO
        if is_formal:
            pass

        self.class_learned_dates[cost_time].append(date_str)
        self.class_res -= cost_time
        self.print()
    
    def get_monthly_fee(self, year, month, tax=0, 
        intern = 0, ill=0, 
        IntroValue=0, CoSell=0, IndiSell=0,
        assist=0, formal=0):

        date_str = '{}_{:02d}'.format(year, month)
        alldays = calendar.monthrange(year, month)[1]
        normal = alldays - intern - ill
        fee_list = {}
        fee_list['base'] = self.base
        fee_list['lessonfee'] = self.lessonfee
        fee_list['tax'] = tax

        fee_list['workdays'] = (normal, ill, intern)
        fee_list['workdays_str'] = '工作: {}, 请假: {}, 实习: {}'.format(normal, ill, intern)

        fee_list['detail'] = {}
        fee_list['detail']['base_fee'] = self.base * (normal / alldays) + self.base * (intern / alldays) * 0.8

        fee_list['detail']['IntroTotal'] = IntroValue * sets['sell_weight']['IntroWeight']
        fee_list['detail']['CoTotal'] = CoSell * sets['sell_weight']['coWeight']
        fee_list['detail']['IndiSellTotal'] = IndiSell*get_sells_weight(IndiSell)

        fee_list['detail']['assistfee'] = assist * sets['fees']['assistfee']
        fee_list['detail']['formalfee'] = formal * self.lessonfee

        fee_list['total'] = sum(list(fee_list['detail'].values()))

        self.fee_list[date_str] = fee_list

class TeacherAllInfo:
    def __init__(self):
        self.cur_id = 0
        self.teacher_dict = {} # id: TeacherInfo
    
    def save_dict(self):
        save_pkl(filename='Teacher_All_Info.pkl', dic=self.teacher_dict)

    def load_dict(self):
        self.teacher_dict = load_pkl(filename='Teacher_All_Info.pkl')
    
    def update_info(self, personal):
        assert type(personal)==TeacherAllInfo
        self.teacher_dict[self.cur_id] = personal #vars(personal)
        self.cur_id += 1
    
    def modify_info(self, personal, id):
        assert type(personal)==TeacherAllInfo
        self.teacher_dict[id] = personal

class StudentInfo:
    def __init__(self, 
        name, lname=None, gender=0, #0:male, 1:female
        age=0,
        phone=13800000000,
        class_sell = (0,0,0), # times_per_week, class_type, class_num
        ps_info='blank Info'):
        self.name = name
        self.lname = lname
        self.age = age
        
        ck.basic(gender, phone)
        self.gender = gender
        self.phone = phone

        self.ps_info = [ps_info]

        times_per_week, class_type, class_num = class_sell
        ck.sell_info(times_per_week, class_type)

        # update when new sells
        self.times_per_week = times_per_week #times_per_week
        self.class_type = class_type #class_type
        self.class_num = class_num

        # update every time
        self.class_learned_dates = {} # cost_time: [date1, date2]
        for i in sets['cost_type']:
            self.class_learned_dates[i] = []
        self.class_res = class_num

        self.print()
    
    def print(self):
        class_set = sets['class_setting']
        name, age, phone = self.name, self.age, self.phone
        class_type, class_num, class_res = self.class_type, self.class_num, self.class_res
        class_type_info = '{} --- {}'.format(class_set[self.times_per_week]['name'], class_set[self.times_per_week][class_type])

        print('Student info: \n')
        print(' >>> Name: {}, Age: {}, PhoneNum: {}'.format(name, age, phone))
        print(' >>> class_info: {}, total_num: {}, class_res: {}'.format(\
            class_type_info, class_num, class_res))

    def update_sells(self, class_sell):
        times_per_week, class_type, class_num = class_sell
        ck.sell_info(times_per_week, class_type)
        self.times_per_week = times_per_week #times_per_week
        self.class_type = class_type #class_type
        self.class_num += class_num
        self.print()

    def update_learned(self, date_str, cost_time):
        ck.cost_info(date_str, cost_time)
        try:
            assert self.class_res>=cost_time
        except:
            print('Too much class cost!!!')
            print('Last Time Res: {}, This time cost: {}'.format(self.class_res, cost_time))
            exit()

        self.class_learned_dates[cost_time].append(date_str)
        self.class_res -= cost_time
        self.print()

    def update_ps(self, ps_info):
        self.ps_info.append(ps_info)

class StudentAllInfo:
    def __init__(self) -> None:
        self.cur_id = 1
        self.student_dict = {} # id: StudentInfo
    
    def save_dict(self):
        save_pkl(filename='Student_All_Info.pkl', dic=self.student_dict)

    def load_dict(self):
        self.student_dict = load_pkl(filename='Student_All_Info.pkl')
    
    def check_exist(self, personal):
        related = self.show_related(personal)
        return related
        # TODO

    def show_related(self, personal):
        assert type(personal)==StudentInfo
        related = []
        name = personal.name
        phone = personal.phone
        allNone =  (name is None) and (phone is None)
        assert allNone is False
        for id in self.student_dict.keys():
            info = self.student_dict[id]
            if name is not None and info['name'] == name:
                related.append(info)
            if phone is not None and info['phone'] == phone:
                related.append(info)

        return related

    def update_info(self, personal):
        assert type(personal)==StudentInfo
        self.student_dict[self.cur_id] = personal #vars(personal)
        self.cur_id += 1

    def modify_info(self, personal, id):
        assert type(personal)==StudentInfo
        self.student_dict[id] = personal

class LessonInfo:
    '''
    lessontime='1900_0101_0000', cost_type=1,
    studentnum=0, teacher='yiyi', assist=None
    '''
    def __init__(self, 
        lessontime='1900_0101_0000', cost_time=1):

        ck.date_info(lessontime)
        self.lessontime = lessontime
        self.cost_time = cost_time

        self.student_list = [] # idlist
        self.teacher = 0 # idlist
        self.assist = 0 # idlist

    def load_detail(self,
        students=[], teacher=0, assist=0):
        self.student_list = students
        self.teacher = teacher
        self.assist = assist

class LessonAllInfo:
    def __init__(self):
        self.lesson_all = {}
        self.lesson_all[1900]={}
        self.lesson_all[1900][1]={}
        self.lesson_all[1900][1][1]={}
    
    def save_dict(self):
        save_pkl(filename='Lesson_All_Info.pkl', dic=self.lesson_all)

    def load_dict(self):
        self.lesson_all = load_pkl(filename='Lesson_All_Info.pkl')
    
    def update_info(self, lessoninfo):
        assert type(lessoninfo)==LessonInfo
        lessontime = lessoninfo.lessontime
        year, month, day, hm = get_time(lessontime)
        if year not in self.lesson_all.keys():
            self.lesson_all[year] = {}
        if month not in self.lesson_all[year].keys():
            self.lesson_all[year][month] = {}
        if day not in self.lesson_all[year][month].keys():
            self.lesson_all[year][month][day] = {}
        self.lesson_all[year][month][day][hm] = lessoninfo
    
    def update_student_from_lesson(self, lessoninfo, studentall):
        for name in lessoninfo.student_list:
            assert name in studentall.keys()
            sinfo = studentall[name]
            assert type(sinfo)==StudentInfo
            sinfo.update_learned(lessoninfo.lessontime, lessoninfo.cost_time)

    def update_teacher_from_lesson(self, lessoninfo, teacherall):
        for name in lessoninfo.student_list:
            assert name in teacherall.keys()
            tinfo = teacherall[name]
            assert type(tinfo)==TeacherInfo
            tinfo.update_learned(lessoninfo.lessontime, lessoninfo.cost_time)




def main():
    a = StudentInfo('haha')
    print(type(a))
    print(vars(a))
if __name__ == '__main__':
    main()