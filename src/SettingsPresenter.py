class SettingsPresenter:

    """
    The SettingsPresenter class is responsible for handling the interactions between the SettingsModel and SettingsView classes.
    """

    def __init__(self, model, view):
        self.settingsmodel = model
        self.settingsview = view

        self.modifytext = "Modify settings"
        self.savetext = "Save changes"

        #self.settingsview.returnbuttonSignal.connect(self.handle_returnbutton)
        self.settingsview.save_button.setText(self.modifytext)
        #self.showCurrentValues()
        #self.settingsview.hideTextFields()

        self.settingsview.savebuttonSignal.connect(self.handle_savebutton)

    def showCurrentValues(self):
        """Shows the current value of each parameter."""
        self.settingsview.showCalDimensions(self.settingsmodel.calrows, self.settingsmodel.calcols)
        self.settingsview.showCalInterval(self.settingsmodel.calinterval)
        self.settingsview.showCalSamples(self.settingsmodel.samples)
        self.settingsview.showValDimensions(self.settingsmodel.valrows, self.settingsmodel.valcols)
        self.settingsview.showImgInterval(self.settingsmodel.imginterval)

    def handle_savebutton(self): 
        """Either makes text input fields appear or saves the values entered in the fields."""
        if self.settingsview.save_button.text() == self.modifytext:
            print(self.settingsview.save_button.text())
            self.settingsview.showTextFields()
            self.settingsview.save_button.setText(self.savetext)
            print(self.settingsview.save_button.text())
        elif self.settingsview.save_button.text() == self.savetext:
            self.saveSettings()
            self.settingsview.save_button.setText(self.modifytext)
            self.settingsview.hideTextFields()
            self.showCurrentValues()
            print("Current calows: {}, calcols: {}".format(self.settingsmodel.calrows, self.settingsmodel.calcols))

    def saveSettings(self):
        """Saves the entered values to the settings model."""
        calrows, calcols = self.settingsview.getCalDimensions()
        self.settingsmodel.setCalibrationRows(calrows)
        self.settingsmodel.setCalibrationColumns(calcols)

        calinterval = self.settingsview.getCalInterval()
        self.settingsmodel.setCalInterval(calinterval)

        samples = self.settingsview.getCalSamples()
        self.settingsmodel.setSamples(samples)

        valrows, valcols = self.settingsview.getValDimensions()
        self.settingsmodel.setValidationRows(valrows)
        self.settingsmodel.setValidationColumns(valcols)

        imginterval = self.settingsview.getImageInterval()
        self.settingsmodel.setImgInterval(imginterval)
        print("Saved new settings")

    def getCalibrationParameters(self):
        """Returns the values needed to initialize a CalibrationWindow."""
        row = self.settingsmodel.calrows
        col = self.settingsmodel.calcols
        interval = self.settingsmodel.calinterval
        samples = self.settingsmodel.samples
        return row, col, interval, samples
    
    def getValidationParameters(self):
        """Returns the values needed to intialize a CalibrationWindow."""
        row = self.settingsmodel.valrows
        col = self.settingsmodel.valcols
        return row, col
    
    def getImageInterval(self):
        """Returns the duration that each image is displayed on the screen for."""
        return self.settingsmodel.imginterval