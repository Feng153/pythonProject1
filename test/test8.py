import sqlite3, sys, time
from datetime import datetime
from PyQt5.QtChart import QDateTimeAxis, QValueAxis, QSplineSeries, QChart, QChartView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QDateTime, Qt, QTimer


class ChartView(QChartView, QChart):  # 原代码如此，继承了两个类，其实去掉QChart也没影响
    def __init__(self, *args, **kwargs):
        super(ChartView, self).__init__(*args, **kwargs)
        self.connect = sqlite3.connect(
            "netdata.db")  # 数据库，表名为t1，包括时间（年月日时分秒的方式，用sqlite的自动时间截生成的，为方便自己看，转成年月日，结果是个坑），下载速度，上传速度
        self.resize(1500, 500)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿，注释此行曲线很难看
        self.limitminute = 240  # 设置显示多少分钟内的活动
        self.maxspeed = 300  # 预设y轴最大值
        self.chart_init()
        self.timer_init()

    def timer_init(self):
        # 使用QTimer，2秒触发一次，更新数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.drawLine)
        self.timer.start(2000)

    def chart_init(self):
        self.chart = QChart()
        self.series = QSplineSeries()  # 这个是平滑曲线类，而QSplineSeries()是折线类，根所自己需求选用，下载数据曲线
        self.series_upload = QSplineSeries()  # 上传数据曲线
        # 设置曲线名称
        self.series.setName("下载速度")
        self.series_upload.setName('上传速度')
        # 把曲线添加到QChart的实例中
        self.chart.addSeries(self.series)
        self.chart.addSeries(self.series_upload)
        # 声明并初始化X轴，Y轴
        self.dtaxisX = QDateTimeAxis()
        self.vlaxisY = QValueAxis()
        # 设置坐标轴显示范围
        self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-self.limitminute * 60))
        self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
        self.vlaxisY.setMin(0)
        self.vlaxisY.setMax(self.maxspeed)  # 设置y轴最大值

        # 设置X轴时间样式
        self.dtaxisX.setFormat("hh:mm")  # 关注就是几小时内的数据，就留时分好了

        # 设置坐标轴上的格点
        self.dtaxisX.setTickCount(15)  # 平均分的刻度分隔
        self.vlaxisY.setTickCount(10)
        # 设置坐标轴名称
        self.dtaxisX.setTitleText("时间")
        self.vlaxisY.setTitleText("速度(M)")
        # 设置网格显示，并设为灰色
        self.vlaxisY.setGridLineVisible(True)
        self.vlaxisY.setGridLineColor(Qt.gray)
        self.dtaxisX.setGridLineVisible(True)
        self.dtaxisX.setGridLineColor(Qt.gray)
        # 把坐标轴添加到chart中
        self.chart.addAxis(self.dtaxisX, Qt.AlignBottom)
        self.chart.addAxis(self.vlaxisY, Qt.AlignLeft)
        # 把曲线关联到坐标轴
        self.series.attachAxis(self.dtaxisX)
        self.series.attachAxis(self.vlaxisY)

        self.series_upload.attachAxis(self.dtaxisX)
        self.series_upload.attachAxis(self.vlaxisY)

        self.setChart(self.chart)

    def drawLine(self):
        # 获取当前时间
        bjtime = QDateTime.currentDateTime()
        # 更新X轴坐标
        self.dtaxisX.setMin(bjtime.addSecs(-self.limitminute * 60))
        self.dtaxisX.setMax(bjtime.addSecs(0))

        # 设Y轴最大值，查询数据库最近4小时内的下载最大值，并乘1.2作为y轴最大值
        for xx in self.connect.execute(
                "select max(downdata) from t1 where time > datetime('now','-4 hour','localtime') order by time"):
            if xx:
                self.vlaxisY.setMax(int(xx[0] * 1.2))
            else:
                self.vlaxisY.setMax(self.maxspeed)

        if self.series.at(
                0):  # self.serie存在索引0时，也就是起码有一个数据对过旧数据进行清除，self.series.removePoints两参数一个是索引，一个是从索引起始删除多少个数值，两条数据均如此处理
            if self.series.at(0).x() < bjtime.addSecs(
                    -self.limitminute * 60).toMSecsSinceEpoch():  # self.series.at(0).x()其实就是图像x坐标值，与原始数据可能并不完全相等，小数点后的值是约去了的，bjtime的toMSecsSinceEpoch()其实与time.time()相约，不过前者是整数，是后者的1000倍，所以后面需要转换
                self.series.removePoints(0, 1)

        if self.series_upload.at(0):
            if self.series_upload.at(0).x() < bjtime.addSecs(-self.limitminute * 60).toMSecsSinceEpoch():
                self.series_upload.removePoints(0, 1)

        for xx in self.connect.execute("select * from t1 order by time desc limit 1"):
            # x1 = self.connect.execute("select strftime('%s',?)", (xx[0],)).fetchone()[0] #用此法转出来的时间截与time.time()整好差8个时区，用sqlite不知如何处理了
            x1 = time.mktime(datetime.strptime(xx[0], '%Y-%m-%d %H:%M:%S').timetuple())  # 用py内置库的办法有日期转为时间截
            x_time = int(x1) * 1000  # 再乘1000，以符号格式要求
            y0_value = xx[1]  # 取得下载数据
            y1_value = xx[2]  # 取得上传数据

            # 添加数据到曲线末端
            if self.series.at(0):  # 因数据库并非每秒更新，为免相同数据重复录入，先判断self.series起码有一个数据
                if x_time != self.series.at(self.series.count() - 1).x():  # 假如最新的时间轴与数据库取得的不一致就录入，相同就跳过
                    self.series.append(x_time, y0_value)
            else:  # 当self.series为空时起码录入第一个数据，下面另外一轴同样处理
                self.series.append(x_time, y0_value)

            if self.series_upload.at(0):
                if x_time != self.series_upload.at(self.series_upload.count() - 1).x():
                    self.series_upload.append(x_time, y1_value)
            else:
                self.series_upload.append(x_time, y1_value)
            # print(self.series.count(),self.series_upload.count())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = ChartView()
    view.show()
    sys.exit(app.exec_())
