from SettingsModel import SettingsModel
from SettingsPresenter import SettingsPresenter
from SettingsView import SettingsView
from PyQt5.QtWidgets import QApplication, QDesktopWidget
import PyQt5.QtWidgets as QtWidgets
import sys

class SettingsWindow(QtWidgets.QMainWindow):

    """
    The SettingsWindow class sets up the GUI for the settings window by combining the SettingsModel, SettingsView, and SettingsPresenter classes.
    """

    def __init__(self):
        super().__init__()

        settingsmodel = SettingsModel()
        settingsview = SettingsView()
        self.settingspresenter = SettingsPresenter(settingsmodel, settingsview)
        self.settingspresenter.showCurrentValues()
        self.settingspresenter.settingsview.hideTextFields()
        self.setCentralWidget(settingsview)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = SettingsWindow()
    #print("start")
    ui.showMaximized()
    sys.exit(app.exec_())