from PyQt5.QtCore import QTimer

class ImagesPresenter:

    """
    The ImagesPresenter class is responsible for handling the interactions between the ImagesModel and ImagesView classes.
    """

    def __init__(self, imagesmodel, imagesview):
        self.imagesmodel = imagesmodel
        self.imagesview = imagesview
        self.imagesview.imageSignal.connect(self.track_gaze)
        self.imagesview.buttonSignal.connect(self.handle_button_click)

    def update_view(self):
        """Updates the view by showing images in a selected folder."""
        self.no_folder_text = "No folder selected"
        self.invalid_folder_text = "Invalid folder selected."
        folder = self.imagesview.getFolder()
        if folder:
            self.imagesmodel.populate_image_list(folder)
            #print(self.imagesmodel.images)
            if len(self.imagesmodel.images) == 0: #if no valid images are present in the selected folder
                self.imagesview.createButton(self.invalid_folder_text)
                print(self.invalid_folder_text)
            else: 
                self.imagesview.showImages(self.imagesmodel.images, self.imagesmodel.interval)
        else: #if no folder was selected
            self.imagesview.createButton(self.no_folder_text)
            print(self.no_folder_text)

    def handle_button_click(self):
        """Hides the button and asks user to select a folder again."""
        self.imagesview.hideButton()
        self.update_view()

    def estimate_gaze(self, imgpath, count=10):
        """Estimates the gaze of a person looking at an image. Gaze data is recorded ten times for each image."""
        if count > 0: 
            gaze_location = self.imagesmodel.estimate_gaze_location(self.imagesmodel.regression_model)
            pos = gaze_location[0]
            self.imagesview.createDot(pos)
            self.imagesmodel.writeToFile(imgpath, pos[0], pos[1])
            count -= 1
            QTimer.singleShot(self.imagesmodel.interval // 10, lambda: self.estimate_gaze(imgpath, count))

    def track_gaze(self):
        """Tracks the gaze of a person looking at an image."""
        imgpath = self.imagesview.getCurrentImage()
        self.estimate_gaze(imgpath, count=10)
