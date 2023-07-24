from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import PyQt5.QtCore as QtCore

class SettingsView(QWidget):

    """
    The SettingsView class is responsible for managing the GUI components of the display and modification of the settings.
    """
    
    returnbuttonSignal = QtCore.pyqtSignal()
    savebuttonSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        
        # Create input fields for calibration phase
        self.calrowLabel = QLabel()
        self.calrowLabel.setAlignment(Qt.AlignCenter)
        self.calrowLabel.setStyleSheet("font-size: 14px;")
        self.calrows = QLineEdit()
        self.calrows.setObjectName("calrows")
        #self.calrows.setFixedSize(500, 25)

        self.calcolLabel = QLabel()
        self.calcolLabel.setStyleSheet("font-size: 14px;")
        self.calcolLabel.setAlignment(Qt.AlignCenter)
        self.calcols = QLineEdit()
        self.calcols.setObjectName("calcols")
        #self.calcols.setFixedSize(500, 25)

        self.calintervalLabel = QLabel()
        self.calintervalLabel.setStyleSheet("font-size: 14px;")
        self.calintervalLabel.setAlignment(Qt.AlignCenter)
        self.calinterval = QLineEdit()
        self.calinterval.setObjectName("calinterval")

        #Create input fields for validation phase
        self.valrowLabel = QLabel()
        self.valrowLabel.setStyleSheet("font-size: 14px;")
        self.valrowLabel.setAlignment(Qt.AlignCenter)
        self.valrows = QLineEdit()
        self.valrows.setObjectName("valrows")

        self.valcolLabel = QLabel()
        self.valcolLabel.setStyleSheet("font-size: 14px;")
        self.valcolLabel.setAlignment(Qt.AlignCenter)
        self.valcols = QLineEdit()
        self.valcols.setObjectName("valcols")

        self.samplesLabel = QLabel()
        self.samplesLabel.setStyleSheet("font-size: 14px;")
        self.samplesLabel.setAlignment(Qt.AlignCenter)
        self.samples = QLineEdit()
        self.samples.setObjectName("samples")

        self.imgintervalLabel = QLabel()
        self.imgintervalLabel.setStyleSheet("font-size: 14px;")
        self.imgintervalLabel.setAlignment(Qt.AlignCenter)
        self.imginterval = QLineEdit()
        self.imginterval.setObjectName("imginterval")

        #Create buttons
        self.return_button_text = "Return to start menu"
        return_button = QPushButton(self.return_button_text)
        return_button.setStyleSheet("font-size: 18px;")
        return_button.clicked.connect(self.returnbutton_clicked)
        return_button.setFixedHeight(50)

        self.save_button = QPushButton()
        self.save_button.setStyleSheet("font-size: 18px;")
        self.save_button.clicked.connect(self.savebutton_clicked)
        self.save_button.setFixedHeight(50)

        #Create layout and add widgets
        self.layout = QVBoxLayout()
        callabel_layout = QHBoxLayout()
        callabel_layout.addWidget(self.calrowLabel)
        callabel_layout.addWidget(self.calcolLabel)
        callabel_layout.setSpacing(20)
        self.layout.addLayout(callabel_layout)

        cal_layout = QHBoxLayout()  #New horizontal layout for calrows and calcols
        cal_layout.addWidget(self.calrows)
        cal_layout.addWidget(self.calcols)
        cal_layout.setSpacing(20)
        self.layout.addLayout(cal_layout)

        self.layout.addWidget(self.calintervalLabel)
        self.layout.addWidget(self.calinterval)
        self.layout.addWidget(self.samplesLabel)
        self.layout.addWidget(self.samples)

        vallabel_layout = QHBoxLayout()
        vallabel_layout.addWidget(self.valrowLabel)
        vallabel_layout.addWidget(self.valcolLabel)
        vallabel_layout.setSpacing(20)
        self.layout.addLayout(vallabel_layout)

        val_layout = QHBoxLayout()
        val_layout.addWidget(self.valrows)
        val_layout.addWidget(self.valcols)
        val_layout.setSpacing(20)
        self.layout.addLayout(val_layout)
        
        self.layout.addWidget(self.imgintervalLabel)
        self.layout.addWidget(self.imginterval)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(return_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.setContentsMargins(0, 75, 0, 0)
        self.layout.addLayout(buttons_layout)
        #layout.addWidget(return_button)

        self.layout.setContentsMargins(350, 200, 350, 150)

        self.setLayout(self.layout)
        #self.showMaximized()

    def hideTextFields(self):
        """Hides all text input fields."""
        for widget in self.findChildren(QLineEdit):
            widget.hide()

    def showTextFields(self):
        """Shows all text input fields."""
        for widget in self.findChildren(QLineEdit):
            widget.show()

    def changeButtonText(self, text):
        """Changes the text of the savebutton object."""
        self.save_button.setText(text)

    def returnbutton_clicked(self):
        """Emits a signal when the return button is pressed."""
        self.returnbuttonSignal.emit()

    def savebutton_clicked(self):
        """Emits a signal when the save button is pressed."""
        self.savebuttonSignal.emit()

    def getCalDimensions(self):
        """Returns the values entered in the calibration text fields."""
        rows = self.calrows.text()
        cols = self.calcols.text()
        return rows, cols
    
    def getCalInterval(self):
        """Returns the value entered in the calibration interval text field."""
        return self.calinterval.text()
    
    def getCalSamples(self): 
        """Returns the value entered in the samples input text field."""
        return self.samples.text()
    
    def getValDimensions(self):
        """Returns the values entered in the validation text fields."""
        rows = self.valrows.text()
        cols = self.valcols.text()
        return rows, cols
    
    def getImageInterval(self):
        """Returns the value entered in the image interval text field."""
        return self.imginterval.text()

    def showCalDimensions(self, rows, cols):
        """Shows the number of rows and columns the calibration grid will have."""
        self.calrowLabel.setText("Number of rows in calibration grid: {}".format(rows))
        self.calcolLabel.setText("Number of columns in calibration grid: {}".format(cols))

    def showCalInterval(self, interval):
        """Shows the interval after which new eye position data can be gathered."""
        self.calintervalLabel.setText("Each calibration point will be shown for: {} milliseconds".format(interval))

    def showCalSamples(self, samples):
        """Shows the number of iris position samples that will be taken at each calibration point."""
        self.samplesLabel.setText("For each calibration point, {} samples will be taken of the iris positions".format(samples))

    def showValDimensions(self, rows, cols):
        """Shows the number of rows and columns the validation grid will have."""
        self.valrowLabel.setText("Number of rows in validation grid: {}".format(rows))
        self.valcolLabel.setText("Number of columns in validation grid: {}".format(cols))

    def showImgInterval(self, interval):
        """Shows the interval after which new image will be displayed."""
        self.imgintervalLabel.setText("Each image will be shown for: {} milliseconds".format(interval))
