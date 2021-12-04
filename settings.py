
import os
import pickle
import sys
from datetime import datetime

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

def load_settings():
    try:
        with open('settings.pkl', 'rb') as f:
            set = pickle.load(f)
    except:
        set = SETTINGS
    return set

def main():
    filename = sys.argv[1]
    d = datetime.now()
    curtime = d.strftime('%m%d_%H%M%S')
    oldname = '{}.bk.{}'.format(filename, curtime)
    if os.path.exists(filename):
        os.rename(filename, oldname)

    with open(filename, 'wb') as fo:
        pickle.dump(SETTINGS, fo)
        fo.close()

if __name__ == '__main__':
    main()