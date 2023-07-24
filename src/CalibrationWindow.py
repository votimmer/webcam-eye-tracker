from CalibrationModel import CalibrationModel
from CalibrationView import CalibrationView
from CalibrationPresenter import CalibrationPresenter
import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget
import PyQt5.QtWidgets as QtWidgets

class CalibrationWindow(QtWidgets.QMainWindow):

    """
    The CalibrationWindow class sets up the GUI for calibration by combining the CalibrationModel, CalibrationView, and CalibrationPresenter classes.
    """

    def __init__(self, row, col, interval, samples):
        super().__init__()

        screen_geometry = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen_geometry.width(), screen_geometry.height()

        calmodel = CalibrationModel(row, col, interval, screen_width, screen_height-72, 'c') #-72 to account for the height of the task bar
        calmodel.setSamples(samples)
        calview = CalibrationView()
        self.calpresenter = CalibrationPresenter(calmodel, calview)
        self.calpresenter.setModelMode('c')

        self.window = QtWidgets.QMainWindow()
        self.setCentralWidget(calview)
        self.setWindowTitle("Webcam Eye-tracking")
        #self.setMinimumSize(1280, 920)
        self.showMaximized()
        #self.setFixedSize(self.size())
        self.activateWindow()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = CalibrationWindow(2, 2, 1500, 50)
    print("start")
    ui.show()
    sys.exit(app.exec_())