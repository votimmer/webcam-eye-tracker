import cv2 as cv

class SettingsModel:

    """
    The SettingsModel class is responsible for managing and storing various settings related to the eye-tracking and calibration process. 
    It provides methods to set and update different values based on user input.
    """

    def __init__(self):
        self.permission = False
        self.calrows = 3
        self.calcols = 3
        self.calinterval = 1500
        self.samples = 50
        self.valrows = 4
        self.valcols = 4
        self.imginterval = 1500

    def askPermission(self, permission):
        """Saves whether user gave permission to access webcam.""" 
        self.permission = permission
        return permission
        
    def setCalibrationRows(self, row):
        """Sets the number of rows the calibration grid should contain."""
        try:
            if row.isnumeric():
                row = int(row)
                if row < 2 or row > 10:
                    print("Row value must be equal to or larger than 2 and equal to or smaller than 10")
                    return -1
                self.calrows = row
                return self.calrows
            else:
                print("Input must be a whole number.")
                return -1
        except:
            print("Invalid input, input must be a whole number.")
            return -1
        
    def setCalibrationColumns(self, col): 
        """Sets the number of columns the calibration grid should contain."""
        try:
            if col.isnumeric():
                col = int(col)
                if col < 2 or col > 10:
                    print("Column value must be equal to or larger than 2 and equal to or smaller than 10")
                    return -1
                self.calcols = col
                return self.calcols
            else:
                return -1
        except:
            print("Invalid input. Please enter a whole number.")
            return -1
        
    def setValidationRows(self, row):
        """Sets the number of rows the validation grid should contain."""
        try:
            if row.isnumeric():
                row = int(row)
                if row < 1 or row > 10:
                    print("Row value must be equal to or larger than 1 and equal to or smaller than 10")
                    return -1
                self.valrows = row
                return self.valrows
            else:
                return -1
        except:
            print("Invalid input")
            return -1
        
    def setValidationColumns(self, col):
        """Sets the number of columns the validation grid should contain."""
        try:
            if col.isnumeric():
                col = int(col)
                if col < 1 or col > 10:
                    print("Column value must be equal to or larger than 1 and equal to or smaller than 10")
                    return -1
                self.valcols = col
                return self.valcols
            else:
                return -1
        except:
            print("Invalid input")
            return -1
    
    def setCalInterval(self, interval):
        """Saves the duration during which a single calibration point is shown (in milliseconds)."""
        try:
            if interval.isnumeric():
                interval = int(interval)
                if interval < 500:
                    print("Interval must be larger than or equal to 500 ms")
                    return -1
                self.calinterval = interval
                return interval
            else:
                return -1
        except:
            print("Invalid input")
            return -1

    def setSamples(self, num): 
        """Saves the number of image samples that are taken for each calibration point."""
        try:
            if num.isnumeric():
                num = int(num)
                if num <= 0:
                    print("Number of samples must be larger than 0")
                    return -1
                self.samples = num
                return num
            else:
                return -1
        except:
            print("Invalid input")
            return -1
    
    def setImgInterval(self, interval):
        """Saves the duration during which a single image is shown (in milliseconds)."""
        try:
            if interval.isnumeric():
                interval = int(interval)
                if interval < 250:
                    print("Interval must be larger than or equal to 250 ms")
                    return -1
                self.imginterval = interval
                return interval
            else:
                return -1
        except:
            print("Invalid input")
            return -1
    
