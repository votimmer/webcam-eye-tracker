import math
import os
from datetime import datetime
import csv
from Webcam import Webcam

class ImagesModel:

    """
    The ImagesModel class is used for tracking a person's gaze while looking at images. 
    It saves the gaze data collected during the image viewing task in a CSV file.
    """

    def __init__(self, interval, webcam=None):
        self.interval = interval
        self.images = []
        self.output_file = None
        self.createFile()
        self.webcam = Webcam()
        self.regression_model = None

    def setRegressionModel(self, regression_model):
        """Sets the regression model to be used."""
        self.regression_model = regression_model

    def populate_image_list(self, folder_path):
        """Fills a list with image paths."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file)[-1].lower() in image_extensions:
                    self.images.append(os.path.join(root, file))

    def createFile(self):
        """Creates a new csv file with the current datetime as name."""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # Create the file name with the timestamp
        file_name = f"images_{timestamp}.csv"
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Image', 'Gaze location x', 'Gaze location y'])
        self.output_file = file_name

    def writeToFile(self, imgpath, gaze_x, gaze_y):
        """Writes the coordinates of the calibration point, center of left iris and center of right iris to a text file."""
        #Open the file in append mode
        with open(self.output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([imgpath, gaze_x, gaze_y])

    def detectIrises(self):
        """Detects the centers of the left and right irises."""
        return self.webcam.detectIris()
        
    def estimate_gaze_location(self, ridge_model):
        """Estimates the gaze location based on the prediction made by the regression model."""
        left_iris, right_iris = self.detectIrises()
        distance = math.sqrt(((left_iris[0] - right_iris[0])**2) + ((left_iris[1] - right_iris[1])**2))
        input_features = (left_iris[0], left_iris[1], right_iris[0], right_iris[1], distance)

        #Predict gaze location using the trained model
        gaze_location = ridge_model.predict([input_features])
        #print("predicted location: {}".format(gaze_location[0]))
        return gaze_location
