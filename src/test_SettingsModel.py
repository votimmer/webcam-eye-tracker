import pytest
from SettingsModel import SettingsModel

@pytest.fixture
def settings_model():
    return SettingsModel()

#--- Tests for setCalibrationRows

def test_setCalibrationRows(settings_model):
    test = '2'
    result = settings_model.setCalibrationRows(test)
    assert result == int(test)

def test_setCalibrationRows_notNumeric(settings_model):
    test = 'five'
    result = settings_model.setCalibrationRows(test)
    assert result == -1

def test_setCalibrationRows_float(settings_model):
    test = '5.0'
    result = settings_model.setCalibrationRows(test)
    assert result == -1

def test_setCalibrationRows_invalidInput(settings_model):
    test = 5
    result = settings_model.setCalibrationRows(test)
    assert result == -1

def test_setCalibrationRows_tooSmall(settings_model):
    test = '1'
    result = settings_model.setCalibrationRows(test)
    assert result == -1

def test_setCalibrationRows_tooBig(settings_model):
    test = '11'
    result = settings_model.setCalibrationRows(test)
    assert result == -1

#--- Tests for setCalibrationColumns()

def test_setCalibrationColumns(settings_model):
    test = '5'
    settings_model.setCalibrationColumns(test)
    assert settings_model.calcols == int(test)

def test_setCalibrationColumns_notNumeric(settings_model):
    test = 'five'
    result = settings_model.setCalibrationColumns(test)
    assert result == -1

def test_setCalibrationColumns_float(settings_model):
    test = '5.0'
    result = settings_model.setCalibrationColumns(test)
    assert result == -1

def test_setCalibrationColumns_invalidInput(settings_model):
    test = 5
    result = settings_model.setCalibrationColumns(test)
    assert result == -1

def test_setCalibrationColumns_tooSmall(settings_model):
    test = '1'
    result = settings_model.setCalibrationColumns(test)
    assert result == -1

def test_setCalibrationColumns_tooBig(settings_model):
    test = '11'
    result = settings_model.setCalibrationColumns(test)
    assert result == -1

#--- Tests for setValidationRows()

def test_setValidationRows(settings_model):
    test = '5'
    settings_model.setValidationRows(test)
    assert settings_model.valrows == int(test)

def test_setValidationRows_notNumeric(settings_model):
    test = 'five'
    result = settings_model.setValidationRows(test)
    assert result == -1

def test_setValidationRows_float(settings_model):
    test = '5.0'
    result = settings_model.setValidationRows(test)
    assert result == -1

def test_setValidationRows_invalidInput(settings_model):
    test = 5
    result = settings_model.setValidationRows(test)
    assert result == -1

def test_setValidationRows_tooSmall(settings_model):
    test = '0'
    result = settings_model.setValidationRows(test)
    assert result == -1

def test_setValidationRows_tooBig(settings_model):
    test = '11'
    result = settings_model.setValidationRows(test)
    assert result == -1

#--- Tests for setValidationColumns()

def test_setValidationColumns(settings_model):
    test = '5'
    settings_model.setValidationColumns(test)
    assert settings_model.valcols == int(test)

def test_setValidationColumns_notNumeric(settings_model):
    test = 'five'
    result = settings_model.setValidationColumns(test)
    assert result == -1

def test_setValidationColumns_float(settings_model):
    test = '5.0'
    result = settings_model.setValidationColumns(test)
    assert result == -1

def test_setCalibrationColumns_invalidInput(settings_model):
    test = 5
    result = settings_model.setValidationColumns(test)
    assert result == -1

def test_setValidationColumns_tooSmall(settings_model):
    test = '0'
    result = settings_model.setValidationColumns(test)
    assert result == -1

def test_setValidationColumns_tooBig(settings_model):
    test = '11'
    result = settings_model.setValidationColumns(test)
    assert result == -1

#--- Tests for setCalInterval()

def test_setCalInterval(settings_model):
    test = '500'
    settings_model.setCalInterval(test)
    assert settings_model.calinterval == int(test)

def test_setCalibrationInterval_notNumeric(settings_model):
    test = 'five'
    result = settings_model.setCalInterval(test)
    assert result == -1

def test_setCalInterval_float(settings_model):
    test = '5.0'
    result = settings_model.setCalInterval(test)
    assert result == -1

def test_setCalInterval_invalidInput(settings_model):
    test = 2500
    result = settings_model.setCalInterval(test)
    assert result == -1

def test_setCalInterval_tooSmall(settings_model):
    test = 100
    result = settings_model.setCalInterval(test)
    assert result == -1
    
#--- Tests for setSamples()

def test_setSamples(settings_model):
    test = '100'
    settings_model.setSamples(test)
    assert settings_model.samples == int(test)

def test_setSamples_notNumeric(settings_model):
    test = 'five'
    result = settings_model.setCalibrationColumns(test)
    assert result == -1

def test_setSamples_float(settings_model):
    test = '5.0'
    result = settings_model.setCalibrationColumns(test)
    assert result == -1

def test_setSamples_invalidInput(settings_model):
    test = 50
    result = settings_model.setCalibrationColumns(test)
    assert result == -1

def test_setSamples_tooSmall(settings_model):
    test = 0
    result = settings_model.setCalibrationColumns(test)
    assert result == -1

#--- Tests for setImgInterval

def test_setImgInterval(settings_model):
    test = '2500'
    settings_model.setImgInterval(test)
    assert settings_model.imginterval == int(test)

def test_setImgInterval_notNumeric(settings_model):
    test = 'five'
    result = settings_model.setImgInterval(test)
    assert result == -1

def test_setImgInterval_float(settings_model):
    test = '5.0'
    result = settings_model.setImgInterval(test)
    assert result == -1

def test_setImgInterval_invalidInput(settings_model):
    test = 2500
    result = settings_model.setImgInterval(test)
    assert result == -1

def test_setImgInterval_tooSmall(settings_model):
    test = 250
    result = settings_model.setImgInterval(test)
    assert result == -1 