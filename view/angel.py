# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'angel.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 50, 771, 511))
        self.widget.setObjectName("widget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.showInfo = QtWidgets.QPushButton(self.widget)
        self.showInfo.setObjectName("showInfo")
        self.gridLayout_2.addWidget(self.showInfo, 1, 1, 1, 1)
        self.hidInfo = QtWidgets.QPushButton(self.widget)
        self.hidInfo.setObjectName("hidInfo")
        self.gridLayout_2.addWidget(self.hidInfo, 1, 2, 1, 1)
        self.closeCam1 = QtWidgets.QPushButton(self.widget)
        self.closeCam1.setObjectName("closeCam1")
        self.gridLayout_2.addWidget(self.closeCam1, 1, 3, 1, 1)
        self.getCam1 = QtWidgets.QPushButton(self.widget)
        self.getCam1.setObjectName("getCam1")
        self.gridLayout_2.addWidget(self.getCam1, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 47, 14))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 4)
        self.gridLayout_5.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 47, 14))
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 2)
        self.getCam2 = QtWidgets.QPushButton(self.widget)
        self.getCam2.setObjectName("getCam2")
        self.gridLayout_3.addWidget(self.getCam2, 1, 0, 1, 1)
        self.closeCam2 = QtWidgets.QPushButton(self.widget)
        self.closeCam2.setObjectName("closeCam2")
        self.gridLayout_3.addWidget(self.closeCam2, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.lengthLineEdit = QtWidgets.QLineEdit(self.widget)
        self.lengthLineEdit.setObjectName("lengthLineEdit")
        self.gridLayout.addWidget(self.lengthLineEdit, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)
        self.widLineEdit = QtWidgets.QLineEdit(self.widget)
        self.widLineEdit.setObjectName("widLineEdit")
        self.gridLayout.addWidget(self.widLineEdit, 1, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.heightLineEdit = QtWidgets.QLineEdit(self.widget)
        self.heightLineEdit.setObjectName("heightLineEdit")
        self.gridLayout.addWidget(self.heightLineEdit, 2, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.widget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 2, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.innnerRadiusLineEdit = QtWidgets.QLineEdit(self.widget)
        self.innnerRadiusLineEdit.setObjectName("innnerRadiusLineEdit")
        self.gridLayout.addWidget(self.innnerRadiusLineEdit, 3, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 3, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 4, 0, 1, 1)
        self.outerRadiusLineEdit = QtWidgets.QLineEdit(self.widget)
        self.outerRadiusLineEdit.setObjectName("outerRadiusLineEdit")
        self.gridLayout.addWidget(self.outerRadiusLineEdit, 4, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.widget)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 4, 2, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.BrightnessHorizontalSlider_Dark = QtWidgets.QSlider(self.widget)
        self.BrightnessHorizontalSlider_Dark.setOrientation(QtCore.Qt.Horizontal)
        self.BrightnessHorizontalSlider_Dark.setObjectName("BrightnessHorizontalSlider_Dark")
        self.gridLayout_4.addWidget(self.BrightnessHorizontalSlider_Dark, 0, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.widget)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 1, 0, 1, 1)
        self.BrightnessHorizontalSlider = QtWidgets.QSlider(self.widget)
        self.BrightnessHorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.BrightnessHorizontalSlider.setObjectName("BrightnessHorizontalSlider")
        self.gridLayout_4.addWidget(self.BrightnessHorizontalSlider, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.showInfo.setText(_translate("MainWindow", "????????????"))
        self.hidInfo.setText(_translate("MainWindow", "????????????"))
        self.closeCam1.setText(_translate("MainWindow", "????????????"))
        self.getCam1.setText(_translate("MainWindow", "????????????"))
        self.groupBox.setTitle(_translate("MainWindow", "?????????"))
        self.label.setText(_translate("MainWindow", "video1"))
        self.groupBox_2.setTitle(_translate("MainWindow", "????????????"))
        self.label_2.setText(_translate("MainWindow", "video2"))
        self.getCam2.setText(_translate("MainWindow", "????????????"))
        self.closeCam2.setText(_translate("MainWindow", "????????????"))
        self.label_5.setText(_translate("MainWindow", "??????"))
        self.label_6.setText(_translate("MainWindow", "mm"))
        self.label_7.setText(_translate("MainWindow", "??????"))
        self.label_11.setText(_translate("MainWindow", "mm"))
        self.label_8.setText(_translate("MainWindow", "??????"))
        self.label_12.setText(_translate("MainWindow", "mm"))
        self.label_9.setText(_translate("MainWindow", "??????"))
        self.label_13.setText(_translate("MainWindow", "mm"))
        self.label_10.setText(_translate("MainWindow", "??????"))
        self.label_14.setText(_translate("MainWindow", "mm"))
        self.label_4.setText(_translate("MainWindow", "????????????"))
        self.label_16.setText(_translate("MainWindow", "????????????"))
