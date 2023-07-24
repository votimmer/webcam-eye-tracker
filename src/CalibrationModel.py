from datetime import datetime
import csv
import math
from Webcam import Webcam
from PyQt5.QtCore import QTimer
from sklearn.linear_model import Ridge
import pandas as pd


class CalibrationModel:

    """
    The CalibrationModel class is used to calibrate and validate eye-tracking systems. 
    It estimates where a person is looking on a computer screen by using the positions of their left and right irises detected from a webcam. 
    The class divides the screen into sections for calibration, records iris positions, and uses them to train a model. 
    This model can then predict the person's gaze location.
    """
    
    def __init__(self, row, col, interval, window_w, window_h, mode):
        self.row = row
        self.col = col 
        self.interval = interval
        self.samples = 50 #default value
        self.window_w = window_w #width of the window in pixels
        self.window_h = window_h #height of the window in pixels
        self.visited = [] #contains the cells that have been visited by the calibration point
        self.unvisited = self.divideScreen()
        self.output_file = None
        self.webcam = Webcam()
        self.mode = mode
        if self.mode == 'c':
            self.createFile()

    def setWindowDimensions(self, window_w, window_h):
        """Sets the screen dimensions."""
        self.window_h = window_h
        self.window_w = window_w

    def setMode(self, mode):
        """Sets the mode of the window."""
        if mode == 'c' or mode == 'v': #c = calibration, v = validation
            self.mode = mode
        else:
            print("Invalid input, mode must be c or v.")

    def setSamples(self, samples):
        """Sets the number of samples taken at each calibration point."""
        self.samples = samples

    def divideScreen(self):
        """Divides the screen into a row x col grid and saves the center of each cell in a list."""
        try:
            cell_h = self.window_h / self.row #height of a single grid cell
            cell_w = self.window_w / self.col #width of a single grid cell
            list_h = []
            list_w = []
            for i in range(self.row):
                center = (cell_h / 2) + (i*cell_h)
                list_h.append(center)
            for j in range(self.col):
                center = (cell_w / 2) + (j*cell_w)
                list_w.append(center)
            list_cells = [(x, y) for x in list_w for y in list_h]
            return list_cells
        except ZeroDivisionError:
            print("Can't divide by zero.")
    
    def visitCell(self, cell):
        """Removes a cell from the list of unvisited cells and appends it to the list of visited cells."""
        try:
            self.visited.append(cell)
            self.unvisited.remove(cell)
            
        except:
            print("Cell doesn't exist")

    def checkAllVisited(self):
        """Checks if all cells have been visited by the calibration point."""
        try:
            return len(self.unvisited) == 0 #True if all cells have been visited, False otherwise
        except TypeError:
            print("The list containing unvisited cells does not exist.")
    
    def createFile(self):
        """Creates a new csv file with the current datetime as name."""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        #Create the file name with the timestamp
        file_name = f"data_{timestamp}.csv"
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Dot location x', 'Dot location y', 
                             'Left eye x-coordinates', 'Left eye y-coordinates', 
                             'Right eye x-coordinates', 'Right eye y-coordinates',
                             'Iris Distance'])
            
        self.output_file = file_name

    def writeToFile(self, dotpos, lefteye, righteye, distance):
        """Writes the coordinates of the calibration point, center of left iris and center of right iris to a text file."""
        #Open the file in append mode
        with open(self.output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([dotpos[0], dotpos[1], lefteye[0], lefteye[1], righteye[0], righteye[1], distance])

    def detectIrises(self):
        """Detects the centers of the left and right irises."""
        return self.webcam.detectIris()
        
    def writeIrises(self, dotpos):
        """Writes iris coordinates to a CSV file."""
        left, right = self.detectIrises()
        distance = self.calculateDistance(left, right) #calculates distance between left and right eye
        self.writeToFile(dotpos, left, right, distance)

    def calculateDistance(self, actual, predicted):
        """Calculates the euclidean distance between the center of a validation point and predicted gaze location."""
        dist = math.sqrt(((predicted[0] - actual[0])**2) + ((predicted[1] - actual[1])**2))
        return dist
    
    def calculateAverageDistance(self, distances):
        """Calculates the average euclidean distance between the predicted points and actual locations."""
        if len(distances) > 0:
            average_distance = sum(distances) / len(distances)
            return round(average_distance, 2) 
        else:
            print("No euclidean distances were saved, the list is empty.")


    def collectSamples(self, samples, dotpos): 
        """Records the positions of the left eye and right eye 'samples' number of times for each calibration point and writes them to a CSV file."""
        try:
            self.remaining_samples = samples  
            timer = QTimer()

            #Writes iris positions to the CSV file for each calibration point
            def timerCallback():
                self.writeIrises(dotpos)
                self.remaining_samples -= 1
                if self.remaining_samples <= 0:
                    timer.stop()

            timer.timeout.connect(timerCallback)
            timerinterval = self.interval / samples
            timer.setInterval(timerinterval)
            timer.start()
        except ZeroDivisionError:
            print("Samples must be larger than 0")

    def averageIrisPositions(self):
        """Calculates the average iris positions for each calibration marker."""
        dataframe = pd.read_csv(self.output_file)
        grouped_dots = dataframe.groupby(['Dot location x', 'Dot location y'])[['Left eye x-coordinates', 'Left eye y-coordinates', 
                                                                                'Right eye x-coordinates', 'Right eye y-coordinates',
                                                                                'Iris Distance']].mean()
        grouped_dots.reset_index(inplace=True)
        print(grouped_dots)
        return grouped_dots
    
    def train(self, dataframe):
        """Trains a ridge regression model using the average iris positions."""
        X = dataframe[['Left eye x-coordinates', 'Left eye y-coordinates', 
                       'Right eye x-coordinates', 'Right eye y-coordinates', 
                       'Iris Distance']]
        y = dataframe[['Dot location x', 'Dot location y']]

        ridge_model = Ridge(alpha=1.0)
        ridge_model.fit(X,y)
        return ridge_model

    def estimate_gaze_location(self, ridge_model):
        """Estimates the gaze location based on the prediction made by the regression model."""
        left_iris, right_iris = self.detectIrises()
        distance = self.calculateDistance(left_iris, right_iris)
        input_features = (left_iris[0], left_iris[1], right_iris[0], right_iris[1], distance)

        #Predict gaze location using the trained model
        gaze_location = ridge_model.predict([input_features])
        print("predicted location: {}".format(gaze_location[0]))
        return gaze_location
