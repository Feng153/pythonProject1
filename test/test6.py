# coding:utf-8
import time
import sys
import random

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
import random

new_data = []
mutex = QMutex()


class DataThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            data = random.randint(0, 10)
            mutex.lock()
            new_data.append(data)
            mutex.unlock()
            time.sleep(0.2)


class Main_window(QWidget):
    def __init__(self):
        super(Main_window, self).__init__()
        # 开启获取新数据的子线程
        self.threadCtl = DataThread()
        self.threadCtl.start()
        # 定时更新折线图
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(200)

        self.init_line()
        self.add_axis()

    def init_line(self):
        # 实例折线对象
        self.series_1 = QLineSeries()  # 定义LineSerise，将类QLineSeries实例化
        # 折线初始数据列表
        self._1_point_list = []
        for i in range(10):
            y = random.randint(0, 10)
            self._1_point_list.append(QPointF(i, y))

        self.series_1.append(self._1_point_list)  # 折线添加坐标点清单
        self.series_1.setName("折线名称")


    def add_axis(self):
        # 设置x轴
        self.x_Aix = QValueAxis()
        self.x_Aix.setRange(0.00, 10.00)
        self.x_Aix.setLabelFormat("%0.2f")
        self.x_Aix.setTickCount(11)  # 将0-10分成11份
        self.x_Aix.setMinorTickCount(4)  # 设置每一份的分割数

        # 设置y轴
        self.y_Aix = QValueAxis()
        self.y_Aix.setTitleText("轴代表的意义名称")
        self.y_Aix.setRange(0.00, 10.00)
        self.y_Aix.setLabelFormat("%0.2f")
        self.y_Aix.setTickCount(11)
        self.y_Aix.setMinorTickCount(4)

        self.charView = QChartView(self)  # 定义charView，父窗体类型为 Window

        self.charView.setGeometry(140, 20,
                                  self.width(),
                                  self.height())  # 设置charView位置、大小

        self.charView.chart().addSeries(self.series_1)  # 添加折线实例

        # 添加轴，Qt.AlignBottom表示底部，Qt.AlignLeft表示左边，Qt.AlignRight表示右边
        self.charView.chart().addAxis(self.x_Aix, Qt.AlignBottom)
        self.charView.chart().addAxis(self.y_Aix, Qt.AlignLeft)

        # 将折线与对应的y轴关联，这里只写了一个y轴，如果有多条折线可以关联不同的y轴
        self.series_1.attachAxis(self.y_Aix)

        # 隐藏或者显示折线 setVisible
        # self.series_1.setVisible(False)  # 隐藏折线

    def update(self):
        # 更新折线上的点的坐标
        if len(new_data) > 0:
            mutex.lock()
            self.value = new_data[0]
            new_data.pop(0)
            mutex.unlock()
            del self._1_point_list[len(self._1_point_list) - 1]
            self._1_point_list.insert(0, QPointF(0, self.value))
            for i in range(0, len(self._1_point_list)):
                self._1_point_list[i].setX(i)
            self.series_1.replace(self._1_point_list)


if __name__ == "__main__":
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    pw = Main_window()
    pw.show()
    sys.exit(app.exec_())
