from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedWidget, QDialog
from PyQt5.uic import loadUi
import sys
from PyQt5.QtCore import QTimer

from MainWidget import Ui_MainWidget
from DietWidget import Ui_DietWidget
from FoodInfoDialog import Ui_FoodInfoDialog
from MenuInfoDialog import Ui_MenuInfoDialog
from thread import RunVideo

class MainScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        # Add Button
        self.ui.pushButton_todayDiet.clicked.connect(parent.switch_diet)
        self.ui.pushButton_galleryView.clicked.connect(parent.switch_gallery)
        self.ui.pushButton_foodInfo.clicked.connect(parent.INMAIN_show_food_dialog)
        self.ui.pushButton_menuInfo.clicked.connect(parent.INMAIN_show_menu_dialog)


class DietScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DietWidget()
        self.ui.setupUi(self)

class GalleryScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DietWidget()
        self.ui.setupUi(self)

class FoodinfoScreen(QDialog):
    def __init__(self, pic, mat):
        super().__init__()
        self.ui = Ui_FoodInfoDialog(pic, mat)
        self.ui.setupUi(self)
        self.ui.picture.setPixmap(self.ui.tmpPicInDialog)

class MenuInfoScreen(QDialog):
    def __init__(self, pic, mat):
        super().__init__()
        self.ui = Ui_MenuInfoDialog(pic, mat)
        self.ui.setupUi(self)
        self.ui.label.setPixmap(self.ui.tmpPicInDialog)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.setGeometry(100, 100, 870, 770)
        self.STARTUP_show_main_window()

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

#        # Set up the layout
#        layout = QVBoxLayout(self)
#        layout.addWidget(self.switch_button)


    def switch_home(self):
        self.stacked_widget.setCurrentIndex(0)

    def switch_diet(self):
        self.stacked_widget.setCurrentIndex(1)

    def switch_gallery(self):
        self.stacked_widget.setCurrentIndex(2)

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
            # self.worker.start()


    # connect video thread to handler in ctrler
    def startVideoThread(self):
        self.worker = RunVideo()
        self.worker.matSignal.connect(self.handleVideoFrame)
        self.worker.start()


    def handleVideoFrame(self, MatTypeImg):
        qtImage = self.main_screen.ui.cvMatToQtImage(MatTypeImg)
        self.main_screen.ui.tmpQPic = qtImage
        self.main_screen.ui.tmpMat = MatTypeImg
        QTimer.singleShot(0, lambda: self.main_screen.ui.updateImageLabel(qtImage))


    def INMAIN_show_menu_dialog(self):
        self._menu_dialog = MenuInfoScreen(self.main_screen.ui.tmpQPic, self.main_screen.ui.tmpMat)
        self._menu_dialog.show()

    def INMAIN_show_food_dialog(self):
        self._food_dialog = FoodinfoScreen(self.main_screen.ui.tmpQPic, self.main_screen.ui.tmpMat)
        print("chk-1")
        self._food_dialog.ui.btnToStore.clicked.connect(lambda: self.INFOOD_store_food_data(self._food_dialog.ui.tmpPicInDialog, ''.join(map(str, self._food_dialog.ui.timeList)), self._food_dialog.ui.foodData))
        print("chk0")
        self._food_dialog.ui.btnToCancel.clicked.connect(self.INFOOD_cancel_food_dialog)
        self._food_dialog.show()

    def INFOOD_cancel_food_dialog(self):
        self._food_dialog = None

    def INFOOD_store_food_data(self, qtTypeImg, timeString, foodData):
        self.model.storeFoodData(qtTypeImg, timeString, foodData)
        self._food_dialog = None

    # def set_calories(self):
    #     _translate = QtCore.QCoreApplication.translate
    #     self.foodinfo_screen.comboBox_grams.setItemText(0, _translate("", "g"))
    #     self.foodinfo_screen.comboBox_grams.setItemText(1, _translate("", "g"))
    #     self.foodinfo_screen.comboBox_grams.setItemText(2, _translate("", "g"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
