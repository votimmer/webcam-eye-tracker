from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import PyQt5.QtCore as QtCore
import numpy as np
from Webcam import Webcam

class WebcamWindow(QWidget):

    """
    The WebcamWindow class is responsible for displaying a webcam feed in a GUI.
    """

    startbuttonSignal = QtCore.pyqtSignal()
    calbuttonSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        self.no_webcam_text = "No webcams connected"
        self.permission_text = "By pressing this button, you give permission to access your webcam. No actual footage will be stored."

        #Creates a button asking the user for permission to access their webcam
        self.permission_button = QPushButton(self.permission_text) 
        self.permission_button.clicked.connect(self.permitWebcamAccess)
        self.permission_button.setFixedSize(640, 150)

        #Create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        self.textLabel = QLabel('Webcam')

        #Create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.permission_button, alignment=Qt.AlignCenter)
        vbox.addWidget(self.image_label)
        
        #self.image_label.hide()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.calibration_text = "Start calibration"
        self.calibration_button = QPushButton(self.calibration_text)
        self.calibration_button.setFixedSize(640, 50)
        self.calibration_button.clicked.connect(self.calibration_button_clicked)
        self.calibration_button.setDisabled(True)
        vbox.addWidget(self.calibration_button, alignment=Qt.AlignHCenter)

        self.return_text = "Return to start menu"
        self.return_button = QPushButton(self.return_text)
        self.return_button.setFixedSize(640, 50)
        self.return_button.clicked.connect(self.return_button_clicked)
        vbox.addWidget(self.return_button, alignment=Qt.AlignHCenter)
        self.setLayout(vbox)

        #Create the video capture thread
        self.thread = Webcam()

    def calibration_button_clicked(self):
        """Emits a signal when the calibration button is clicked."""
        self.calbuttonSignal.emit()

    def return_button_clicked(self):
        """Emits a signal when the return button is clicked."""
        self.startbuttonSignal.emit()

    def permitWebcamAccess(self):
        """Starts recording if the user gives permission to access their webcam."""
        self.permission_button.hide()
        if self.thread.noWebcams() == False:
            self.calibration_button.setEnabled(True)
            self.start_recording()
        else:
            self.image_label.setText(self.no_webcam_text)

    def start_recording(self):
        #Connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        #Start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = WebcamWindow()
    #a.start_recording()
    a.showMaximized()
    sys.exit(app.exec_())