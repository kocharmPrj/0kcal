from PyQt5 import QtCore, QtGui, QtWidgets

from MainWindow import Ui_MainWindow
from FoodInfoDialog import Ui_FoodInfoDialog
from MenuInfoDialog import Ui_MenuInfoDialog
from TodayDiet import Ui_TodayDietWindow

class WindowCtrl:
    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def popDialog(self, view):
        self._view = view
        self._view.window = QtWidgets.QDialog()
        self._view.setupUi(self._view.window)
        self._view.window.show()

    def changeWindow(self, view):
        self._view = view
        self._view.window = QtWidgets.QMainWindow()
        self._view.setupUi(self._view.window)
        self._view.window.show()

    def _connectSignals(self):
        self._view.pushButton_foodInfo.clicked.connect(lambda: self.popDialog(Ui_FoodInfoDialog()))
        self._view.pushButton_menuInfo.clicked.connect(lambda: self.popDialog(Ui_MenuInfoDialog()))
        self._view.pushButton_todayDiet.clicked.connect(lambda: self.changeWindow(Ui_TodayDietWindow()))

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    view = Ui_MainWindow()
    view.setupUi(MainWindow)
    MainWindow.show()
    WindowCtrl(view=view)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()