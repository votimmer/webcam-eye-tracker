from StartWindow import StartWindow
from SettingsWindow import SettingsWindow
from CalibrationWindow import CalibrationWindow
from ValidationWindow import ValidationWindow
from ImagesWindow import ImagesWindow
from WebcamWindow import WebcamWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys

class Main(QMainWindow):

    """
    The Main class represents the main window of the application. 
    It facilitates switching between different windows.
    """

    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.start_window = StartWindow()
        self.start_window.startbuttonSignal.connect(self.toWebcam)
        self.start_window.settingsbuttonSignal.connect(self.toSettings)
        self.stacked_widget.addWidget(self.start_window)

        self.webcam_window = WebcamWindow()
        self.webcam_window.startbuttonSignal.connect(self.returnToStart)
        self.webcam_window.calbuttonSignal.connect(self.toCalibration)
        self.stacked_widget.addWidget(self.webcam_window)

        self.settingswindow = SettingsWindow()
        self.settingswindow.settingspresenter.settingsview.returnbuttonSignal.connect(self.returnToStart)
        self.stacked_widget.addWidget(self.settingswindow)

        self.calibration_window = None
        self.validation_window = None
        self.image_window = None

        self.trained_model = None

        self.stacked_widget.setCurrentWidget(self.start_window)

    def returnToStart(self):
        """Switches to the Start Window."""
        self.stacked_widget.setCurrentWidget(self.start_window)

    def toSettings(self):
        """Switches to the Settings Window."""
        self.stacked_widget.setCurrentWidget(self.settingswindow)

    def toWebcam(self):
        """Switches to the Webcam Window."""
        self.stacked_widget.setCurrentWidget(self.webcam_window)

    def toCalibration(self):
        """Switches to the Calibration Window."""
        row, col, interval, samples = self.settingswindow.settingspresenter.getCalibrationParameters()
        self.calibration_window = CalibrationWindow(row, col, interval, samples)
        self.calibration_window.calpresenter.calview.buttonSignal.connect(self.toValidation)
        self.stacked_widget.addWidget(self.calibration_window)
        self.stacked_widget.setCurrentWidget(self.calibration_window)

    def toValidation(self):
        """Switches to the Validation Window."""
        self.trained_model = self.calibration_window.calpresenter.getTrainedModel()
        row, col = self.settingswindow.settingspresenter.getValidationParameters()
        self.validation_window = ValidationWindow(row, col, 100)
        self.validation_window.calpresenter.calview.buttonSignal.connect(self.toImageViewer)
        self.validation_window.calpresenter.calview.redoSignal.connect(self.toCalibration)
        self.validation_window.calpresenter.setTrainedModel(self.trained_model)
        self.stacked_widget.addWidget(self.validation_window)
        self.stacked_widget.setCurrentWidget(self.validation_window)
        self.validation_window.calpresenter.trackEyes()

    def toImageViewer(self):
        """Switches to the Image Viewer Window."""
        interval = self.settingswindow.settingspresenter.getImageInterval()
        self.image_window = ImagesWindow(interval)
        self.image_window.imgpresenter.imagesmodel.setRegressionModel(self.trained_model)
        self.stacked_widget.addWidget(self.image_window)
        self.stacked_widget.setCurrentWidget(self.image_window)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Main()
    ui.showMaximized()
    sys.exit(app.exec_())
