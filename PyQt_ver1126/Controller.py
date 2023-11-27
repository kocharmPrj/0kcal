from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedWidget, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QTimer
# from PyQt5.uic import loadUi
import sys

from MainWidget import Ui_MainWidget
from DietWidget import Ui_DietWidget
from FoodInfoDialog import Ui_FoodInfoDialog
from MenuInfoDialog import Ui_MenuInfoDialog

from thread import RunVideo
from ObjectDetection import ObjectDetector
from MenuProcess import MenuProcessor
from functools import partial
from Model import Model


class MainScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        # Add Button
        self.ui.pushButton_todayDiet.clicked.connect(parent.INMAIN_switch_diet_widget)
        self.ui.pushButton_galleryView.clicked.connect(parent.switch_gallery)
        self.ui.pushButton_foodInfo.clicked.connect(parent.INMAIN_show_food_dialog)
        self.ui.pushButton_menuInfo.clicked.connect(parent.INMAIN_show_menu_dialog)


class DietScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DietWidget()


class GalleryScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DietWidget()
        self.ui.setupUi(self)


class FoodinfoScreen(QDialog):
    def __init__(self, pic, mat, foodList):
        super().__init__()
        self.ui = Ui_FoodInfoDialog(pic, mat, foodList)
        self.ui.setupUi(self)
        self.ui.tmpPicInDialog = self.ui.tmpPicInDialog.scaled(360, 310)
        self.ui.picture.setPixmap(self.ui.tmpPicInDialog)

        # Add Button
        for i in range(self.ui.count):
            self.ui.select_button_list[i].clicked.connect(
                partial(self.ui.selectButtonTo, i)
            )


class MenuInfoScreen(QDialog):
    def __init__(self, pic, mat, foodList):
        super().__init__()
        self.ui = Ui_MenuInfoDialog(pic, mat, foodList)
        self.ui.setupUi(self)
        self.ui.tmpPicInDialog = self.ui.tmpPicInDialog.scaled(530, 470)
        self.ui.label.setPixmap(self.ui.tmpPicInDialog)

        # Add Button
        for i in range(self.ui.count):
            self.ui.select_button_list[i].clicked.connect(
                partial(self.ui.selectButtonTo, i)
            )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.setGeometry(100, 100, 870, 770)
        self.STARTUP_show_main_window()
        self.modelClass = Model()

        # Load UI objects
        self.main_screen = MainScreen(self)
        self.diet_screen = DietScreen()
        self.gallery_screen = GalleryScreen()

        # Add a widgets to the stack
        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.diet_screen)
        self.stacked_widget.addWidget(self.gallery_screen)

        # Set the index of the widget
        self.stacked_widget.setCurrentIndex(0)

        # Associating buttons with interations
        self.switch_button = QPushButton("", self)
        self.switch_button.setGeometry(QtCore.QRect(740, 40, 45, 40))
        self.switch_button.setStyleSheet("border-image:url(\"home.png\");\n")
        self.switch_button.clicked.connect(self.switch_home)

        # MessageBox
        self.msg = QMessageBox()

        # Load Object
        self.food_model_xml_path = "model/model.xml"
        self.food_model_bin_path = "model/model.bin"
        self._detector = ObjectDetector(
            self.food_model_xml_path,
            self.food_model_bin_path
        )

    def switch_home(self):
        self.stacked_widget.setCurrentIndex(0)

    def INMAIN_switch_diet_widget(self):
        returnFile = self.modelClass.loadFoodData()
        if returnFile is None:
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("오류 메세지")
            self.msg.setText("   오늘의 기록이 없습니다.!   ")
            self.msg.exec_()
        else:
            textInFile, imgInFile = returnFile
            print(textInFile)
            self.diet_screen.ui.setData(textInFile, imgInFile)
            self.diet_screen.ui.setupUi(self.diet_screen)
            self.stacked_widget.setCurrentIndex(1)

    def switch_gallery(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle("오류 메세지")
        self.msg.setText("   To be continue...   ")
        self.msg.exec_()

    def popup_food(self):
        self.foodinfo_screen.setWindowTitle('Dialog')
        # self.dialog.resize(640, 480)
        self.foodinfo_screen.show()

    def popup_menu(self):
        self.menuifo_screen.setWindowTitle('Dialog')
        # self.dialog.resize(640, 480)
        self.menuifo_screen.show()

    def STARTUP_show_main_window(self):
        self.startVideoThread()

    # connect video thread to handler in ctrler
    def startVideoThread(self):
        self.worker = RunVideo()
        self.worker.matSignal.connect(self.handleVideoFrame)
        self.worker.start()

    def handleVideoFrame(self, MatTypeImg):
        qtImage = self.main_screen.ui.cvMatToQtImage(MatTypeImg)
        self.main_screen.ui.tmpQPic = qtImage
        self.main_screen.ui.tmpMat = MatTypeImg
        QTimer.singleShot(
            0,
            lambda: self.main_screen.ui.updateImageLabel(qtImage)
        )

    def INMAIN_show_menu_dialog(self):
        try:
            menu_model_xml_path = "./model/openvino.xml"
            self.save_image = self.main_screen.ui.tmpMat
            self._infer = MenuProcessor(
                self.main_screen.ui.tmpMat,
                menu_model_xml_path
            )
            self.scan_image = self._infer.preprocessing()
            self._infer.MakeRoi(self.scan_image)
            self.result_strings = self._infer.Inference(self.scan_image)

            # make menu list using info read by inference
            menuList = []
            for elem in self.result_strings:
                menuList.append(self.modelClass.foodInfoRequest(elem))
            try:
                self._menu_dialog = MenuInfoScreen(
                    self.main_screen.ui.tmpQPic,
                    self.main_screen.ui.tmpMat, menuList
                )
            except Exception as e:
                print("Err :", e)
            self._menu_dialog.show()

        # if can't read menu board
        except Exception as e:
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("오류 메세지")
            self.msg.setText("   메뉴가 인식되지 않았습니다!   ")
            self.msg.exec_()

    def INMAIN_show_food_dialog(self):
        _translate = QtCore.QCoreApplication.translate

        # get food list(label_names_list) found on picture frame
        self.tmpImgSave = self.main_screen.ui.tmpMat
        label_names_list = self._detector.detect_objects(self.tmpImgSave)

        # get food info of food list
        foodList = []
        for elem in label_names_list:
            elem = self.modelClass.getHighestSimilarityFoodName(elem)
            foodList.append(self.modelClass.foodInfoRequest(elem))

        self._food_dialog = FoodinfoScreen(
            self.main_screen.ui.tmpQPic,
            self.tmpImgSave,
            foodList
        )

        self._food_dialog.ui.btnToStore.clicked.connect(
            lambda: self.INFOOD_store_food_data(
                self.tmpImgSave,
                ''.join(map(str, self._food_dialog.ui.timeStr)),
                self._food_dialog.ui.local_db
            )
        )
        self._food_dialog.ui.btnToCancel.clicked.connect(
            self.INFOOD_cancel_food_dialog
        )
        for foodName in label_names_list:
            foodList.append(self.modelClass.foodInfoRequest(foodName))
        # self._food_dialog.ui.chgCnt(len(foodList)+1)

        if label_names_list == []:
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("오류 메세지")
            self.msg.setText("   음식이 인식되지 않았습니다!   ")
            self.msg.exec_()
        else:
            time = self._food_dialog.ui.timeList
            strTime = '{:4d}/{:2d}/{:2d} {:2d}:{:2d}'.format(
                time[0], time[1], time[2], time[3], time[4]
            )
            '''
            rcvFoodNameList = []
            for i in label_names_list:
                rcvFoodNameList.append(requesthttp(i))
            '''
            self._food_dialog.ui.date.setText(
                _translate("FoodInfoDialog", strTime))
            self._food_dialog.show()

    def INFOOD_cancel_food_dialog(self):
        self._food_dialog.hide()
        self._food_dialog = None

    def INFOOD_store_food_data(self, qtTypeImg, timeString, foodData):
        self.modelClass.storeFoodData(qtTypeImg, timeString, foodData)
        self._food_dialog = None

    def INFOOD_infer_food_name(self, ):
        # self.model.storeFoodData(qtTypeImg, timeString, foodData)
        self._food_dialog = None

    # Keyboard Interrupt
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_F:
            self.INMAIN_show_food_dialog()
        elif e.key() == Qt.Key_M:
            self.INMAIN_show_menu_dialog()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
