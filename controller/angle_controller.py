import sys

import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QSlider
from skimage.exposure import exposure

from utils.measurement_util import MeasurementUtils
from view.angel import Ui_MainWindow
import pyrealsense2 as rs

gamma = 1
beta = 1


class AngleMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(AngleMainWindow, self).__init__()
        self.resize_color_image = None
        self.dis = 0
        self.r2 = 0
        self.b = 0
        self.a = 0
        self.r1 = 0
        self.showImage_rgb = None
        self.rgb_img = None
        self.setupUi(self)
        # 相机初始化
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)  # 配置depth流
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)  # 配置color流
        self.cfg = self.pipeline.start(self.config)
        # 系统内置摄像头
        self.cap = cv2.VideoCapture(2)
        # 彩色图像计时器
        self.timer_camera_RGB = QTimer()
        self.timer_camera_RGB.timeout.connect(self.show_rgb)
        self.getCam1.clicked.connect(lambda: self.openCameraRGB())
        # 关闭画面
        self.closeCam1.clicked.connect(lambda: self.closeCameraRGB())
        # 尺寸信息输出
        self.timer_camera_Info = QTimer()
        self.timer_camera_Info.timeout.connect(self.show_info)
        self.showInfo.clicked.connect(lambda: self.openShowCamera())
        # 尺寸信息隐藏
        self.hidInfo.clicked.connect(lambda: self.closeShowCamera())
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
        # 第二视角打开
        self.timer_camera_angle = QTimer()
        self.timer_camera_angle.timeout.connect(self.show_cam2)
        self.getCam2.clicked.connect(lambda: self.openCamera2())
        # 第二视角关闭
        self.closeCam2.clicked.connect(lambda: self.closeCamera2())

    def closeCamera2(self):
        self.label_2.clear()
        self.timer_camera_angle.stop()
        self.cap.release()

    def openCamera2(self):
        self.timer_camera_angle.start(30)

    def show_cam2(self):
        ret, frame = self.cap.read()
        # frame = cv2.resize(frame, (640, 480))
        # image = np.asanyarray(frame.get_data())
        show_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.rgb_img = cv2.resize(show_rgb, (740, 360))
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, gamma)
        self.rgb_img = exposure.adjust_gamma(self.rgb_img, beta)
        self.showImage_rgb = QImage(self.rgb_img.data, self.rgb_img.shape[1],
                                    self.rgb_img.shape[0],
                                    QImage.Format_RGB888)
        self.label_2.resize(self.showImage_rgb.size())
        self.label_2.setPixmap(QPixmap.fromImage(self.showImage_rgb))

    def change_brightness(self):
        global gamma
        gamma = (10 - self.BrightnessHorizontalSlider.value() + 1) / 10

    def change_brightness_dark(self):
        global beta
        beta = self.BrightnessHorizontalSlider_Dark.value()

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
        self.label.resize(self.showImage_rgb.size())
        self.label.setPixmap(QPixmap.fromImage(self.showImage_rgb))

    def openCameraRGB(self):
        self.timer_camera_RGB.start(30)

    def closeCameraRGB(self):
        self.label.clear()
        self.timer_camera_RGB.stop()
        self.timer_camera_Info.stop()
        self.lengthLineEdit.clear()
        self.widLineEdit.clear()
        self.innnerRadiusLineEdit.clear()
        self.outerRadiusLineEdit.clear()
        self.heightLineEdit.clear()

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

        self.resize_color_image = cv2.resize(color_image, (740, 360))
        self.resize_color_image = exposure.adjust_gamma(self.resize_color_image, gamma)
        self.resize_color_image = exposure.adjust_gamma(self.resize_color_image, beta)

        self.lengthLineEdit.setText(str(format(self.a, '.2f')))
        self.widLineEdit.setText(str(format(self.b, '.2f')))
        self.heightLineEdit.setText(str(format((self.dis * 100), '.2f')))
        self.innnerRadiusLineEdit.setText(str(format(self.r2 * 10, '.2f')))
        self.outerRadiusLineEdit.setText(str(format(self.r1, '.2f')))
        cv2.circle(self.resize_color_image, (185, 90), 3, [255, 0, 0], thickness=-1)

        self.showImage_rgb = QImage(self.resize_color_image.data, self.resize_color_image.shape[1],
                                    self.resize_color_image.shape[0],
                                    QImage.Format_RGB888)
        self.label.resize(self.showImage_rgb.size())
        self.label.setPixmap(QPixmap.fromImage(self.showImage_rgb))

    def openShowCamera(self):
        self.timer_camera_RGB.stop()
        self.timer_camera_Info.start()

    def closeShowCamera(self):
        self.timer_camera_Info.stop()
        self.label.clear()
        self.timer_camera_RGB.start()
        self.lengthLineEdit.clear()
        self.widLineEdit.clear()
        self.heightLineEdit.clear()
        self.innnerRadiusLineEdit.clear()
        self.outerRadiusLineEdit.clear()


if __name__ == '__main__':
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = AngleMainWindow()
    File = open("../qss/Adaptic.qss", 'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)
    window.show()
    sys.exit(app.exec_())
