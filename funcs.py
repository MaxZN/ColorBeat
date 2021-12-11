import numpy as np
import pickle
import os

import settings
from datetime import datetime
from utils import save_pkl, load_pkl

sets = settings.load_settings(settings.SETFILE)

class Check:
    def __init__(self) -> None:
        pass

    def basic(self, gender, phone):
        assert gender in [0,1]
        assert phone//(1E10) == 1
        pass
    
    def sell_info(self, cnt, class_type):
        class_set = sets['class_setting']

        assert cnt in class_set.keys()
        assert class_type in class_set[cnt].keys()
        pass

    def date_info(self, date_str):
        assert datetime.strptime(date_str, "%Y_%m%d_%H%M")

    def cost_info(self, date_str, cost_num):
        assert type(date_str)==str
        self.date_info(date_str)

        assert cost_num in sets['cost_type'] # 1,2,3
        pass

