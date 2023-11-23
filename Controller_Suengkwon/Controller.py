from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedWidget, QDialog
from PyQt5.uic import loadUi
import sys

from MainWidget import Ui_MainWidget
from DietWidget import Ui_DietWidget
from FoodInfoDialog import Ui_FoodInfoDialog
from MenuInfoDialog import Ui_MenuInfoDialog

class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("MainWidget.ui", self)

class DietScreen(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("DietWidget.ui", self)

class GalleryScreen(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("DietWidget.ui", self)

class FoodinfoScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("FoodInfoDialog.ui", self)

class MenuInfoScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("MenuInfoDialog.ui", self)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Load UI objects
        self.main_screen = MainScreen()
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
        self.switch_button = QPushButton("Home", self)
        self.switch_button.clicked.connect(self.switch_home)
        self.main_screen.pushButton_todayDiet.clicked.connect(self.switch_diet)
        self.main_screen.pushButton_galleryView.clicked.connect(self.switch_gallery)
        self.main_screen.pushButton_foodInfo.clicked.connect(self.popup_food)
        self.main_screen.pushButton_menuInfo.clicked.connect(self.popup_menu)
        
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())