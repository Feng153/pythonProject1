import datetime

import time

import sys

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QSlider
from skimage import exposure

import pyrealsense2 as rs
from datetime import datetime

from controller.dis_win import DisWin
from utils.measurement_util import MeasurementUtils
from utils.feature_util import FeatureUtils
from view.measurement import Ui_MainWindow

gamma = 1
beta = 1


class MeasureMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MeasureMainWindow, self).__init__()
        self.k = 0
        self.j = 0
        self.i = 0
        self.series_1 = None
        self.chart_a = None
        self.a = 0
        self.dis = 0
        self.r1 = 0
        self.r2 = 0
        self.rgb_img = None
        self.showImage_depth = None
        self.showImage_rgb = None
        self.saveImage = None

        self.setupUi(self)
        # 相机初始化
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)  # 配置depth流
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)  # 配置color流
        self.pipeline.start(self.config)
        # 彩色图像计时器
        self.timer_camera_RGB = QTimer()
        self.timer_camera_RGB.timeout.connect(self.show_rgb)
        self.getCamPushButton1.clicked.connect(lambda: self.openCameraRGB())
        # 深度图像计时器
        self.timer_camera_Depth = QTimer()
        self.timer_camera_Depth.timeout.connect(self.show_depth)
        self.getCamPushButton2.clicked.connect(lambda: self.openCameraDepth())
        # 关闭画面
        self.closePushButton1.clicked.connect(lambda: self.closeCameraRGB())
        self.closePushButton2.clicked.connect(lambda: self.closeCameraDepth())
        # 保存画面
        self.savePushButton1.clicked.connect(lambda: self.savePictureRGB())
        self.savePushButton2.clicked.connect(lambda: self.savePictureDepth())
        # Canny边缘检测
        self.timer_camera_Canny = QTimer()
        self.timer_camera_Canny.timeout.connect(self.canny_edge)
        self.cannyRadioButton.toggled.connect(lambda: self.canny_edge_check())
        # Sobel边缘检测
        self.timer_camera_Sobel = QTimer()
        self.timer_camera_Sobel.timeout.connect(self.sobel_edge)
        self.sobelRadioButton.toggled.connect(lambda: self.sobel_edge_check())
        # Laplacian边缘检测
        self.timer_camera_Laplacian = QTimer()
        self.timer_camera_Laplacian.timeout.connect(self.laplacian_edge)
        self.laplacianRadioButton.toggled.connect(lambda: self.laplacian_edge_check())
        # Harris角点检测
        self.timer_camera_Harris = QTimer()
        self.timer_camera_Harris.timeout.connect(self.harris_corner)
        self.harrisRadioButton.toggled.connect(lambda: self.harris_corner_check())
        # FAST角点检测
        self.timer_camera_Fast = QTimer()
        self.timer_camera_Fast.timeout.connect(self.fast_corner)
        self.fastRadioButton.toggled.connect(lambda: self.fast_corner_check())
        # Tomasi角点检测
        self.timer_camera_Tomasi = QTimer()
        self.timer_camera_Tomasi.timeout.connect(self.tomasi_corner)
        self.tomasiRadioButton.toggled.connect(lambda: self.tomasi_corner_check())
        # 尺寸信息输出
        self.timer_camera_Info = QTimer()
        self.timer_camera_Info.timeout.connect(self.show_info)
        self.DisplayButton.clicked.connect(lambda: self.openShowCamera())

        # 尺寸信息隐藏
        self.HiddenButton.clicked.connect(lambda: self.closeShowCamera())

        # 光照强度控制滑块(调亮)
        self.BrightnessHorizontalSlider.setMaximum(10)
        self.BrightnessHorizontalSlider.setMinimum(1)
        self.BrightnessHorizontalSlider.setSingleStep(1)
        self.BrightnessHorizontalSlider.setValue(1)
        self.BrightnessHorizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.BrightnessHorizontalSlider.setTickInterval(1)
        self.BrightnessHorizontalSlider.valueChanged.connect(self.change_brightness)
        # 光照强度控制滑块(调暗)
        self.BrightnessHorizontalSlider_Dark.setMaximum(5)
        self.BrightnessHorizontalSlider_Dark.setMinimum(1)
        self.BrightnessHorizontalSlider_Dark.setSingleStep(1)
        self.BrightnessHorizontalSlider_Dark.setValue(1)
        self.BrightnessHorizontalSlider_Dark.setTickPosition(QSlider.TicksBelow)
        self.BrightnessHorizontalSlider_Dark.setTickInterval(1)
        self.BrightnessHorizontalSlider_Dark.valueChanged.connect(self.change_brightness_dark)
        # 监控界面
        self.timer_dis = QTimer()
        self.timer_r1 = QTimer()
        self.timer_r2 = QTimer()
        self.timer_dis.timeout.connect(self.dis_monitor)
        self.timer_r1.timeout.connect(self.r1_monitor)
        self.timer_r2.timeout.connect(self.r2_monitor)
        self.MonitorPushButton_3.clicked.connect(lambda: self.show_diswin())
        self.MonitorPushButton_4.clicked.connect(lambda: self.show_r1win())
        self.MonitorPushButton_5.clicked.connect(lambda: self.show_r2win())

    def r2_monitor(self):
        data = self.r2
        self.k += 1
        # 当时间轴大于现有时间轴，进行更新坐标轴，并删除之前数据
        if self.k >= 10:
            self.ui_r2.chart.axisX().setRange(self.k - 10, self.k)
        if self.ui_r2.series_1.count() > 10:
            self.ui_r2.series_1.removePoints(0, self.ui_r2.series_1.count() - 10)
        self.ui_r2.series_1.append(self.k, data)

    def r1_monitor(self):
        data = self.r1
        self.j += 1
        # 当时间轴大于现有时间轴，进行更新坐标轴，并删除之前数据
        if self.j >= 10:
            self.ui_r1.chart.axisX().setRange(self.j - 10, self.j)
        if self.ui_r1.series_1.count() > 10:
            self.ui_r1.series_1.removePoints(0, self.ui_r1.series_1.count() - 10)
        self.ui_r1.series_1.append(self.j, data)

    def dis_monitor(self):
        data = self.a
        self.i += 1
        # 当时间轴大于现有时间轴，进行更新坐标轴，并删除之前数据
        if self.i >= 10:
            self.ui_dis.chart.axisX().setRange(self.i - 10, self.i)
        if self.ui_dis.series_1.count() > 10:
            self.ui_dis.series_1.removePoints(0, self.ui_dis.series_1.count() - 10)
        self.ui_dis.series_1.append(self.i, data)

    def show_diswin(self):
        self.dis_win = QMainWindow()
        self.ui_dis = DisWin()
        self.ui_dis.setupUi(self.dis_win)
        self.timer_dis.start()
        self.dis_win.show()

    def show_r1win(self):
        self.r1_win = QMainWindow()
        self.ui_r1 = DisWin()
        self.ui_r1.setupUi(self.r1_win)
        self.timer_r1.start()
        self.r1_win.show()

    def show_r2win(self):
        self.r2_win = QMainWindow()
        self.ui_r2 = DisWin()
        self.ui_r2.setupUi(self.r2_win)
        self.timer_r2.start()
        self.r2_win.show()

    def change_brightness(self):
        global gamma
        gamma = (10 - self.BrightnessHorizontalSlider.value() + 1) / 10

    def change_brightness_dark(self):
        global beta
        beta = self.BrightnessHorizontalSlider_Dark.value()

    def closeShowCamera(self):
        self.timer_camera_Info.stop()
        self.RGB_Video.clear()
        self.timer_camera_RGB.start()
        self.lengthLineEdit.clear()
        self.widLineEdit.clear()
        self.heightLineEdit.clear()
        self.innnerRadiusLineEdit.clear()
        self.outerRadiusLineEdit.clear()

    def openShowCamera(self):
        self.close_all_timer()
        self.timer_camera_Info.start()

    def show_info(self):
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

        resize_color_image = cv2.resize(color_image, (740, 360))

        self.lengthLineEdit.setText(str(format(self.a, '.2f')))
        self.widLineEdit.setText(str(format(self.b, '.2f')))
        self.heightLineEdit.setText(str(format((self.dis * 100), '.2f')))
        self.innnerRadiusLineEdit.setText(str(format(self.r2 * 10, '.2f')))
        self.outerRadiusLineEdit.setText(str(format(self.r1, '.2f')))
        cv2.circle(resize_color_image, (185, 90), 3, [255, 0, 0], thickness=-1)

        self.showImage_rgb = QImage(resize_color_image.data, resize_color_image.shape[1],
                                    resize_color_image.shape[0],
                                    QImage.Format_RGB888)
        self.RGB_Video.resize(self.showImage_rgb.size())
        self.RGB_Video.setPixmap(QPixmap.fromImage(self.showImage_rgb))

    def close_all_timer(self):
        self.timer_camera_Laplacian.stop()
        self.timer_camera_Sobel.stop()
        self.timer_camera_Canny.stop()
        self.timer_camera_RGB.stop()
        self.timer_camera_Harris.stop()
        self.timer_camera_Fast.stop()
        self.timer_camera_Tomasi.stop()
        # self.timer_camera_Info.stop()
        self.RGB_Video.clear()

    def harris_corner(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        show_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.rgb_img = cv2.resize(show_rgb, (740, 360))
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, gamma)
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, beta)
        utils = FeatureUtils()
        harris_corner = utils.harris(self.rgb_img)
        self.showImage_rgb = QImage(harris_corner.data, harris_corner.shape[1],
                                    harris_corner.shape[0],
                                    QImage.Format_RGB888)
        self.RGB_Video.resize(self.showImage_rgb.size())
        self.RGB_Video.setPixmap(QPixmap.fromImage(self.showImage_rgb))
        img = cv2.cvtColor(harris_corner, cv2.COLOR_BGR2RGB)
        self.saveImage = img

    def harris_corner_check(self):
        self.close_all_timer()
        if self.harrisRadioButton.isChecked():
            self.timer_camera_Harris.start()
        else:
            self.timer_camera_Harris.stop()

    def fast_corner(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        show_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.rgb_img = cv2.resize(show_rgb, (740, 360))
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, gamma)
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, beta)
        utils = FeatureUtils()
        fast_corner = utils.fast(self.rgb_img)
        self.showImage_rgb = QImage(fast_corner.data, fast_corner.shape[1],
                                    fast_corner.shape[0],
                                    QImage.Format_RGB888)
        self.RGB_Video.resize(self.showImage_rgb.size())
        self.RGB_Video.setPixmap(QPixmap.fromImage(self.showImage_rgb))
        img = cv2.cvtColor(fast_corner, cv2.COLOR_BGR2RGB)
        self.saveImage = img

    def fast_corner_check(self):
        self.close_all_timer()
        if self.fastRadioButton.isChecked():
            self.timer_camera_Fast.start()
        else:
            self.timer_camera_Fast.stop()

    def tomasi_corner(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        show_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.rgb_img = cv2.resize(show_rgb, (740, 360))
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, gamma)
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, beta)
        utils = FeatureUtils()
        tomasi_corner = utils.tomasi(self.rgb_img)
        self.showImage_rgb = QImage(tomasi_corner.data, tomasi_corner.shape[1],
                                    tomasi_corner.shape[0],
                                    QImage.Format_RGB888)
        self.RGB_Video.resize(self.showImage_rgb.size())
        self.RGB_Video.setPixmap(QPixmap.fromImage(self.showImage_rgb))
        img = cv2.cvtColor(tomasi_corner, cv2.COLOR_BGR2RGB)
        self.saveImage = img

    def tomasi_corner_check(self):
        self.close_all_timer()
        if self.tomasiRadioButton.isChecked():
            self.timer_camera_Tomasi.start()
        else:
            self.timer_camera_Tomasi.stop()

    def laplacian_edge(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        show_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.rgb_img = cv2.resize(show_rgb, (740, 360))
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, gamma)
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, beta)
        utils = FeatureUtils()
        edge_laplacian = utils.laplacian(self.rgb_img)
        self.showImage_rgb = QImage(edge_laplacian.data, edge_laplacian.shape[1], edge_laplacian.shape[0],
                                    QImage.Format_RGB888)
        self.RGB_Video.resize(self.showImage_rgb.size())
        self.RGB_Video.setPixmap(QPixmap.fromImage(self.showImage_rgb))
        self.saveImage = edge_laplacian

    def laplacian_edge_check(self):
        self.close_all_timer()
        if self.laplacianRadioButton.isChecked():
            self.timer_camera_Laplacian.start()
        else:
            self.timer_camera_Laplacian.stop()

    def sobel_edge(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        show_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.rgb_img = cv2.resize(show_rgb, (740, 360))
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, gamma)
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, beta)
        utils = FeatureUtils()
        edge_sobel = utils.sobel(self.rgb_img)
        self.showImage_rgb = QImage(edge_sobel.data, edge_sobel.shape[1], edge_sobel.shape[0],
                                    QImage.Format_RGB888)
        self.RGB_Video.resize(self.showImage_rgb.size())
        self.RGB_Video.setPixmap(QPixmap.fromImage(self.showImage_rgb))
        self.saveImage = edge_sobel

    def sobel_edge_check(self):
        self.close_all_timer()
        if self.sobelRadioButton.isChecked():
            self.timer_camera_Sobel.start()
        else:
            self.timer_camera_Sobel.stop()

    def canny_edge(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        show_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.rgb_img = cv2.resize(show_rgb, (740, 360))
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, gamma)
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, beta)
        utils = FeatureUtils()
        edge_canny = utils.canny(self.rgb_img)
        self.showImage_rgb = QImage(edge_canny.data, edge_canny.shape[1], edge_canny.shape[0],
                                    QImage.Format_RGB888)
        self.RGB_Video.resize(self.showImage_rgb.size())
        self.RGB_Video.setPixmap(QPixmap.fromImage(self.showImage_rgb))
        self.saveImage = edge_canny

    def canny_edge_check(self):
        self.close_all_timer()
        if self.cannyRadioButton.isChecked():
            self.timer_camera_Canny.start()
        else:
            self.timer_camera_Canny.stop()

    def savePictureRGB(self):
        time = datetime.now()
        time = time.strftime('%Y-%m-%d_%H-%M-%S')
        img = self.saveImage
        path = '../img/img-general-' + str(time) + '.jpg'
        cv2.imwrite(path, img)
        self.LogtextBrowser.append('保存成功: ' + path)

    def savePictureDepth(self):
        time = datetime.now()
        time = time.strftime('%Y-%m-%d_%H-%M-%S')
        img = self.saveImage
        path = '../img/img-depth-' + str(time) + '.jpg'
        cv2.imwrite(path, img)
        self.LogtextBrowser.append('保存成功: ' + path)

    def closeCameraRGB(self):
        self.close_all_timer()
        self.RGB_Video.clear()

    def closeCameraDepth(self):
        self.timer_camera_Depth.stop()
        self.Depth_Video.clear()

    def openCameraDepth(self):
        self.timer_camera_Depth.start(30)

    def show_depth(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        colorizer = rs.colorizer()
        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(depth_frame)
        colorized_depth = np.asanyarray(colorizer.colorize(filled_depth).get_data())
        self.depth_img = cv2.resize(colorized_depth, (740, 360))
        self.showImage_depth = QImage(self.depth_img.data, self.depth_img.shape[1], self.depth_img.shape[0],
                                      QImage.Format_RGB888)
        self.Depth_Video.resize(self.showImage_depth.size())
        self.Depth_Video.setPixmap(QPixmap.fromImage(self.showImage_depth))
        self.saveImage = self.depth_img

    def openCameraRGB(self):
        self.timer_camera_RGB.start(30)

    def show_rgb(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        show_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.rgb_img = cv2.resize(show_rgb, (740, 360))
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, gamma)
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, beta)
        self.showImage_rgb = QImage(self.rgb_img.data, self.rgb_img.shape[1],
                                    self.rgb_img.shape[0],
                                    QImage.Format_RGB888)
        self.RGB_Video.resize(self.showImage_rgb.size())
        self.RGB_Video.setPixmap(QPixmap.fromImage(self.showImage_rgb))
        img = cv2.cvtColor(self.rgb_img, cv2.COLOR_BGR2RGB)
        self.saveImage = img


if __name__ == '__main__':
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MeasureMainWindow()
    File = open("../qss/Adaptic.qss", 'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)
    window.show()
    sys.exit(app.exec_())
