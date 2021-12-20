
import sys
from colorbeat import ColorBeat
from DataMap import DataMap, YearMap
from BaseInfo import SellInfo

#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5 import QtCore, QtWidgets
# from PyQt5.QtWidgets import QDialogButtonBox, QDateTimeEdit,QDialog,QComboBox,QTableView,QAbstractItemView,QHeaderView,QTableWidget, QTableWidgetItem, QMessageBox,QListWidget,QListWidgetItem, QStatusBar,  QMenuBar,QMenu,QAction,QLineEdit,QStyle,QFormLayout,   QVBoxLayout,QWidget,QApplication ,QHBoxLayout, QPushButton,QMainWindow,QGridLayout,QLabel
# from PyQt5.QtGui import QIcon,QPixmap,QStandardItem,QStandardItemModel,QCursor,QFont,QBrush,QColor,QPainter,QMouseEvent,QImage,QTransform
# from PyQt5.QtCore import QStringListModel,QAbstractListModel,QModelIndex,QSize,Qt,QObject,pyqtSignal,QTimer,QEvent,QDateTime,QDate,QFileDialog

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_selected_video = "waiting for new video"
        self.modelarts_api = ColorBeat()

        self.initUI()
        self.threads = []

    def initUI(self):
        self.setWindowTitle('ColorBeat Data System')

        self.centralwidget = QWidget(self)

        # self.init_menubar()
        self.statusBar().showMessage(f'System Init')
        self.init_widgets()
        # grid = QGridLayout()
        self.setCentralWidget(self.centralwidget)
    
    def init_widgets(self):
        fbox = QFormLayout()

        # database loading
        hbox = QHBoxLayout()
        self.db_file_line = QLineEdit()
        self.db_file_line.setReadOnly(True)
        self.db_open_button = QPushButton('&Open')
        self.db_open_button.setText("打开数据库文件")
        self.db_open_button.clicked.connect(self.open_db_file)
        hbox.addWidget(self.db_file_line)
        hbox.addWidget(self.db_open_button)
        fbox.addRow(QLabel("数据库："), hbox)

        # function switch
        self.sell_butt = QPushButton(self)
        self.sell_butt.clicked.connect(self.open_sellui)


        btn11.clicked.connect(self.do_btn11) # 输入：整数

        self.func_options = QComboBox()
        funcs = ["销售数据录入", "查询--课程信息", "查询--学员信息", "查询--教师信息"]
        self.func_options.addItems(funcs)
        fbox.addRow(QLabel("功能选择："), self.func_options)
        self.func_options.currentIndexChanged.connect(self.funcopt_relate_hbox)

    # =====================================================================
    def open_sellui(self):
        layout = QGridLayout()

        # basic info
        firstLabel = QLabel('姓：');    layout.addWidget(firstLabel, 0, 0, 1, 1)
        firstInput = QLineEdit();        layout.addWidget(firstInput, 0, 1, 1, 1)
        nameLabel = QLabel('名：');    layout.addWidget(nameLabel, 0, 2, 1, 1)
        nameInput = QLineEdit();        layout.addWidget(nameInput, 0, 3, 1, 1)
        snameLabel = QLabel('小名：');    layout.addWidget(snameLabel, 0, 4, 1, 1)
        snameInput = QLineEdit();        layout.addWidget(snameInput, 0, 5, 1, 1)

        ageLabel = QLabel('年龄：');    layout.addWidget(ageLabel, 1, 0, 1, 1)
        ageInput = QLineEdit();        layout.addWidget(ageInput, 1, 1, 1, 1)
        gendLabel = QLabel('性别：');    layout.addWidget(gendLabel, 1, 2, 1, 1)
        gendInput = QComboBox();gendInput.addItems(['男', '女'])
        layout.addWidget(gendInput, 1, 3, 1, 1)

        phoneLabel = QLabel('电话');  layout.addWidget(phoneLabel, 2, 0, 1, 1)
        phoneInput = QLineEdit();       layout.addWidget(phoneInput, 2, 1, 1, 5)
        otherLabel = QLabel('备注'); layout.addWidget(otherLabel, 3, 0, 1, 1)
        otherInput = QLineEdit();        layout.addWidget(otherInput, 3, 1, 1, 5)

        # sell info
        '''
        课程数目：basic_num: 基础课程包; trial: 试听; gift: 赠送; referral: 转介绍; exper: 体验课
        价格计算：baseMoney: 基础价格, discount: 折扣, discountMoney: [] 抵扣(体验+团报+转介绍)
        >> income_cal = baseMoney*basic_num*discount - sum(discountMoney)
        收入统计:income_cal: 需缴费, income_done: 实缴费, income_res: 待缴费
        '''
        basicLabel = QLabel('基础课程包');  layout.addWidget(basicLabel, 4, 0, 1, 1)
        trialLabel = QLabel('试听');       layout.addWidget(trialLabel, 4, 1, 1, 1)
        giftLabel = QLabel('赠送');        layout.addWidget(giftLabel, 4, 2, 1, 1)
        referLabel = QLabel('转介绍');     layout.addWidget(referLabel, 4, 3, 1, 1)
        experLabel = QLabel('体验课');     layout.addWidget(experLabel, 4, 4, 1, 1)

        basicInput = QLineEdit();       layout.addWidget(basicInput, 5, 0, 1, 1)
        trialInput = QLineEdit();       layout.addWidget(trialInput, 5, 1, 1, 1)
        giftInput = QLineEdit();       layout.addWidget(giftInput, 5, 2, 1, 1)
        referInput = QLineEdit();       layout.addWidget(referInput, 5, 3, 1, 1)
        experInput = QLineEdit();       layout.addWidget(experInput, 5, 4, 1, 1)

        
        totalLabel = QPushButton(self, text="合计");  layout.addWidget(totalLabel, 4, 5, 1, 1)
        totalLabel.clicked.connect(self.open_sellui)
        totalInput = QLineEdit();       layout.addWidget(basicInput, 5, 5, 1, 1)


        return layout
        
    # 点击按钮的槽函数
    def click_button(self,btn):
        # 遍历右侧布局中的子部件，将其删除
        while self.right_widget_layout.count():
            child = self.right_widget_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        text = QtWidgets.QLabel("这是按钮{}的文本".format(btn)) # 创建一个文本部件
        self.right_widget_layout.addWidget(text) # 将文本部件添加到右侧布局中


    def funcopt_relate_hbox(self, i):
        hbox 

        pass

    def process(self):
        self.func_options.currentText

    def func_sell_hbox(self):
        pass
    
    def func_query_lesson_hbox(self):
        pass
    
    def func_query_stu_hbox(self):
        pass
    
    def func_query_tea_hbox(self):
        pass
    
    def xxxx(self):


        self.start_job_button = QPushButton()
        self.start_job_button.setText("执行任务")
        self.start_job_button.clicked.connect(self.process)

        # HCSO login
        self.hcso_region = QComboBox()
        self.hcso_region.addItem("武汉计算中心")

        self.hcso_ak_line = QLineEdit()
        self.hcso_sk_line = QLineEdit()
        self.hcso_project_id_line = QLineEdit()

        fbox.addRow(QLabel("局点："), self.hcso_region)
        # fbox.addRow(QLabel("AK："), self.hcso_ak_line)
        # fbox.addRow(QLabel("SK："), self.hcso_sk_line)
        # fbox.addRow(QLabel("项目ID："), self.hcso_project_id_line)

        # open video hint and label
        hbox = QHBoxLayout()
        video_path_label = QLineEdit()
        video_path_label.setReadOnly(True)
        # open video push button
        self.open_button = QPushButton('&Open')
        self.open_button.setText("打开")
        self.open_button.clicked.connect(self.open_file)
        hbox.addWidget(video_path_label)
        hbox.addWidget(self.open_button)

        self.video_label = video_path_label
        fbox.addRow(QLabel("选择视频："), hbox)

        # task option checkbox
        task_options = ["去噪", "2倍插帧", "2倍超分", "4倍超分"]
        pre_check = [True, False, False, True]
        self.task_checkbox_list = []
        hlayout = QHBoxLayout()
        for i, task in enumerate(task_options):
            task_cb = QCheckBox(task)
            task_cb.setChecked(pre_check[i])
            self.task_checkbox_list.append(task_cb)
            hlayout.addWidget(task_cb)
        fbox.addRow(QLabel("任务："), hlayout)


        hbox = QHBoxLayout()
        ncl = QLineEdit()
        ncl.setValidator(QIntValidator())
        ncl.setText('100')
        hbox.addWidget(ncl)
        hbox.addWidget(QLabel('尼特'))
        fbox.addRow(QLabel("最大亮度："), hbox)


        # codec engine
        codecs = ['x264', 'x265', 'xavc@300', 'avs2', 'avs3']
        codec_cb = QComboBox()
        codec_cb.addItems(codecs)
        fbox.addWidget(codec_cb)

        hbox = QHBoxLayout()
        bitrate = QLineEdit()
        bitrate.setValidator(QIntValidator())
        bitrate.setText('10')
        hbox.addWidget(bitrate)
        hbox.addWidget(QLabel('MB'))
        fbox.addRow(QLabel("比特率："), hbox)

        instance_choices = [str(i) for i in range(1,9)]
        self.instance_number = QComboBox()
        self.instance_number.addItems(instance_choices)
        self.instance_number.setCurrentIndex(0)
        fbox.addRow(QLabel("节点数量"), self.instance_number)

        # add process button
        self.job_id = QLineEdit()
        self.job_id.setReadOnly(True)
        fbox.addRow(QLabel("作业名："), self.job_id)

        # add download
        self.download_button = QPushButton()
        self.download_button.setText("下载文件")
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setEnabled(False)

        self.start_job_button = QPushButton()
        self.start_job_button.setText("执行任务")
        self.start_job_button.clicked.connect(self.process)

        hbox = QHBoxLayout()
        hbox.addWidget(self.start_job_button)
        hbox.addWidget(self.download_button)

        fbox.addRow(QLabel(""), hbox)

        # add icon
        pixmap = QPixmap('logo/header-logo.png')
        logo_label = QLabel()
        logo_label.setPixmap(pixmap)

        fbox.addWidget(logo_label)

        self.centralwidget.setLayout(fbox)

    def open_db_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                  "All Files (*);;PKL Files (*.pkl)",
                                                  options=options)
        if fileName:
            self.db_file_line.setText(fileName)

# query_lesson ui
class SellUI(QWidget):
    def __init__(self):
        super(SellUI, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("SellUI")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(100, 80, 181, 91))
        self.label.setText("SellUI")

# query_lesson ui
class QLessonUI(QWidget):
    def __init__(self):
        super(QLessonUI, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("QLessonUI")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(100, 80, 181, 91))
        self.label.setText("QLessonUI")

# query_stu ui
class QStuUI(QWidget):
    def __init__(self):
        super(QStuUI, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("QStuUI")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(100, 80, 181, 91))
        self.label.setText("QStuUI")

# query_tea ui
class QTeaUI(QWidget):
    def __init__(self):
        super(QTeaUI, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("QTeaUI")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(100, 80, 181, 91))
        self.label.setText("QTeaUI")

if __name__=="__main__":
    import sys
    
    app = QApplication(sys.argv)
    win = GUI()
    win.show()
    sys.exit(app.exec_())