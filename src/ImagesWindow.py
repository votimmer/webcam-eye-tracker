from ImagesModel import ImagesModel
from ImagesView import ImagesView
from ImagesPresenter import ImagesPresenter
from PyQt5.QtWidgets import QApplication, QDesktopWidget
import PyQt5.QtWidgets as QtWidgets
import sys

class ImagesWindow(QtWidgets.QMainWindow):

    """
    The ImagesWindow class sets up the GUI for the image viewing task by combining the ImagesModel, ImagesView, and ImagesPresenter classes.
    """

    def __init__(self, interval):
        super().__init__()

        imgmodel = ImagesModel(interval)
        imgview = ImagesView()
        self.imgpresenter = ImagesPresenter(imgmodel, imgview)

        self.window = QtWidgets.QMainWindow()
        self.setCentralWidget(imgview)
        self.setWindowTitle("Webcam Eye-tracking")
        self.setMinimumSize(1280, 920)
        self.showMaximized()
        self.imgpresenter.update_view()
        #self.setFixedSize(self.size())
        self.activateWindow()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ImagesWindow(1500)
    #ui.imgpresenter.update_view
    print("start")
    ui.show()
    sys.exit(app.exec_())