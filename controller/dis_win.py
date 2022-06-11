from PyQt5 import QtWidgets, QtCore
from PyQt5.QtChart import QChart, QSplineSeries, QValueAxis, QChartView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMainWindow


class DisWin(QMainWindow):
    def setupUi(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 20, 600, 600))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setBackgroundVisible(False)
        self.series_1 = QSplineSeries()
        self.x_Aix = QValueAxis()
        self.x_Aix.setRange(0.00, 10.00)
        self.x_Aix.setLabelFormat("%u")
        self.x_Aix.setTickCount(11)
        self.x_Aix.setMinorTickCount(9)
        self.x_Aix.setTitleText("T")
        self.y_Aix = QValueAxis()
        self.y_Aix.setRange(10.00, 60.00)
        self.y_Aix.setLabelFormat("%u")
        self.y_Aix.setTickCount(11)
        self.y_Aix.setMinorTickCount(1)
        self.y_Aix.setTitleText("y")
        self.chart.addAxis(self.x_Aix, Qt.AlignBottom)
        self.chart.addAxis(self.y_Aix, Qt.AlignLeft)
        self.chart.addSeries(self.series_1)
        self.series_1.attachAxis(self.x_Aix)
        self.series_1.attachAxis(self.y_Aix)
        self.chartview = QChartView(self.chart)
        self.chartview.setGeometry(0, 0, 600, 600)
        self.chartview.setRenderHint(QPainter.Antialiasing)
        self.verticalLayout.addWidget(self.chartview)
