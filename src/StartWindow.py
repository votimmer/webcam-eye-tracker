from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
import PyQt5.QtCore as QtCore
import sys

class StartWindow(QWidget):

    """
    The StartWindow class represents the initial window shown to the user.
    Through this window the user can either view the settings or start calibration.
    """

    startbuttonSignal = QtCore.pyqtSignal()
    settingsbuttonSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        title_text = "Webcam Eye Tracker"
        title_label = QLabel(title_text)
        title_label.setStyleSheet("font-size: 36px;")
        self.layout.addWidget(title_label)
        title_label.setAlignment(Qt.AlignCenter)

        start_text = "Start eye tracking"
        start_button = QPushButton(start_text)
        start_button.setStyleSheet("font-size: 18px;")
        start_button.clicked.connect(self.startbutton_clicked)
        start_button.setFixedSize(640, 50)
        self.layout.addWidget(start_button, alignment=Qt.AlignHCenter)

        settings_text = "Settings"
        settings_button = QPushButton(settings_text)
        settings_button.setStyleSheet("font-size: 18px;")
        settings_button.clicked.connect(self.settingsbutton_clicked)
        settings_button.setFixedSize(640, 50)
        self.layout.addWidget(settings_button, alignment=Qt.AlignHCenter)

        self.setLayout(self.layout)
        #self.setFixedSize(1280, 720)

    def startbutton_clicked(self):
        """Emits a signal when the start button is pressed."""
        self.startbuttonSignal.emit()
        #print("Clicked")

    def settingsbutton_clicked(self):
        """Emits a signal when the settings button is pressed."""
        self.settingsbuttonSignal.emit()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = StartWindow()
    ui.showMaximized()
    sys.exit(app.exec_())
