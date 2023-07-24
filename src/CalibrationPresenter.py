import random
from PyQt5.QtCore import QTimer

class CalibrationPresenter:

    """
    The CalibrationPresenter class is responsible for handling the interactions between the CalibrationModel and CalibrationView classes.
    """

    def __init__(self, calibrationmodel, calibrationview):
        self.calmodel = calibrationmodel
        self.calview = calibrationview
        print(self.calmodel.unvisited)
        self.calview.spacebarSignal.connect(self.handle_spacebar)
        self.dot_coordinates = []
        self.distances = [] 
        self.trainedmodel = None 
        self.timer_tick = 0
        self.eye_timer = None
        self.current_gaze_location = []

    def handle_spacebar(self):
        """Handles actions that should be triggered when the spacebar is pressed."""
        if self.calmodel.checkAllVisited(): 
            if self.calmodel.mode == 'c':
                self.createButton("Calibration complete. Continue to validation")
                dataframe = self.calmodel.averageIrisPositions()
                self.trainedmodel = self.calmodel.train(dataframe)
            if self.calmodel.mode == 'v':
                self.calculateAverageDistance(self.calview.currentDot)
                self.eye_timer.stop()
                self.calmodel.webcam.webcam.release()
                self.createButton("Go to image viewing task")
                self.createRedoButton("Redo calibration")
                average_distance = self.calmodel.calculateAverageDistance(self.distances)
                self.createTextLabel("Validation complete, mean error is: {} px".format(average_distance))
            print("All cells have been visited")
            return
        
        #Get currentdot
        prev = self.calview.currentDot
        self.calview.hideDot(prev)

        #Get unvisited cells
        unvisited = self.calmodel.unvisited

        #Select random cell
        currCell = random.choice(unvisited)
        print("Current cell is: {}".format(currCell))
        self.dot_coordinates.append(currCell)

        #Create dot at that position
        self.calview.createDot(currCell)

        if self.calmodel.mode == 'c':
            self.calmodel.collectSamples(self.calmodel.samples, currCell)
            self.calview.countdown(self.calmodel.interval)
        if self.calmodel.mode == 'v':
            if prev is not None:
                self.calculateAverageDistance(prev)

        #Visit the selected cell 
        self.calmodel.visitCell(currCell)
    
    def setModelMode(self, mode):
        """Sets the mode (calibration or validation) of the window."""
        self.calmodel.setMode(mode)

    def getTrainedModel(self):
        """Returns the trained regression model."""
        return self.trainedmodel
    
    def setTrainedModel(self, regression_model):
        """Sets the trained model to be equal to the given trained regression model."""
        self.trainedmodel = regression_model

    def estimateGaze(self):
        """Estimates the gaze location."""
        location = self.calmodel.estimate_gaze_location(self.trainedmodel)
        self.current_gaze_location.append(location)
        return location
    
    def calculateAverageDistance(self, prev):
        """Calculates the average distance between a validation point and the predicted gaze location in pixels."""
        gaze_distances = []
        prev_x = prev.x()
        prev_y = prev.y()
        last_few = self.current_gaze_location[-10:] #last ten gaze estimates for the current validation point

        #Calculates euclidean distances 
        for location in last_few:
            distance = self.calmodel.calculateDistance((prev_x, prev_y), location[0])
            gaze_distances.append(distance)
        
        average = self.calmodel.calculateAverageDistance(gaze_distances) #Calculates average euclidean distance
        self.distances.append(average)
        self.current_gaze_location = []
        print(gaze_distances)

    def trackEyes(self):
        """Starts a timer that updates the eye cursor with 60 fps."""
        self.calview.createEyeCursor()
        self.eye_timer = QTimer()
        self.eye_timer.timeout.connect(self.update_eye_cursor)
        self.eye_timer.start(16)  #Update every 16 milliseconds (60 FPS)

    def update_eye_cursor(self):
        """Moves the dot that follows the eyes to the right location on the screen."""
        self.timer_tick += 1
        if self.timer_tick % 4 == 0:
            location = self.estimateGaze()
            self.calview.moveEyeCursor(location[0]) 

    def stopEyeTracking(self):
        """Stops the eye tracker from updating."""
        self.eye_timer.stop()

    def createButton(self, text):
        """Creates a button with the given text."""
        x = (self.calmodel.window_w / 2) - 250
        y = (self.calmodel.window_h / 2) - 100
        self.calview.createButton(text, x, y, 500, 150)

    def createRedoButton(self, text):
        """Creates a button with the given text. The button connects to the calibration window."""
        x = (self.calmodel.window_w / 2) - 250
        y = (self.calmodel.window_h / 2) + 100
        self.calview.createRedoButton(text, x, y, 500, 150)

    def createTextLabel(self, text):
        """Creates a label with the given text."""
        x = (self.calmodel.window_w / 2) - 310
        y = (self.calmodel.window_h / 2) -300
        self.calview.createTextLabel(text, x, y, 1500, 300)
