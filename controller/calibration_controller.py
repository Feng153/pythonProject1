import sys
from datetime import datetime

import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from view.calibration import Ui_MainWindow
import pyrealsense2 as rs


class CalibrationMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(CalibrationMainWindow, self).__init__()
        self.showImage_rgb = None
        self.rgb_img = None
        self.saveImage = None
        self.setupUi(self)
        # 相机初始化
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)  # 配置depth流
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)  # 配置color流
        self.cfg = self.pipeline.start(self.config)
        # 彩色图像计时器
        self.timer_camera_RGB = QTimer()
        self.timer_camera_RGB.timeout.connect(self.show_rgb)
        self.getCam.clicked.connect(lambda: self.openCameraRGB())
        # 关闭画面
        self.closeCam.clicked.connect(lambda: self.closeCameraRGB())
        # 保存画面
        self.shoot.clicked.connect(lambda: self.savePictureRGB())
        # 标定
        self.calibration.clicked.connect(lambda: self.calibrationCam())

    def calibrationCam(self):
        profile = self.cfg.get_stream(rs.stream.depth)
        intr = profile.as_video_stream_profile().get_intrinsics()
        intr_matrix = np.asarray([
            [intr.fx, 0, intr.ppx], [0, intr.fy, intr.ppy], [0, 0, 1]
        ])
        dis = 10
        self.log.append("相机的内参矩阵：\n" + str(intr_matrix))
        self.log.append("相机的畸变系数: " + str(intr.coeffs))
        self.log.append("相机距离水平面的高度为: " + str(dis) + "cm")

    def savePictureRGB(self):
        time = datetime.now()
        time = time.strftime('%Y-%m-%d_%H-%M-%S')
        img = self.saveImage
        path = '../img/img-general-' + str(time) + '.jpg'
        cv2.imwrite(path, img)
        self.log.append('保存成功: ' + path)

    def closeCameraRGB(self):
        self.video.clear()
        self.timer_camera_RGB.stop()
        self.pipeline.stop()

    def openCameraRGB(self):
        self.timer_camera_RGB.start(30)

    def show_rgb(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        show_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        self.rgb_img = cv2.resize(show_rgb, (740, 360))
        self.showImage_rgb = QImage(self.rgb_img.data, self.rgb_img.shape[1],
                                    self.rgb_img.shape[0],
                                    QImage.Format_RGB888)
        self.video.resize(self.showImage_rgb.size())
        self.video.setPixmap(QPixmap.fromImage(self.showImage_rgb))
        img = cv2.cvtColor(self.rgb_img, cv2.COLOR_BGR2RGB)
        self.saveImage = img


if __name__ == '__main__':
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = CalibrationMainWindow()
    File = open("../qss/Adaptic.qss", 'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)
    window.show()
    sys.exit(app.exec_())
