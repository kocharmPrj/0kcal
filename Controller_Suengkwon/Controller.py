from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedWidget, QDialog
from PyQt5.uic import loadUi
import sys

from MainWidget import Ui_MainWidget
from DietWidget import Ui_DietWidget
from FoodInfoDialog import Ui_FoodInfoDialog
from MenuInfoDialog import Ui_MenuInfoDialog

class MainScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        # Add Button
        self.ui.pushButton_todayDiet.clicked.connect(parent.switch_diet)
        self.ui.pushButton_galleryView.clicked.connect(parent.switch_gallery)
        self.ui.pushButton_foodInfo.clicked.connect(parent.popup_food)
        self.ui.pushButton_menuInfo.clicked.connect(parent.popup_menu)

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
    def __init__(self):
        super().__init__()
        self.ui = Ui_FoodInfoDialog()
        self.ui.setupUi(self)

class MenuInfoScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MenuInfoDialog()
        self.ui.setupUi(self)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.setGeometry(100, 100, 870, 770)

        # Load UI objects
        self.main_screen = MainScreen(self)
        self.diet_screen = DietScreen()
        self.gallery_screen = GalleryScreen()
        self.foodinfo_screen = FoodinfoScreen()
        self.menuifo_screen = MenuInfoScreen()

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

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.switch_button)


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
