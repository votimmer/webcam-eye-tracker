import cv2
import mediapipe as mp
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from IrisDetector import IrisDetector

class Webcam(QThread):

    """
    The Webcam class handles webcam-related functionalities. 
    It uses OpenCV and the IrisDetector class to access the webcam, detect and mark a person's irises, and display the webcam feed with the irises marked.
    """

    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

        self.all_webcams = self.findAllWebcams()

        if not self.noWebcams(): #if at least one webcam is connected
            self.video_source = len(self.all_webcams) - 1
            self.webcam = cv2.VideoCapture(self.video_source)
        
        self.iris_detector = IrisDetector()
    
    def findAllWebcams(self):
        """Finds all available webcams."""
        webcams = []
        i = 0
        is_working = True
        while is_working:
            webcam = cv2.VideoCapture(i)
            if webcam.isOpened():
                webcams.append(i)
                i += 1
            else:
                is_working = False
        print("Indexes of webcam sources found: {}".format(webcams))
        return webcams
    
    def noWebcams(self):
        """Returns whether there are zero webcams available."""
        return len(self.all_webcams) == 0

    def detectIris(self):
        """Detects a person's irises."""
        success, image = self.webcam.read()
        image, l_cx, l_cy, r_cx, r_cy = self.iris_detector.detectIris(image)
        return (l_cx, l_cy), (r_cx, r_cy)

    def run(self):
        """Displays webcam feed with the irises of a person marked."""
        while self._run_flag:
            success, image = self.webcam.read()
            if not success:
                break

            image,lc, lcc, rc, rcc = self.iris_detector.detectIris(image)
            #image,lc, lcc, rc, rcc = self.detectIris()
            #print(lc, lcc, rc, rcc)
            self.change_pixmap_signal.emit(image)
            #cv2.imshow("Webcam eye tracker", image)
            if cv2.waitKey(10) and 0xFF == ord('q'):
                break

        self.webcam.release()
        cv2.destroyAllWindows()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

if __name__ == "__main__":
    webcam = Webcam()
    webcam.run()