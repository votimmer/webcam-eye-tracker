from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import  QLabel, QPushButton, QWidget

class CalibrationView(QWidget):

    """
    The CalibrationView class is responsible for managing the GUI components of the calibration and validation phases.
    """

    buttonSignal = QtCore.pyqtSignal()
    spacebarSignal = QtCore.pyqtSignal()
    redoSignal = QtCore.pyqtSignal()

    def __init__ (self):
        super().__init__()
        self.visited = [] #contains the cells that the visual marker has inhabited 
        self.currentDot = None #dot that is currently visible
        self.eyeCursor = None 
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.button = None
        self.redo_button = None
        self.text_label = None

    def spacebar_Click(self): 
        """Sends a signal when the space bar is pressed."""
        self.spacebarSignal.emit()

    def button_Click(self):
        """Sends a signal when the button is clicked."""
        self.buttonSignal.emit()

    def redobutton_Click(self):
        """Sends a signal when the button to redo calibration is clicked."""
        self.redoSignal.emit()

    def createDot(self, cell):
        """Creates a dot that will serve as the visual marker in a calibration phase."""
        dot = QLabel(self)
        dot_size = 50
        dot.setFixedSize(dot_size, dot_size)
        dot.setStyleSheet(
            "background: #BDB246;" + 
            "border-radius: 25px;"
            )
        self.currentDot = dot
        dot.move(cell[0], cell[1])
        dot.show()
    
    def hideDot(self, dot): 
        """Hides the given dot."""
        if dot is not None:
            #previous dot is made 'invisible' by setting the opacity to 0
            dot.setStyleSheet(
                "opacity: 0.0;" + 
                "border-radius: 37px;"
                ) 
            
    def createEyeCursor(self):
        """Creates a circular QLabel that acts as a eye-controlled cursor."""
        cursor = QLabel(self)
        cursor.setFixedSize(26, 26)
        cursor.setStyleSheet(
            "background: #CA2E55;" +
            "border-radius: 13px;"
        )
        self.eyeCursor = cursor
        cursor.show()
    
    def moveEyeCursor(self, position):
        """Moves a circular QLabel to the location on the screen a person is looking at."""
        self.eyeCursor.move(position[0], position[1])

    def keyPressEvent(self, event):
        """Moves the dot and makes screencaps of person's face after the space bar is pressed."""
        if event.key() == QtCore.Qt.Key_Space:
            self.spacebar_Click()
            print("Current dot position: {}".format(self.currentDot.pos()))

    def countdown(self, interval):
        """Disables input evens for 'interval' milliseconds."""
        self.setDisabled(True)
        QTimer.singleShot(
            interval, 
            lambda: self.currentDot.setStyleSheet( #The dot changes color after 'interval' milliseconds have passed
                "background: #8A6552;" +
                "border-radius: 25px;"
            )
        )
        QTimer.singleShot(interval, self.enable_and_focus)

    def enable_and_focus(self):
        """Enables spacebar events."""
        self.setDisabled(False)
        self.setFocus(Qt.OtherFocusReason)

    def createButton(self, text, x, y, width, length):
        """Creates a new button."""
        self.button = QPushButton(text, self)
        self.button.setStyleSheet(
            "font-size: 24px;" + 
            "color: #462521;")
        self.button.setGeometry(x, y, width, length)
        self.button.clicked.connect(self.button_Click)
        self.button.show()

    def createRedoButton(self, text, x, y, width, length):
        """Creates a new button."""
        self.redo_button = QPushButton(text, self)
        self.redo_button.setStyleSheet(
            "font-size: 24px;" + 
            "color: #462521;")
        self.redo_button.setGeometry(x, y, width, length)
        self.redo_button.clicked.connect(self.redobutton_Click)
        self.redo_button.show()

    def createTextLabel(self, text, x, y, width, length):
        """Creates a new label."""
        self.text_label = QLabel(text, self)
        self.text_label.setStyleSheet(
            "font-size: 36px;" + 
            "color: #462521;")
        self.text_label.setGeometry(x, y, width, length)
        self.text_label.show()

    def clearView(self):
        """Hides all elements on the screen."""
        self.currentDot.hide()
        self.button.hide()
