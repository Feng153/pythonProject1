import cv2
import numpy as np
from PyQt5.QtChart import QChart, QChartView, QSplineSeries, QValueAxis
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QPointF, Qt, QTimer
from PyQt5.QtGui import QPainter
import sys
import random

from utils.measurement_util import MeasurementUtils


class Charts(QChart):
    def __init__(self):
        super().__init__()
        self.chart_init()
        self.i = 0
        self.time_init()

    def time_init(self):
        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.update_series1)

    def chart_init(self):
        # 创建折线视图
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        # self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)
        # 曲线
        self.series_1 = QSplineSeries()
        self.series_1.setName("line1")  # 设置曲线名称
        self.series_2 = QSplineSeries()
        self.series_2.setName("line2")
        x2_val = [0, 1, 2, 3, 4, 5, 6, 7]
        y2_val = [0, 2, 6, 1, 7, 5, 4, 3]
        for value in range(len(x2_val)):
            self.series_2.append(x2_val[value], y2_val[value])
        # 坐标轴
        self.x_Aix = QValueAxis()
        self.x_Aix.setRange(0.00, 10.00)
        self.x_Aix.setLabelFormat("%u")  # %0.2f
        self.x_Aix.setTickCount(11)  # 10+1
        self.x_Aix.setMinorTickCount(9)
        self.x_Aix.setTitleText("T")
        self.y_Aix = QValueAxis()
        self.y_Aix.setRange(0.00, 10.00)
        self.y_Aix.setLabelFormat("%u")
        self.y_Aix.setTickCount(11)
        self.y_Aix.setMinorTickCount(1)
        self.y_Aix.setTitleText("y")

        # 画坐标轴
        self.chart.addAxis(self.x_Aix, Qt.AlignBottom)
        self.chart.addAxis(self.y_Aix, Qt.AlignLeft)
        # 画xian
        self.chart.addSeries(self.series_1)
        self.chart.addSeries(self.series_2)
        # 把曲线关联到坐标轴
        self.series_1.attachAxis(self.x_Aix)
        self.series_1.attachAxis(self.y_Aix)
        self.series_2.attachAxis(self.x_Aix)
        self.series_2.attachAxis(self.y_Aix)

        # 创建折线视图 窗口
        self.chartview = QChartView(self.chart)
        self.chart.setTitle("简单折线图")
        self.chartview.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.chartview.setGeometry(0, 0, 600, 600)
        # self.chartview.chart().addSeries(self.series_1)
        # self.chartview.chart().setAxisX(self.x_Aix)
        # self.chartview.chart().setAxisY(self.y_Aix)
        # self.chartview.chart().createDefaultAxes()
        # # self.chartview.chart().setTitleBrush(QBrush())
        # self.chartview.chart().setTitle("Title")
        # self.chartview.series_1
        self.chartview.show()

    def update_series1(self):
        data = self.a
        self.i += 1
        # 当时间轴大于现有时间轴，进行更新坐标轴，并删除之前数据
        if self.i >= 10:
            self.chart.axisX().setRange(self.i - 10, self.i)
        if self.series_1.count() > 10:
            self.series_1.removePoints(0, self.series_1.count() - 10)
        self.series_1.append(self.i, data)

    def set_num(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        depth_frame = frames.get_depth_frame()
        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        measurement_util = MeasurementUtils()
        self.r1, self.a, self.b = measurement_util.corner_detection(color_image, depth_frame, depth_intrin)
        self.r2 = measurement_util.hough_detection(color_image, depth_frame, depth_intrin)
        depth_pixel = [740, 360]
        self.dis, camera_coordinate = measurement_util.get_3d_camera_coordinate(depth_pixel, depth_frame, depth_intrin)


# if __name__ == "__main__":
#     # app = QApplication(sys.argv)
#     # charts = Charts()
#
#     # v_box = QVBoxLayout()
#     # v_box.addWidget(charts.chartview)
#     # mw  = QMainWindow()
#     # mw.setLayout(v_box)
#     # mw.show()
#
#     # sys.exit(app.exec())
