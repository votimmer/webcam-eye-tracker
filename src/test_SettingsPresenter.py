import pytest
from unittest.mock import MagicMock
from SettingsPresenter import SettingsPresenter

@pytest.fixture
def mock_settings_model():
    model = MagicMock()
    model.calrows = 3
    model.calcols = 3
    model.calinterval = 1500
    model.samples = 50
    model.valrows = 4
    model.valcols = 4
    model.imginterval = 1500
    return model

@pytest.fixture
def mock_settings_view():
    view = MagicMock()
    return view

@pytest.fixture
def settings_presenter(mock_settings_model, mock_settings_view):
    presenter = SettingsPresenter(mock_settings_model, mock_settings_view)
    return presenter

def test_showCurrentValues_showCalDimensions(settings_presenter, mock_settings_model, mock_settings_view):
    settings_presenter.showCurrentValues()
    mock_settings_view.showCalDimensions.assert_called_once_with(mock_settings_model.calrows, mock_settings_model.calcols)  

def test_showCurrentValues_showCalInterval(settings_presenter, mock_settings_model, mock_settings_view):
    settings_presenter.showCurrentValues()
    mock_settings_view.showCalInterval.assert_called_once_with(mock_settings_model.calinterval)

def test_showCurrentValues_showCalSamples(settings_presenter, mock_settings_model, mock_settings_view):
    settings_presenter.showCurrentValues()
    mock_settings_view.showCalSamples.assert_called_once_with(mock_settings_model.samples)

def test_showCurrentValues_showValDimensions(settings_presenter, mock_settings_model, mock_settings_view):
    settings_presenter.showCurrentValues()
    mock_settings_view.showValDimensions.assert_called_once_with(mock_settings_model.valrows, mock_settings_model.valcols)

def test_showCurrentValues_showImgInterval(settings_presenter, mock_settings_model, mock_settings_view):
    settings_presenter.showCurrentValues()
    mock_settings_view.showImgInterval.assert_called_once_with(mock_settings_model.imginterval)

def test_getCalibrationParameters(settings_presenter, mock_settings_model):
    assert settings_presenter.getCalibrationParameters() == (mock_settings_model.calrows, mock_settings_model.calcols, 
                                                             mock_settings_model.calinterval, mock_settings_model.samples)

def test_getValidationParameters(settings_presenter, mock_settings_model):
    assert settings_presenter.getValidationParameters() == (mock_settings_model.valrows, mock_settings_model.valcols)

def test_getImageInterval(settings_presenter, mock_settings_model):
    assert settings_presenter.getImageInterval() == mock_settings_model.calinterval

#Tests for saveSettings()

def setUpViewGetters(mock_settings_view):
    """Sets up return values for the get methods of the view."""
    row, col = 2, 4
    mock_settings_view.getCalDimensions = MagicMock(return_value=(row, col))
    interval = 500
    mock_settings_view.getCalInterval = MagicMock(return_value=interval)
    samples = 10
    mock_settings_view.getCalSamples = MagicMock(return_value=samples)
    #valrow, valcol = 4, 5
    mock_settings_view.getValDimensions = MagicMock(return_value=(row, col))
    #imginterval = 1500
    mock_settings_view.getImageInterval = MagicMock(return_value=interval)
    return row, col, interval, samples

def test_saveSettings_calibration(settings_presenter, mock_settings_model, mock_settings_view):
    row, col, interval, samples = setUpViewGetters(mock_settings_view)

    settings_presenter.saveSettings()

    mock_settings_model.setCalibrationRows.assert_called_once_with(row)
    mock_settings_model.setCalibrationColumns.assert_called_once_with(col)

def test_saveSettings_validation(settings_presenter, mock_settings_model, mock_settings_view):
    row, col, interval, samples = setUpViewGetters(mock_settings_view)

    settings_presenter.saveSettings()

    mock_settings_model.setValidationRows.assert_called_once_with(row)
    mock_settings_model.setValidationColumns.assert_called_once_with(col) 

def test_saveSettings_calinterval(settings_presenter, mock_settings_model, mock_settings_view):
    row, col, interval, samples = setUpViewGetters(mock_settings_view)

    settings_presenter.saveSettings()

    mock_settings_model.setCalInterval.assert_called_once_with(interval)

def test_saveSettings_imginterval(settings_presenter, mock_settings_model, mock_settings_view):
    row, col, interval, samples = setUpViewGetters(mock_settings_view)

    settings_presenter.saveSettings()

    mock_settings_model.setImgInterval.assert_called_once_with(interval)

def test_saveSettings_samples(settings_presenter, mock_settings_model, mock_settings_view):
    row, col, interval, samples = setUpViewGetters(mock_settings_view)

    settings_presenter.saveSettings()

    mock_settings_model.setSamples.assert_called_once_with(samples) 

#Tests for handle_savebutton()

def test_handle_savebutton_showTextFields(settings_presenter, mock_settings_view):
    mock_settings_view.save_button = MagicMock()
    mock_settings_view.save_button.text = MagicMock(return_value=settings_presenter.modifytext)
    settings_presenter.handle_savebutton()
    mock_settings_view.showTextFields.assert_called_once()

def test_handle_savebutton_set_savetext(settings_presenter, mock_settings_view):
    mock_settings_view.save_button = MagicMock()
    mock_settings_view.save_button.text = MagicMock(return_value=settings_presenter.modifytext)
    settings_presenter.handle_savebutton()
    mock_settings_view.save_button.setText.assert_called_once_with(settings_presenter.savetext)

def test_handle_savebutton_hideTextFields(settings_presenter, mock_settings_view):
    setUpViewGetters(mock_settings_view)
    mock_settings_view.save_button = MagicMock()
    mock_settings_view.save_button.text = MagicMock(return_value=settings_presenter.savetext)
    settings_presenter.handle_savebutton()
    mock_settings_view.hideTextFields.assert_called_once()

def test_handle_savebutton_set_modifytext(settings_presenter, mock_settings_view):
    setUpViewGetters(mock_settings_view)
    mock_settings_view.save_button = MagicMock()
    mock_settings_view.save_button.text = MagicMock(return_value=settings_presenter.savetext)
    settings_presenter.handle_savebutton()
    mock_settings_view.save_button.setText.assert_called_once_with(settings_presenter.modifytext)




