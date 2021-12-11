
import os
import pickle
import sys
import math
from datetime import datetime

from utils import save_pkl, load_pkl

SETFILE='settings.pkl'
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
COST_TYPE=(1,2,3) # could cost how many classes each time
SELLWEIGHT={'IntroWeight': 0.01, 'coWeight': 0.01}
FEES={'assistfee': 8}

SETTINGS['class_setting'] = CLASS_TYPE
SETTINGS['cost_type'] = COST_TYPE
SETTINGS['sell_weight'] = SELLWEIGHT
SETTINGS['fees'] = FEES

def load_settings(filename=None):
    if filename is None:
        return SETTINGS
    else:
        return load_pkl(filename)

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = SETFILE
    save_pkl(filename, SETTINGS)
if __name__ == '__main__':
    main()