from CalibrationModel import CalibrationModel
from CalibrationView import CalibrationView
from CalibrationPresenter import CalibrationPresenter
import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget
import PyQt5.QtWidgets as QtWidgets

class ValidationWindow(QtWidgets.QMainWindow):

    """
    The ValidationWindow class sets up the GUI for the validation stage by combining the CalibrationModel, CalibrationView, and CalibrationPresenter classes.
    It uses the same model, view and presenter classes as the CalibrationWindow class.
    """

    def __init__(self, row, col, interval):
        super().__init__()

        screen_geometry = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen_geometry.width(), screen_geometry.height()

        calmodel = CalibrationModel(row, col, interval, screen_width, screen_height-72, 'v')
        calview = CalibrationView()
        self.calpresenter = CalibrationPresenter(calmodel, calview)
        self.calpresenter.setModelMode('v')

        self.window = QtWidgets.QMainWindow()
        self.setCentralWidget(calview)
        self.setWindowTitle("Webcam Eye-tracking")
        #self.setMinimumSize(1280, 920)
        self.showMaximized()
        #self.setFixedSize(self.size())
        self.activateWindow()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ValidationWindow(4, 4, 1500)
    print("start")
    ui.show()
    sys.exit(app.exec_())