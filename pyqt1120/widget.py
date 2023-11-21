# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import cv2

from PySide2.QtWidgets import (
        QApplication, QWidget, QPushButton,
        QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit)
from PySide2.QtGui import QPixmap, QColor, QImage
from PySide2.QtCore import QFile, Qt, QSize
from PySide2.QtUiTools import QUiLoader
from thread import RunVideo
from ViewForCalorieInfoDialog import ViewForFoodInfoDialog, ViewForMenuInfoDialog


class DefaultWidget(QMainWindow):
    def __init__(self):
        super(DefaultWidget, self).__init__()
        self.setWindowTitle("main")
        self.tmpMat = None
        self.tmpPic = None
        self.initUI()

    def initUI(self):
        self.btnTakeShotMenu = QPushButton("get Menu")
        self.btnTakeShotMenu.clicked.connect(self.theBtn_was_clicked)
        self.btnTakeShotFood = QPushButton("get Food")
        self.btnTakeShotFood.clicked.connect(self.theBtn_was_clicked)
        layout1_V2 = QVBoxLayout()
        layout1_V2.addWidget(self.btnTakeShotMenu)
        layout1_V2.addWidget(self.btnTakeShotFood)

        self.button = QPushButton("btn")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.theBtn_was_clicked)
        self.button.clicked.connect(self.theBtn_was_toggled)
        self.setCentralWidget(self.button)
        self.label = QLabel()
        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)
        self.image_label = QLabel(self)
        self.greyImg = QPixmap(640, 480)
        self.greyImg.fill(QColor('darkgrey'))
        self.image_label.setPixmap(self.greyImg)
        layout1_V1 = QVBoxLayout()
        layout1_V1.addWidget(self.input)
        layout1_V1.addWidget(self.label)
        layout1_V1.addWidget(self.button)
        layout1_V1.addWidget(self.image_label)

        layout1_H = QHBoxLayout()
        layout1_H.addLayout(layout1_V1)
        layout1_H.addLayout(layout1_V2)
        container = QWidget()
        container.setLayout(layout1_H)

        self.thread = self.startVideoThread()

        self.setCentralWidget(container)
        # self.load_ui()

    def startVideoThread(self):
        self.worker = RunVideo()
        self.worker.start()
        self.worker.matSignal.connect(self.updateFrame)

    def updateFrame(self, img):
        qtImage = self.cvMatToQtImage(img)
        self.tmpPic = qtImage
        self.tmpMat = img
        self.image_label.setPixmap(qtImage)

    def cvMatToQtImage(self, mat) -> QPixmap:
        rgbImage = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = w * ch
        convertToQtImageFormat = QImage(rgbImage, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtImageFormat.scaled(QSize(640, 480), aspectMode=Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def theBtn_was_clicked(self):
        senderBtn = self.sender()

        if senderBtn == self.btnTakeShotFood:
            print("hi")
            foodDialog = ViewForFoodInfoDialog(self.tmpPic, self.tmpMat)
            # foodDialog.getPicAndMatData(self.tmpPic, self.tmpMat)
            # foodDialog.setImageLabel(foodDialog.tmpPicInDialog)
            foodDialog.exec_()
        elif senderBtn == self.btnTakeShotFood:
            print("hi2")

        # self.button.setText("you clicked me?")
        # self.button.setEnabled(False)

    def theBtn_was_toggled(self, checked):
        print("checked? : ", checked)
        print("2. ", self.button.isChecked())

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    app = QApplication([])
    window = DefaultWidget()
    window.show()
    sys.exit(app.exec_())
