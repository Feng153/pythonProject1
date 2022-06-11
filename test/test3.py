import cv2
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from skimage.exposure import exposure


class SliderDemo(QWidget):
    def __init__(self, parent=None):
        super(SliderDemo, self).__init__(parent)
        # 设置标题与初始大小
        self.setWindowTitle('QSlider例子')
        self.resize(300, 100)

        # 垂直布局
        layout = QVBoxLayout()

        # 创建标签，居中
        self.l1 = QLabel('Hello PyQt5')
        self.l1.setAlignment(Qt.AlignCenter)
        self.img = cv2.imread('../img/img-general-2022-06-09_01-00-37.jpg')
        showImage_rgb = QImage(self.img.data, self.img.shape[1],
                               self.img.shape[0],
                               QImage.Format_RGB888)
        self.l1.setPixmap(QPixmap.fromImage(showImage_rgb))
        layout.addWidget(self.l1)
        # 创建水平方向滑动条
        self.s1 = QSlider(Qt.Horizontal)
        ##设置最小值
        self.s1.setMinimum(1)
        # 设置最大值
        self.s1.setMaximum(10)
        # 步长
        self.s1.setSingleStep(1)
        # 设置当前值
        self.s1.setValue(10)
        # 刻度位置，刻度下方
        self.s1.setTickPosition(QSlider.TicksBelow)
        # 设置刻度间距
        self.s1.setTickInterval(1)
        layout.addWidget(self.s1)
        # 设置连接信号槽函数
        self.s1.valueChanged.connect(self.valuechange)

        self.setLayout(layout)

    def valuechange(self):
        # 输出当前地刻度值，利用刻度值来调节字体大小
        print('current slider value=%s' % self.s1.value())
        gamma = self.s1.value() / 10
        img = self.img
        img2 = exposure.adjust_gamma(img, gamma)
        showImage_rgb = QImage(img2.data, img2.shape[1],
                               img2.shape[0],
                               QImage.Format_RGB888)
        self.l1.clear()
        self.l1.setPixmap(QPixmap.fromImage(showImage_rgb))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SliderDemo()
    demo.show()
    sys.exit(app.exec_())
