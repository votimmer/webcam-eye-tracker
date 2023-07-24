from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication, QGridLayout, QLabel, QPushButton, QDesktopWidget
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap

class ImagesView(QWidget):

    """
    The ImagesView class is responsible for managing the GUI components of the image viewing task.
    """

    imageSignal = QtCore.pyqtSignal()
    buttonSignal = QtCore.pyqtSignal()

    def __init__ (self):
        super().__init__()
        self.current_img = None
        self.button = None
        screen_geometry = QDesktopWidget().screenGeometry()
        self.screen_width = screen_geometry.width() - 50
        self.screen_height = screen_geometry.height() - 100

        self.grid = QGridLayout(self)
        self.setWindowTitle("Webcam Eye-tracking")
        self.setMinimumSize(1280, 920)
        self.createImageBorder()

    def newImage(self, imgpath): 
        """Sends a signal when a new image is shown."""
        self.createLabel(imgpath)
        self.current_img = imgpath
        self.imageSignal.emit()
        #print("New image")

    def getCurrentImage(self):
        """Returns the path of the image currently being shown."""
        return self.current_img

    def getFolder(self):
        """Returns the path of the selected  folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        return folder
    
    def button_Click(self):
        """Emits a signal when the button is pressed."""
        self.buttonSignal.emit()
    
    def createButton(self, text):
        """Creates a button"""
        self.button = QPushButton(text)
        self.button.setFixedSize(500, 150)
        #self.button.setAlignment(Qt.AlignCenter)
        self.button.clicked.connect(self.button_Click)
        self.grid.addWidget(self.button, 1, 1, Qt.AlignCenter)

    def hideButton(self):
        """Hides a button"""
        self.button.hide()

    def createImageBorder(self):
        """Creates widget that contain the image label."""
        imgborder = QWidget()
        imgborder.setStyleSheet("background: black;")
        imgborder.setFixedSize(self.screen_width, self.screen_height)
        self.grid.addWidget(imgborder, 1, 1, Qt.AlignCenter)
        return imgborder

    def createLabel(self, imgpath):
        """Creates label in which the given image will be displayed."""
        imglabel = QLabel()
        imglabel.setStyleSheet("background: black;")
        imglabel.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(imgpath)
        pixmap = self.checkSize(pixmap)
        imglabel.setPixmap(pixmap)
        self.grid.addWidget(imglabel, 1, 1)
        return imglabel

    def showImages(self, images, interval):
        """Displays the given images on the screen for interval milliseconds."""
        for i, img in enumerate(images):
                timer = QtCore.QTimer(self)
                timer.setSingleShot(True)
                timer.timeout.connect(lambda i=i: self.newImage(images[i]))
                timer.start(interval * i)
   
    def checkSize(self, img):
        """Checks whether an image is too small, if it is then the image is made larger."""
        if img.height() < 250 or img.width() < 250: #dit gedeelte kan als functie binnen imagesmodel geimplementeerd worden
            print("too small")
            img = img.scaled(QSize(255,255), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            print("h: " + str(img.height()) + ", w: " + str(img.width()))
        if img.height() > self.screen_height or img.width() > self.screen_width:
             img = img.scaled(QSize(self.screen_width - 10, self.screen_height - 10), Qt.KeepAspectRatio)
        return img
    
    def createDot(self, cell): 
        """Creates a dot that will serve as the visual marker in a calibration phase."""
        dot = QLabel(self)
        dot_size = 20
        dot.setFixedSize(dot_size, dot_size)
        dot.setStyleSheet(
            "background: blue;" + 
            "border-radius: 10px;"
            )
        dot.move(cell[0], cell[1])
        dot.show()

