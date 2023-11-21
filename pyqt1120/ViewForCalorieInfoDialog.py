# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import (
        QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit)
from PySide2.QtGui import QPixmap, QColor, QImage
from PySide2.QtCore import Qt, QSize
import sys
import cv2
import time
from thread import ThreadWorker


class AbstractViewForCalorieInfoDialog(QDialog):
    # after make ai processing func, delete para "pic"
    # because ai processing func will set pic. this is just for test
    def __init__(self, pic=None, mat=None):
        super().__init__()
        self.image_label = QLabel(self)
        self.greyImg = QPixmap(640, 480)
        self.greyImg.fill(QColor('darkgrey'))
        self.image_label.setPixmap(self.greyImg)
        self.tmpPicInDialog = None
        self.tmpMatInDialog = None
        if pic is not None:
            print("pic is not None in abstract")
            self.tmpPicInDialog = pic
        else :
            print("pic is None in abstract")
        if mat is not None:
            self.tmpMatInDialog = mat

    def getPicAndMatData(self, pic, mat):
        self.tmpPicInDialog = pic
        self.tmpMatInDialog = mat

    # for cvt Mat data from ai processing to convert to QPixmap proper to show in qt
    def cvMatToQtImage(self, mat) -> QPixmap:
        rgbImage = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = w * ch
        convertToQtImageFormat = QImage(rgbImage, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtImageFormat.scaled(QSize(640, 480), aspectMode=Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class ViewForFoodInfoDialog(AbstractViewForCalorieInfoDialog):
    def __init__(self, pic=None, mat=None):
        super().__init__(pic, mat)
        if pic is not None:
            print("got pic in init of food info")
        else :
            print("empty in food info..")
        if pic is not None:
            print("chk!")
            self.tmpPicInDialog = pic
        if mat is not None:
            self.tmpMatInDialog = mat
        self.foodName = QLabel('tmp', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Food Info")
        self.timeList = self.getTime()
        time_str = [str(i) for i in self.timeList]
        foodName_const = QLabel("Food", self)
        currentTime_const = QLabel("Time", self)
        self.currentTime = QLabel(' '.join(time_str), self)
        self.setGeometry(100, 100, 800, 600)

        # for view test showing frame in poped up Dialog
        print("chk1")
        if self.tmpPicInDialog is not None:
            print("chk2")
            self.image_label.setPixmap(self.tmpPicInDialog)
        else :
            print("empty!")
        print("chk3")

        Layout1_V1 = QVBoxLayout()
        # self.Layout1_V1.addWidget(self.image_label)
        Layout1_V2 = QVBoxLayout()
        Layout1_V2.addWidget(foodName_const)
        Layout1_V2.addWidget(self.foodName)
        Layout1_V2.addWidget(currentTime_const)
        Layout1_V2.addWidget(self.currentTime)
        Layout1_H = QHBoxLayout()
        Layout1_H.addLayout(Layout1_V1)
        Layout1_H.addLayout(Layout1_V2)
        container = QDialog()
        container.setLayout(Layout1_H)
        print("chk4")

        # container.show()

    def getTime(self) -> time:
        tm = time.localtime(time.time())
        returnList = [tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min]
        return returnList

    def setTextOnFoodName(self, new_name):
        self.foodName(new_name)

    # call this func everytime this Dialog poped up = call this func in ai processing func
    def setImageLabel(self, pic):
        return self.image_label.setPixmap(pic)

    # todo
    # make updating text function

    # todo
    # make ai processing func of obj detection


class ViewForMenuInfoDialog(AbstractViewForCalorieInfoDialog):
    def __init__(self, pic=None, mat=None):
        super().__init__()
        self.setWindowTitle("Menu Info")

    # todo
    # make ai processing func of classification reading the menu
