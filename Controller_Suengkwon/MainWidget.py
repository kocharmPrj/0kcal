# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(870, 770)
        self.frame = QtWidgets.QFrame(MainWidget)
        self.frame.setGeometry(QtCore.QRect(80, 600, 700, 85))
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame.setStyleSheet("background-color:rgb(200, 200, 200);\\n\n"
        "padding: 10px 30px;\\n\n"
        "border-radius: 10px;\\n")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_todayDiet = QtWidgets.QPushButton(self.frame)
        self.pushButton_todayDiet.setGeometry(QtCore.QRect(20, 10, 200, 35))
        self.pushButton_todayDiet.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_todayDiet.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButton_todayDiet.setStyleSheet("background-color:rgb(50,150,150);\n"
        "color:white;\n"
        "border-radius:10px")
        self.pushButton_todayDiet.setObjectName("pushButton_todayDiet")
        self.pushButton_foodInfo = QtWidgets.QPushButton(self.frame)
        self.pushButton_foodInfo.setGeometry(QtCore.QRect(290, 10, 60, 35))
        self.pushButton_foodInfo.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pushButton_foodInfo.setStyleSheet("background-color:white;\n"
        "border-radius:10px")
        icon = QtGui.QIcon.fromTheme("camera-photo")
        self.pushButton_foodInfo.setIcon(icon)
        self.pushButton_foodInfo.setObjectName("pushButton_foodInfo")
        self.pushButton_galleryView = QtWidgets.QPushButton(self.frame)
        self.pushButton_galleryView.setGeometry(QtCore.QRect(480, 10, 200, 35))
        self.pushButton_galleryView.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_galleryView.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButton_galleryView.setStyleSheet("background-color:rgb(50,150,150);\n"
        "color:white;\n"
        "border-radius:10px")
        self.pushButton_galleryView.setObjectName("pushButton_galleryView")
        self.pushButton_menuInfo = QtWidgets.QPushButton(self.frame)
        self.pushButton_menuInfo.setGeometry(QtCore.QRect(360, 10, 60, 35))
        self.pushButton_menuInfo.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pushButton_menuInfo.setStyleSheet("background-color:white;\n"
        "border-radius:10px")
        icon = QtGui.QIcon.fromTheme("camera-photo")
        self.pushButton_menuInfo.setIcon(icon)
        self.pushButton_menuInfo.setObjectName("pushButton_menuInfo")
        self.label = QtWidgets.QLabel(MainWidget)
        self.label.setGeometry(QtCore.QRect(80, 80, 700, 500))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../../Downloads/jellyfish.jpg"))
        self.label.setObjectName("label")
        self.label.raise_()
        self.frame.raise_()

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWidget", "Form"))
        self.pushButton_todayDiet.setText(_translate("MainWidget", "Today\'s Diet"))
        self.pushButton_foodInfo.setText(_translate("MainWidget", "Food"))
        self.pushButton_galleryView.setText(_translate("MainWidget", "gallery view"))
        self.pushButton_menuInfo.setText(_translate("MainWidget", "Menu"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWidget = QtWidgets.QWidget()
    ui = Ui_MainWidget()
    ui.setupUi(MainWidget)
    MainWidget.show()
    sys.exit(app.exec_())
