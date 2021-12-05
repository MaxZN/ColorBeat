
import os
import pickle
import sys
import math
from datetime import datetime

from utils import save_pkl, load_pkl, get

SETTINGS ={}

CLASS_TYPE = {}
CLASS_TYPE_0 = {
    'name': '体验课',
    0: '每周1节',
    1: '每周2节',
}
CLASS_TYPE_1 = {
    'name': '正式课 每周 1 节',
    0: '指定课时',
    1: '全年 94节',
    2: '暑期+寒假 30节',
    3: '秋季+寒假 42节',
    4: '暑期+秋季 52节',
}
CLASS_TYPE_2 = {
    'name': '正式课 每周 2 节',
    0: '指定课时',
    1: '全年 45节',
    2: '秋季 16节',
    3: '秋季+寒假 19节',
}

CLASS_TYPE = {0:CLASS_TYPE_0, 1:CLASS_TYPE_1, 2:CLASS_TYPE_2}
SETTINGS['class_setting'] = CLASS_TYPE

COST_TYPE=(1,2,3) # could cost how many classes each time
SETTINGS['cost_type'] = COST_TYPE

SELLWEIGHT={
    'IntroWeight': 0.01, 'coWeight': 0.01, 
}
SETTINGS['sell_weight'] = SELLWEIGHT

FEES={
    'assistfee': 8
}
SETTINGS['fees'] = FEES

def load_settings(filename=None):
    if filename is None:
        return SETTINGS
    else:
        return load_pkl(filename)

def main():
    filename = sys.argv[1]
    save_pkl(filename, SETTINGS)
if __name__ == '__main__':
    main()