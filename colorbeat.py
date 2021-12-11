import numpy as np
from DataMap import DataMap, YearMap
from BaseInfo import SellInfo, StudentAllInfo, TeacherAllInfo

class ColorBeat(object):
    def __init__(self) -> None:
        super().__init__()
        self.data_lesson = None
        self.data_stu = None
        self.data_tea = None
    
    def loading_database(self, data_stu, data_tea, data_lesson):
        assert type(data_stu) == StudentAllInfo
        assert type(data_tea) == TeacherAllInfo
        assert type(data_lesson) == YearMap
        self.data_stu = data_stu
        self.data_tea = data_tea
        self.data_lesson = data_lesson
    
    def update_sellinfo(self):
        pass
    
    def update_lessoninfo(self):
        pass

    def sign_up(self, InfoDict):
        pass

    def query(self, name):
        pass


def main():
    colorbeat = ColorBeat()

    data_stu = StudentAllInfo()
    data_tea = TeacherAllInfo()
    data_lesson = YearMap()

    data_stu.load_dict()
    data_tea.load_dict()
    data_lesson.load_dict()

    colorbeat.loading_database(data_stu, data_tea, data_lesson)

    new_sell = SellInfo()

if __name__ == '__main__':
    main()