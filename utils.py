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