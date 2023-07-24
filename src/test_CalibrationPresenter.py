import pytest
from unittest.mock import MagicMock
from CalibrationPresenter import CalibrationPresenter

@pytest.fixture
def mock_calibration_model():
    calibration_model = MagicMock()
    calibration_model.row = 2
    calibration_model.col = 2
    calibration_model.interval = 1500
    calibration_model.window_w = 1920
    calibration_model.window_h = 1080
    calibration_model.visited = []
    calibration_model.unvisited =[(270, 480), (270, 1440), (810, 480), (810, 1440)]
    calibration_model.output_file = None
    calibration_model.webcam = MagicMock()
    calibration_model.mode = 'c'
    calibration_model.createFile().return_value = None

    return calibration_model

@pytest.fixture
def mock_calibration_view():
    calibration_view = MagicMock()
    calibration_view.visited = [] #contains the cells that the visual marker has inhabited 
    calibration_view.currentDot = None #dot that is currently visible
    calibration_view.eyeCursor = None 
    calibration_view.button = None
    calibration_view.redo_button = None
    calibration_view.text_label = None

    return calibration_view

@pytest.fixture
def calibration_presenter(mock_calibration_model, mock_calibration_view):
    presenter = CalibrationPresenter(mock_calibration_model, mock_calibration_view)
    return presenter

@pytest.fixture
def mock_trainedmodel():
    trainedmodel = MagicMock()
    return trainedmodel 

def test_handle_spacebar_NotAllVisited_hideDot(calibration_presenter, mock_calibration_model, mock_calibration_view):
    mock_calibration_model.checkAllVisited = MagicMock(return_value=False)
    mock_calibration_model.unvisited = [(0,0), (0,1), (1,0)]
    prev = MagicMock()
    mock_calibration_view.currentDot = prev
    calibration_presenter.handle_spacebar()
    mock_calibration_view.hideDot.assert_called_once_with(prev)

def test_handle_spacebar_NotAllVisited_createDot(calibration_presenter, mock_calibration_model, mock_calibration_view):
    mock_calibration_model.checkAllVisited = MagicMock(return_value=False)
    mock_calibration_model.unvisited = [(0,0)]
    prev = MagicMock()
    mock_calibration_view.currentDot = prev
    currCell = (0,0)
    calibration_presenter.handle_spacebar()
    mock_calibration_view.createDot.assert_called_once_with(currCell)

def test_setModelMode(calibration_presenter, mock_calibration_model):
    calibration_presenter.setModelMode('v')
    mock_calibration_model.setMode.assert_called_once_with('v')

def test_getTrainedModel(calibration_presenter, mock_trainedmodel):
    calibration_presenter.trainedmodel = mock_trainedmodel
    assert calibration_presenter.getTrainedModel() == mock_trainedmodel 

def test_setTrainedModel(calibration_presenter, mock_trainedmodel):
    calibration_presenter.setTrainedModel(mock_trainedmodel)
    assert calibration_presenter.trainedmodel == mock_trainedmodel

def test_estimateGaze_model_called(calibration_presenter, mock_calibration_model, mock_trainedmodel):
    """Tests whether the estimate_gaze_location of the model is called."""
    calibration_presenter.trainedmodel = mock_trainedmodel
    location = [(50, 120)]
    mock_calibration_model.estimate_gaze_location = MagicMock(return_value=location)
    calibration_presenter.estimateGaze()
    mock_calibration_model.estimate_gaze_location.assert_called_once_with(mock_trainedmodel)

def test_estimateGaze_location(calibration_presenter, mock_calibration_model, mock_trainedmodel):
    """Tests whether the presenter finds the same gaze estimate as the model."""
    calibration_presenter.trainedmodel = mock_trainedmodel
    location = [(50, 120)]
    mock_calibration_model.estimate_gaze_location = MagicMock(return_value=location)
    assert calibration_presenter.estimateGaze() == location

def test_trackEyes_eyetimer(calibration_presenter):
    calibration_presenter.trackEyes()
    assert calibration_presenter.eye_timer is not None

def test_trackEyes_eyecursor(calibration_presenter, mock_calibration_view): 
    calibration_presenter.trackEyes()
    mock_calibration_view.createEyeCursor.assert_called_once()

def test_update_eye_cursor(calibration_presenter, mock_trainedmodel, mock_calibration_view): 
    calibration_presenter.timer_tick = 3
    calibration_presenter.trainedmodel = mock_trainedmodel
    location = [(50, 120)]
    calibration_presenter.estimateGaze = MagicMock(return_value=location)
    calibration_presenter.update_eye_cursor()
    mock_calibration_view.moveEyeCursor.assert_called_once_with(location[0]) 

def test_stopEyeTracking(calibration_presenter):
    calibration_presenter.eye_timer = MagicMock()
    calibration_presenter.stopEyeTracking()
    calibration_presenter.eye_timer.stop.assert_called_once()

def test_createButton(calibration_presenter, mock_calibration_view, mock_calibration_model): 
    text = "test"
    x = (mock_calibration_model.window_w)/2 - 250
    y = (mock_calibration_model.window_h)/2 - 100
    calibration_presenter.createButton(text)
    mock_calibration_view.createButton.assert_called_once_with(text, x, y, 500, 150)

def test_createRedoButton(calibration_presenter, mock_calibration_view, mock_calibration_model): 
    text = "test"
    x = (mock_calibration_model.window_w)/2 - 250
    y = (mock_calibration_model.window_h)/2 + 100
    calibration_presenter.createRedoButton(text)
    mock_calibration_view.createRedoButton.assert_called_once_with(text, x, y, 500, 150)

def test_createTextLabel(calibration_presenter, mock_calibration_view, mock_calibration_model):
    text = "test"
    x = (mock_calibration_model.window_w)/2 - 310
    y = (mock_calibration_model.window_h)/2 - 300
    calibration_presenter.createTextLabel(text)
    mock_calibration_view.createTextLabel.assert_called_once_with(text, x, y, 1500, 300)

