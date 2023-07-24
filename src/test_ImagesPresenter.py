import pytest
from unittest.mock import MagicMock
from ImagesPresenter import ImagesPresenter

@pytest.fixture
def mock_images_model():
    images_model = MagicMock()
    images_model.images = []
    images_model.interval = 1500
    images_model.regression_model = MagicMock()
    return images_model

@pytest.fixture
def mock_images_view():
    images_view = MagicMock()
    return images_view

@pytest.fixture
def images_presenter(mock_images_model, mock_images_view):
    presenter = ImagesPresenter(mock_images_model, mock_images_view)
    return presenter

def test_update_view_getFolder(images_presenter, mock_images_view):
    images_presenter.update_view()
    mock_images_view.getFolder.assert_called_once()

def test_update_view_showImages(images_presenter, mock_images_view, mock_images_model):
    mock_images_model.images.append("test.png")
    test = "Folder"
    mock_images_view.getFolder = MagicMock(return_value=test)
    images_presenter.update_view()
    mock_images_view.showImages.assert_called_once_with(mock_images_model.images, mock_images_model.interval)

def test_update_view_createButton(images_presenter, mock_images_view):
    test = "Folder"
    mock_images_view.getFolder = MagicMock(return_value=test)
    images_presenter.update_view()
    mock_images_view.createButton.assert_called_once_with(images_presenter.invalid_folder_text)

def test_update_view_populate_img_list(images_presenter, mock_images_model, mock_images_view):
    test = "Folder"
    mock_images_view.getFolder = MagicMock(return_value=test)
    images_presenter.update_view()
    mock_images_model.populate_image_list.assert_called_once_with(test)

def test_update_view_no_folder(images_presenter, mock_images_view):
    mock_images_view.getFolder = MagicMock(return_value=None)
    images_presenter.update_view()
    mock_images_view.createButton.assert_called_once_with(images_presenter.no_folder_text)

def test_track_gaze_getCurrentImage(images_presenter, mock_images_view): 
    images_presenter.track_gaze()
    mock_images_view.getCurrentImage.assert_called_once()


