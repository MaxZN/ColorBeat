import numpy as np
import settings
from datetime import datetime

set = settings.load_settings()
class_set = set['class_setting']

class Check:
    def __init__(self) -> None:
        pass

    def basic(self, gender, phone):
        assert gender in [0,1]
        assert phone//(1E10) == 1
        pass
    
    def sell_info(self, cnt, class_type):
        assert cnt in class_set.keys()
        assert class_type in class_set[cnt].keys()
        pass

    def cost_info(self, date_str, cost_num):
        assert type(date_str)==str
        assert datetime.strptime(date_str, "%Y_%m%d_%H%M")

        assert cost_num in set['cost_type'] # 1,2,3
        pass

